# Internship Application Manager

The **Internship Application Manager** is a Python-based tool that simplifies tracking internship applications and categorizing email responses automatically. It includes features for:
- Adding internship applications to a tracker.
- Fetching emails and categorizing responses using LLMs and sentiment analysis (positive, negative, or neutral).
- Automatically updating your Excel tracker with the latest email responses.
- Automating recurring daily checks for email updates.

---

## Features

### 1. Add Internship Applications
Easily add a new application to your Excel tracker with relevant details such as:
- Company name
- Job title
- Application date
- Internship period and location
- Application link

### 2. Fetch and Process Emails
Automatically fetch emails from the past 24 hours and:
- Identify emails related to internship applications.
- Use Bert as a judge to extract the application status:
  - **1:** Confirmation (process started or ongoing)
  - **2:** Positive response (offer or interview)
  - **3:** Negative response (rejection)
- Use of Bert to determine the company name based on email content.

### 3. Update Application Tracker
Update your Excel tracker with:
- Application status color-coded for better visibility:
  - **Blue** for positive responses.
  - **Red** for rejections.

### 4. Recurring Daily Checks
Automate the email-fetching and tracker-updating process to run daily at 8 AM. You can use Task Scheduler on Windows, or Cron Job on Linux/macOs and call: 
```bash
main.py daily_check.
```
---

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or above
- Required Python libraries:
  - pandas
  - openpyxl
  - transformers
  - beautifulsoup4
  - imaplib
  - email

You can install the required dependencies using:
```bash
pip install -r requirements.txt
```
