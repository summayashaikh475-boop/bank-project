----------Bank Management System (Python)----------

A simple command-line banking system built using Python with JSON-based data storage.

#Features
Create account with PIN validation
Login system with limited attempts
Temporary account lock after failed attempts
Deposit and withdraw money
Transfer money between users
Transaction history with ID and timestamp
Persistent data storage using JSON

#Files
accounts.json
auth.py
main.py
models.py
storage.py
utils.py
full_project.py

#How to Run
Run the main file:
python full_project.py

#Notes
PIN must be 4 digits and cannot be weak patterns
Accounts are locked for 5 minutes after 3 wrong attempts
All transactions are saved automatically


This project was built to practice Python concepts like classes, file handling, JSON storage, and basic authentication logic.
