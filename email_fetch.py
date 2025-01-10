import time
from itertools import chain
import email
import imaplib
import os
import re
import pandas as pd
from email.header import decode_header
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def get_daily_email():
    EMAIL_ACCOUNT = "EMAIL"
    EMAIL_PASSWORD = "PASSWORD"

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    date_24hrs_ago = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

    status, messages = mail.search(None, f'SINCE {date_24hrs_ago}')

    email_ids = messages[0].split()
    emails = pd.DataFrame(columns=['From', 'Subject', 'Body'])

    if email_ids:
        print(f"Found {len(email_ids)} emails received since {date_24hrs_ago}.")
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject = decode_header(msg["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(errors="ignore")  

                    sender = msg.get("From")
                    if sender:
                        sender = re.sub(r"<.*?>", "", sender).strip()  

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode(errors="ignore").strip()
                            elif content_type == "text/html":
                                html_body = part.get_payload(decode=True).decode(errors="ignore")
                                body = BeautifulSoup(html_body, "html.parser").get_text(strip=True).strip()
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            body = msg.get_payload(decode=True).decode(errors="ignore").strip()
                        elif content_type == "text/html":
                            html_body = msg.get_payload(decode=True).decode(errors="ignore")
                            body = BeautifulSoup(html_body, "html.parser").get_text(strip=True).strip()

                    new_email = [sender, subject, body]
                    emails.loc[len(emails)] = new_email
    else:
        print(f"No emails received since {date_24hrs_ago}.")

    emails.to_csv('mails.csv', index=False)
    print("Daily emails successully fetched")
    mail.close()
    mail.logout()
    
