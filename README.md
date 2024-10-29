# 整點報時程式

這是一個簡單的整點報時程式,可以在系統匣中運行,並提供以下功能:

1. 根據設定的時間播報語音報時
2. 可以在系統匣中開始、停止和退出報時
3. 可以從 JSON 檔案中自定義報時訊息

## 功能

- 使用 gTTS (Google Text-to-Speech) 模組播報報時語音
- 使用 pygame 模組播放報時音效
- 使用 pystray 模組在系統匣中建立報時控制功能
- 可以從 JSON 檔案中讀取自定義的報時訊息

## 使用方法

1. 確保安裝了以下依賴庫:
   - `gtts`
   - `pygame`
   - `pystray`
   - `PIL`

2. 修改 `chime_messages.json` 檔案,在其中定義想要播報的時間和訊息。格式如下:

   ```json
   [
     {
       "time": "12:00",
       "message": "12:00 了準備吃飯"
     },
     {
       "time": "18:00",
       "message": "18:00 了準備下班"
     }
   ]