import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Read the data
data = pd.read_csv("data/keystroke_data.csv")

# Calculate keys' durations and intervals
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

for i in range(1, len(key_durations)):
    key_intervals.append(key_durations[i] - key_durations[i-1])

# Generate training data
X = np.array([key_durations[:-1], key_intervals]).T
y = np.ones(len(X))  # assuming that the data is from the same user

# Divide the training set and the test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train SVM machine learning model
model = SVC(kernel="linear")
model.fit(X_train, y_train)

# Forecast and evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model trained successfully with accuracy: {accuracy * 100:.2f}%")
        