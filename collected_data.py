import time
import csv
from pynput import keyboard

data = []

def on_press(key):
    """ Record the time when the button is pressed. """
    try:
        press_time = time.time()
        data.append((str(key), press_time, "press"))
    except:
        pass

def on_release(key):
    """ Record the button release time and calculate the button duration. """
    try:
        release_time = time.time()
        data.append((str(key), release_time, "release"))
        if key == keyboard.Key.esc:  # Press esc to exit the program
            return False
    except:
        pass

# Monitor keyboard input
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Store data
with open("features.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Key", "Timestamp", "Event"])
    writer.writerows(data)

print("Keystroke data saved successfully!")