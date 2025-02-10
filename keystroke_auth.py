import time
import pickle
import numpy as np
from pynput import keyboard

# Load the trained model
with open("results/svm_model.pkl", "rb") as f:
    model = pickle.load(f)

data = []

def on_press(key):
    """ Record the time when the key is pressed. """
    try:
        press_time = time.time()
        data.append((str(key), press_time, "press"))
    except:
        pass

def on_release(key):
    """ Record the key release time and calculate the key duration. """
    try:
        release_time = time.time()
        data.append((str(key), release_time, "release"))
        if key == keyboard.Key.esc:  # Press ESC to exit the program
            return False
    except:
        pass

# Monitor keyboard input
print("Please type your passphrase for authentication...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Calculate features
press_times = {}
key_durations = []
key_intervals = []

for entry in data:
    key, timestamp, event = entry
    if event == "press":
        press_times[key] = timestamp
    elif event == "release" and key in press_times:
        duration = timestamp - press_times[key]
        key_durations.append(duration)
        press_times[key] = None

for i in range(1, len(key_durations)):
    key_intervals.append(key_durations[i] - key_durations[i-1])

# Construct the characterisric data
X_new = np.array([key_durations[:-1], key_intervals]).T

# Predict identity
prediction = model.predict([X_new.flatten()])

if prediction[0] == 1:
    print("Authentication Successful! Welcome back.")
else:
    print("Authentication Failed! Identity mismatch detected.")