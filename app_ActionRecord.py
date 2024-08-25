import pyautogui
import pyperclip
import keyboard
import time
import json
from pynput import mouse, keyboard as pynput_keyboard

# 記録するイベントを保持するリスト
events = []
start_time = time.time()  # ツール起動時の時刻
last_time = start_time    # 最後のイベント実行時刻

# 待機時間を記録する関数
def record_sleep():
    global last_time
    current_time = time.time()
    duration = current_time - last_time
    events.append({
        "event": "sleep",
        "duration": duration
    })
    last_time = current_time

# マウスのクリックイベントを記録する
def on_click(x, y, button, pressed):
    if pressed:
        record_sleep()
        events.append({
            "event": "click",
            "button": str(button),
            "position": (x, y)
        })

# マウスのスクロールイベントを記録する
def on_scroll(x, y, dx, dy):
    record_sleep()
    events.append({
        "event": "scroll",
        "position": (x, y),
        "scroll": (dx, dy)
    })

# キーボードイベントを記録する
def on_key_press(key):
    record_sleep()
    try:
        key_name = key.char
    except AttributeError:
        key_name = str(key)

    # 既に押されているキーをチェックし、同時押しを記録する
    if hasattr(keyboard, 'is_pressed'):
        pressed_keys = [str(k) for k in keyboard._pressed_events.keys() if k != key]
        pressed_keys.append(key_name)
        key_name = "+".join(pressed_keys)

    events.append({
        "event": "key",
        "name": key_name
    })

# メインの記録関数
def record_events(output_file):
    # マウスのリスナー
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    mouse_listener.start()
    
    # キーボードのリスナー
    keyboard_listener = pynput_keyboard.Listener(on_press=on_key_press)
    keyboard_listener.start()

    print("Recording... Press ESC to stop.")
    # ESCキーが押されるまで待機
    keyboard.wait('esc')

    # リスナーを停止
    mouse_listener.stop()
    keyboard_listener.stop()

    # イベントをファイルに保存
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(events, file, indent=4)

    print(f"Events saved to {output_file}")

# 記録ツールの実行
record_events('events.json')
