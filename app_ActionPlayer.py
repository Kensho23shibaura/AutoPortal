import pyautogui
import time
import json
import pyperclip
from PIL import ImageGrab

# クリップボードの内容を保存する関数
def save_clipboard_content(folder_path):
    try:
        clipboard_content = ImageGrab.grabclipboard()
        if clipboard_content is None:
            clipboard_content = pyperclip.paste()
            file_extension = ".txt"
            file_content = clipboard_content
        else:
            file_extension = ".png"
            clipboard_content.save(file_path)
            file_content = None

        timestamp = int(time.time())
        file_path = f"{folder_path}/clipboard_{timestamp}{file_extension}"
        if file_content is not None:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
        else:
            clipboard_content.save(file_path)

        print(f"Clipboard content saved to {file_path}")
    except Exception as e:
        print(f"Failed to save clipboard content: {e}")

# 操作を再実行する関数
def replay_events(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        events = json.load(file)

    for event in events:
        if event["event"] == "sleep":
            time.sleep(event["duration"])
        
        elif event["event"] == "click":
            x, y = event["position"]
            pyautogui.click(x, y, button=event["button"])
        
        elif event["event"] == "scroll":
            x, y = event["position"]
            dx, dy = event["scroll"]
            pyautogui.scroll(dy, x, y)
        
        elif event["event"] == "key":
            keys = event["name"].split("+")
            for key in keys:
                pyautogui.keyDown(key)
            for key in keys:
                pyautogui.keyUp(key)
        
        elif event["event"] == "clipboard_save":
            folder_path = event["folder_path"]
            save_clipboard_content(folder_path)

        time.sleep(0.1)  # 各操作間に短い待機時間を挟む

# 再実行ツールの実行
replay_events('events.json')
