import os
import time
import pandas as pd
from pynput import keyboard

os.makedirs("data", exist_ok=True)

user_id = input("Enter User ID (e.g., 1, 2, 3...): ")

data = []

def on_press(key):
    """Records the timestamp when a key is pressed."""
    try:
        key_char = key.char if hasattr(key, 'char') else str(key)  
        press_time = time.time()
        data.append([key_char, press_time, "press", user_id])
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """Records the timestamp when a key is released."""
    try:
        key_char = key.char if hasattr(key, 'char') else str(key)
        release_time = time.time()
        data.append([key_char, release_time, "release", user_id])
        
        # Stop collection when 'ESC' is pressed
        if key == keyboard.Key.esc:
            return False
    except Exception as e:
        print(f"Error: {e}")

print("Please type the following phrase multiple times: 'the quick brown fox jumps over the lazy dog'")
print("Press ESC when you are finished.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

df = pd.DataFrame(data, columns=["Key", "Timestamp", "Event", "User_Label"])

file_name = f"user_{user_id}.csv"
df.to_csv(f"data/{file_name}", index=False)
print(f"Keystroke data saved to 'data/{file_name}'")
