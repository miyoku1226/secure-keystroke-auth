import time
import pickle
import numpy as np
from pynput import keyboard

with open("models/svm_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

data = []

def on_press(key):
    """Record the timestamp when a key is pressed."""
    try:
        key_char = key.char if hasattr(key, 'char') else str(key)
        press_time = time.time()
        data.append((key_char, press_time, "press"))
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """Record the timestamp when a key is released."""
    try:
        key_char = key.char if hasattr(key, 'char') else str(key)
        release_time = time.time()
        data.append((key_char, release_time, "release"))

        if key == keyboard.Key.esc:  # Stop recording when ESC is pressed
            return False
    except Exception as e:
        print(f"Error: {e}")

print("Please type the following passphrase for authentication: 'the quick brown fox jumps over the lazy dog'")
print("Press ESC when finished.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

press_times = {}
key_durations = []
key_intervals = []
bigram_intervals = []
typing_speeds = []
pause_times = []
last_timestamp = None

for entry in data:
    key, timestamp, event = entry
    if event == "press":
        press_times[key] = timestamp
        if last_timestamp is not None:
            interval = timestamp - last_timestamp
            key_intervals.append(interval)
            if interval > 0.25:
                pause_times.append(interval)

        last_timestamp = timestamp

    elif event == "release" and key in press_times:
        duration = timestamp - press_times[key]
        key_durations.append(duration)
        typing_speeds.append(1 / duration if duration > 0 else 0)
        press_times[key] = None

min_length = min(len(key_durations), len(key_intervals), len(typing_speeds))
key_durations = key_durations[:min_length]
key_intervals = key_intervals[:min_length]
typing_speeds = typing_speeds[:min_length]

bigram_intervals = [key_intervals[i] + key_intervals[i - 1] for i in range(1, min_length)] + [0]
mean_duration = np.mean(key_durations) if key_durations else 0
std_duration = np.std(key_durations) if key_durations else 0
mean_interval = np.mean(key_intervals) if key_intervals else 0
std_interval = np.std(key_intervals) if key_intervals else 0
mean_typing_speed = np.mean(typing_speeds) if typing_speeds else 0
pause_count = len(pause_times)

X_new = np.array([[
    key_durations[-1] if key_durations else 0,
    key_intervals[-1] if key_intervals else 0,
    bigram_intervals[-1] if bigram_intervals else 0,
    typing_speeds[-1] if typing_speeds else 0,
    mean_duration,
    std_duration,
    mean_interval,
    std_interval,
    mean_typing_speed,
    pause_count
]])

X_new = scaler.transform(X_new)

prediction = model.predict(X_new)
print(f"Predicted User: {prediction[0]}")

print("Raw X_new:", X_new)
X_new = scaler.transform(X_new)
print("Normalized X_new:", X_new)
