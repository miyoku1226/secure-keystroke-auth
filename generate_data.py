import os
import random
import pandas as pd

os.makedirs("data", exist_ok=True)

def generate_keystroke_data(file_name, num_users=5, num_samples_per_user=200):
    """
    Generate synthetic keystroke data for multiple users with distinct typing speeds.
    """
    data = []
    base_timestamp = random.uniform(100000.0, 200000.0)  

    user_typing_speeds = {
        user_id: random.uniform(0.02, 0.05) for user_id in range(1, num_users + 1)
    }

    for user_id in range(1, num_users + 1):  
        for _ in range(num_samples_per_user):
            phrase = "the quick brown fox jumps over the lazy dog"
            press_times = {}

            for char in phrase:
                if char == " ":
                    continue  

                key = char
                press_time = base_timestamp + round(random.uniform(0.01, user_typing_speeds[user_id]), 3)
                release_time = press_time + round(random.uniform(0.05, 0.15), 3)

                data.append([key, press_time, "press", user_id])
                data.append([key, release_time, "release", user_id])

                base_timestamp = release_time  

    df = pd.DataFrame(data, columns=["Key", "Timestamp", "Event", "User_Label"])

    df.to_csv(f"data/{file_name}", index=False)
    print(f"Keystroke data saved to 'data/{file_name}'.")
    
generate_keystroke_data("features.csv", num_users=5, num_samples_per_user=150)
