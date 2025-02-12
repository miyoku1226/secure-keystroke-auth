import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Read the data
data = pd.read_csv("data/features.csv")

if "User Label" in data.columns:
    data.rename(columns={"User Label": "User_Label"}, inplace=True)

print("Unique User Labels in Dataset:", data["User_Label"].unique())

# Calculate durations, intervals, and new features
key_durations = []
key_intervals = []
typing_speeds = []
bigram_intervals = []
pause_times = []
press_times = {}

last_timestamp = None

for index, row in data.iterrows():
    key = row["Key"]
    timestamp = row["Timestamp"]
    event = row["Event"]

    if event == "press":
        press_times[key] = timestamp
        if last_timestamp is not None:
            interval = timestamp - last_timestamp
            key_intervals.append(interval)
            if interval > 0.25:  # Pause detection (long gap between words)
                pause_times.append(interval)

        last_timestamp = timestamp

    elif event == "release" and key in press_times:
        duration = timestamp - press_times[key]
        key_durations.append(duration)
        typing_speeds.append(1 / duration if duration > 0 else 0)  # Typing speed (char/sec)
        press_times[key] = None

# Calculate bigram and trigram timing features
for i in range(1, len(key_intervals)):
    bigram_intervals.append(key_intervals[i] + key_intervals[i - 1])

# Ensure we have valid samples
if len(key_durations) < 2 or len(key_intervals) < 1:
    print("ERROR: Not enough valid keystroke samples to train the model.")
    exit(1)

# Additional Features
mean_duration = np.mean(key_durations)
std_duration = np.std(key_durations)
mean_interval = np.mean(key_intervals)
std_interval = np.std(key_intervals)
mean_typing_speed = np.mean(typing_speeds)
pause_count = len(pause_times)

# Generate feature matrix with NEW FEATURES
X = np.array([
    key_durations[:-1], 
    key_intervals, 
    bigram_intervals + [0],  # Bigram intervals (add a 0 to match length)
    typing_speeds[:-1],  # Typing speed per character
    [mean_duration] * len(key_durations[:-1]), 
    [std_duration] * len(key_durations[:-1]), 
    [mean_interval] * len(key_durations[:-1]), 
    [std_interval] * len(key_durations[:-1]),
    [mean_typing_speed] * len(key_durations[:-1]),  # Avg typing speed
    [pause_count] * len(key_durations[:-1])  # Pause frequency
]).T

# Assign user labels
y = data["User_Label"][: len(X)]  

print("Unique Classes in y:", np.unique(y))

if len(np.unique(y)) < 2:
    print("ERROR: Only one class detected in y. Model cannot be trained.")
    exit(1)

# Normalize the feature data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Reduce test set to maximize training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Train optimized SVM model
model = SVC(kernel="rbf", C=100, gamma=0.1)  # More balanced hyperparameters
model.fit(X_train, y_train)

# Make predictions and evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model trained successfully with accuracy: {accuracy * 100:.2f}%")

