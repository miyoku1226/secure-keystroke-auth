# Secure Keystroke Authentication

## Overview
Secure Keystroke Authentication is a biometric-based authentication system that leverages keystroke dynamics to enhance security. By analyzing typing patterns, such as key press durations and transition times, this project aims to provide an additional layer of authentication beyond traditional password-based methods.

## Features
- Collects keystroke timing data to create a unique user profile.
- Trains a machine learning model (Support Vector Machine) for user authentication.
- Detects unauthorized users based on typing behavior.
- Lightweight and does not require additional hardware.

## Project Structure
```
├── collected_data.py       # Script to collect keystroke data
├── train_model.py          # Script to train SVM model for authentication
├── keystroke_auth.py       # Main authentication script
├── requirements.txt        # Required dependencies
├── README.md               # Project documentation
└── research_paper.pdf      # Research paper detailing the project
```

## Installation
### Clone the Repository
```sh
 git clone https://github.com/miyoku1226/secure-keystroke-auth.git
 cd secure-keystroke-auth
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage
### Collect Keystroke Data
Run the script to record typing behavior for different users:
```sh
python collected_data.py
```

### Train the Authentication Model
After collecting sufficient data, train the SVM model:
```sh
python train_model.py
```

### Authenticate a User
Once the model is trained, run the authentication process:
```sh
python keystroke_auth.py
```

## Example Results
| Model      | Accuracy | False Accept Rate (FAR) | False Reject Rate (FRR) |
|------------|----------|-----------------|-----------------|
| SVM        | 85%      | 5%              | 10%             |
| KNN        | 82%      | 7%              | 12%             |

## Future Improvements
- Improve accuracy by testing with a larger dataset.
- Implement additional classification models (e.g., neural networks).
- Develop a GUI for user-friendly interaction.
- Test the system on different keyboard layouts and devices.

## References
- [Keystroke Dynamics in Cybersecurity](https://scholar.google.com/)
- [Support Vector Machines in Biometrics](https://arxiv.org/)

## License
This project is open-source under the MIT License.


