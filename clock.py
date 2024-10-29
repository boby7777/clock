import time
from datetime import datetime
from gtts import gTTS
import pygame
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import json

# 初始化 pygame mixer
pygame.mixer.init()

running = True  # 用於控制報時的開關

# 從 JSON 檔案讀取報時訊息
with open("messages.json", "r", encoding="utf-8") as f:
    chime_messages = json.load(f)

def speak_time(message):
    tts = gTTS(text=message, lang='zh-tw')
    tts.save("message.mp3")

    pygame.mixer.music.load("message.mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def hourly_chime():
    global running
    while True:
        if running:
            now = datetime.now()
            for message in chime_messages:
                if message["time"] == f"{now.hour:02d}:00":
                    speak_time(message["message"])
                    time.sleep(60)  # 避免重複播放
            time.sleep(1)
        else:
            time.sleep(60)

# 系統匣圖示
def create_image():
    image = Image.new('RGB', (64, 64), color=(73, 109, 137))
    d = ImageDraw.Draw(image)
    d.rectangle([0, 0, 64, 64], fill=(255, 255, 255))
    d.text((10, 20), "時", fill=(0, 0, 0))
    return image

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
icon.icon = create_image()
icon.menu = pystray.Menu(
    item('開始報時', start_chime, enabled=lambda item: not running),
    item('停止報時', stop_chime, enabled=lambda item: running),
    item('退出', quit_app)
)

# 啟動系統匣
threading.Thread(target=icon.run, daemon=True).start()

# 開始背景報時
hourly_chime()