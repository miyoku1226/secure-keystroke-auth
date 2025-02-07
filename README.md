# Secure Keystroke Authentication

## Overview
This project explores **keystroke dynamics as an additional security layer** for passphrase-based authentication. By analyzing the unique timing patterns of an individual’s typing behavior, we aim to enhance authentication security while maintaining user convenience.

## Motivation
Traditional password-based authentication is vulnerable to **keylogging, shoulder surfing, and brute-force attacks**. To improve security without relying on hardware tokens or biometrics, this project investigates **keystroke dynamics as a behavioral biometric**, using typing rhythm to distinguish legitimate users from impostors.

## Key Features
1. **Keystroke Dynamics Analysis** – Captures typing speed, key press duration, and inter-key intervals  
2. **Machine Learning Integration** – Uses **Support Vector Machines (SVM)** for user authentication  
3. **Lightweight & Usable** – Designed for minimal computational overhead, no extra hardware required  

## Methodology
1. **Data Collection** – We collected **keystroke timing data** from multiple test users while typing a predefined passphrase.  
2. **Feature Engineering** – Extracted key press duration, inter-key intervals, and digraph latency.  
3. **Model Training** – Implemented **SVM** for binary classification of legitimate vs. fraudulent users.  
4. **Evaluation** – Measured **False Acceptance Rate (FAR)** and **False Rejection Rate (FRR)** to optimize performance.  

## Future Work
- Expand dataset for better model generalization.
- Implement multi-factor authentication.
- Improve user experience with real-time feedback.

## Contact
For inquiries, please reach out to me at miyoku1226@gmail.com.