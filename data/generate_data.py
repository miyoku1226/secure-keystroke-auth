import random
import pandas as pd

def generate_keystroke_data(user_id, num_samples=20):
    """ Generate synthetic keystroke data, simulating key press durations and intervals. """
    data = []
    for _ in range(num_samples):
        # Simulate key press durations (0.08s ~ 0.15s)
        durations = [round(random.uniform(0.08, 0.15), 3) for _ in range(10)]
        
        # Simulate key intervals (0.1s ~ 0.3s)
        intervals = [round(random.uniform(0.1, 0.3), 3) for _ in range(9)]
        
        # Simulate total typing time (3.0s ~ 4.0s)
        typing_speed = round(random.uniform(3.0, 4.0), 2)
        
        # Combine features into a single row
        row = durations + intervals + [typing_speed, user_id]
        data.append(row)
    
    # Feature column names
    duration_cols = [f"Duration_{i+1}" for i in range(10)]
    interval_cols = [f"Interval_{i+1}" for i in range(9)]
    columns = duration_cols + interval_cols + ["Typing_Speed", "User_Label"]
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=columns)
    return df

# Generate synthetic data for multiple users
all_data = []
for user_id in range(1, 6):  # Simulate 5 users
    user_data = generate_keystroke_data(user_id)
    all_data.append(user_data)

# Combine data from all users
final_data = pd.concat(all_data, ignore_index=True)

# Save to CSV file
final_data.to_csv("data/features.csv", index=False)
print("Synthetic keystroke data has been saved to 'data/features.csv'!")
