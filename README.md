
# Reply Classifier

## Project Overview
Reply Classifier is a simple Python application that analyses written messages and classifies them into different categories.

It helps identify whether a reply is Positive, Negative, Mixed or Neutral.

## Features
- Classifies positive and negative replies.
- Identifies mixed and neutral messages.
- Detects urgent messages.
- Identifies messages that require follow-up.
- Assigns message priority: NORMAL, HIGH or URGENT.
- Saves classified messages in a CSV file.
- Provides a simple graphical user interface using Tkinter.

## Technologies Used
- Python
- Tkinter
- CSV
- Unittest

## Project Files
- `reply_classifier.py` – Main application and classification logic.
- `test_reply_classifier.py` – Automated tests.
- `classified_replies.csv` – Stores classified messages.
- `README.md` – Project documentation.

## How to Run

1. Open Command Prompt.
2. Navigate to the project folder:
   `cd C:\Users\Admin\ReplyClassifier`
3. Run:
   `python reply_classifier.py`

## How to Run Tests

Run:
`python -m unittest discover -v`

## Expected Output
The application displays:
- Category
- Priority
- Follow-up requirement

## Project Status
Basic classification, graphical interface, CSV saving and automated tests are implemented.
