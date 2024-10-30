import os
import time
from datetime import datetime
from gtts import gTTS
import pygame
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import json
import uuid

# 初始化 pygame mixer
pygame.mixer.init()

running = True  # 用於控制報時的開關

# 從 JSON 檔案讀取報時訊息
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 解析工作開始和結束時間
work_start_time = datetime.strptime(config["work_start_time"], "%H:%M").time()
work_end_time = datetime.strptime(config["work_end_time"], "%H:%M").time()

def speak_time(message):
    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=message, lang='zh-tw')
    tts.save(filename)
    time.sleep(1) # 等待檔案寫入

    print(message)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove(filename)

def within_work_hours():
    """判斷目前是否在設定的工作時間內"""
    now = datetime.now().time()
    return work_start_time <= now <= work_end_time

def hourly_chime():
    global running
    while True:
        if running and within_work_hours:
            now = datetime.now()
            found_message = False
            for message in config["chime_messages"]:
                if message["time"] == f"{now.hour:02d}:{now.minute:02d}":
                    found_message = True
                    speak_time(message["message"])
                    break
            if now.minute == 0 and found_message == False:
                speak_time(f"現在是 {now.hour:02d}:00")
            time.sleep(60)  # 避免重複播放
        else:
            time.sleep(60) # 每分鐘檢查一次


def start_chime(icon, item):
    global running
    if not running:
        running = True
        threading.Thread(target=hourly_chime, daemon=True).start()

def stop_chime(icon, item):
    global running
    running = False

def quit_app(icon, item):
    global running
    running = False
    icon.stop()

icon = pystray.Icon("clock")
icon.icon = Image.open('clock.png')  # 直接讀取 PNG 圖片
icon.menu = pystray.Menu(
    item('開始報時', start_chime, enabled=lambda item: not running),
    item('停止報時', stop_chime, enabled=lambda item: running),
    item('退出', quit_app)
)

# 啟動系統匣
threading.Thread(target=icon.run, daemon=True).start()

# 開始背景報時
hourly_chime()