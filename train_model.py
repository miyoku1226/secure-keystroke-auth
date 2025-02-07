import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# read the data
data = pd.read_csv("data/keystroke_data.csv")

# calculate keys' durations and intervals
key_durations = []
key_intervals = []

press_times = {}

for index, row in data.iterrows():
    key = row["Key"]
    timestamp = row["Timestamp"]
    event = row["Event"]
    
    if event == "press":
        press_times[key] = timestamp
    elif event == "release" and key in press_times:
        duration = timestamp - press_times[key]
        key_durations.append(duration)
        press_times[key] = None
        