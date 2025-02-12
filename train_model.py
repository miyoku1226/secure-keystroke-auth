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

# Calculate durations and intervals
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

# Ensure we have valid samples
if len(key_durations) < 2 or len(key_intervals) < 1:
    print("ERROR: Not enough valid keystroke samples to train the model.")
    exit(1)

# Generate feature matrix
X = np.array([key_durations[:-1], key_intervals]).T
y = data["User_Label"][: len(X)]  

print("Unique Classes in y:", np.unique(y))

if len(np.unique(y)) < 2:
    print("ERROR: Only one class detected in y. Model cannot be trained.")
    exit(1)

# Normalize the feature data
scaler = StandardScaler()
X = scaler.fit_transform(X) * 5  # Expanding feature range

# Split data (smaller test set to improve learning)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

# Train optimized SVM model
model = SVC(kernel="rbf", C=500, gamma=0.05)  # Adjusted hyperparameters
model.fit(X_train, y_train)

# Make predictions and evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model trained successfully with accuracy: {accuracy * 100:.2f}%")
