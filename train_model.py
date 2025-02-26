import os
import pickle
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

os.makedirs("models", exist_ok=True)

data_list = []

features_path = "data/features.csv"
if os.path.exists(features_path):
    print("Loading synthetic data from 'features.csv'...")
    features_data = pd.read_csv(features_path)
    data_list.append(features_data)

data_path = "data/"
for file in os.listdir(data_path):
    if file.startswith("user_") and file.endswith(".csv"):
        print(f"Loading real user data from '{file}'...")
        user_data = pd.read_csv(os.path.join(data_path, file))
        data_list.append(user_data)

if not data_list:
    print("ERROR: No data found! Please generate synthetic data or collect real data.")
    exit(1)

data = pd.concat(data_list, ignore_index=True)

if "User Label" in data.columns:
    data.rename(columns={"User Label": "User_Label"}, inplace=True)

print("Unique User Labels in Dataset:", np.unique(data["User_Label"]))

key_durations = []
key_intervals = []
typing_speeds = []
bigram_intervals = []
pause_times = []
user_labels = []

press_times = {}
last_timestamp = None

for index, row in data.iterrows():
    key = row["Key"]
    timestamp = row["Timestamp"]
    event = row["Event"]
    user_label = row["User_Label"]

    if event == "press":
        press_times[key] = timestamp
        if last_timestamp is not None:
            interval = timestamp - last_timestamp
            key_intervals.append(interval)
            if interval > 0.25:
                pause_times.append(interval)
        last_timestamp = timestamp

    elif event == "release":
        if key in press_times and press_times[key] is not None:
            duration = timestamp - press_times[key]
            key_durations.append(duration)
            typing_speeds.append(1 / duration if duration > 0 else 0)
            press_times[key] = None  # Reset
            user_labels.append(user_label) 

min_length = min(len(key_durations), len(key_intervals), len(typing_speeds), len(user_labels))

key_durations = key_durations[:min_length]
key_intervals = key_intervals[:min_length]
typing_speeds = typing_speeds[:min_length]
pause_times = pause_times[:min_length]
bigram_intervals = [key_intervals[i] + key_intervals[i - 1] for i in range(1, min_length)] + [0]
user_labels = user_labels[:min_length]

if len(key_durations) < 2 or len(user_labels) < 2:
    print("ERROR: Not enough valid keystroke samples to train the model.")
    exit(1)

y = np.array(user_labels)

mean_duration = np.mean(key_durations)
std_duration = np.std(key_durations)
mean_interval = np.mean(key_intervals)
std_interval = np.std(key_intervals)
mean_typing_speed = np.mean(typing_speeds)
pause_count = len(pause_times)

X = np.array([
    key_durations, 
    key_intervals, 
    bigram_intervals,  
    typing_speeds,  
    [mean_duration] * min_length, 
    [std_duration] * min_length, 
    [mean_interval] * min_length, 
    [std_interval] * min_length,
    [mean_typing_speed] * min_length,  
    [pause_count] * min_length  
]).T

print("Final unique classes in y:", np.unique(y))

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

model = SVC(kernel="rbf", C=1, gamma=0.01)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model trained successfully with accuracy: {accuracy * 100:.2f}%")

with open("models/svm_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Trained model saved to 'models/svm_model.pkl'!")
print("Scaler saved to 'models/scaler.pkl'!")

print("Scaler mean:", scaler.mean_)
print("Scaler variance:", scaler.var_)