import smtplib
import os
from email.mime.text import MIMEText


def send_email(receiver, subject, body):

    sender = "smarthireai.3@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, receiver, msg.as_string())
        server.quit()

        return True

    except Exception as e:
        print(f"Email sending failed for {receiver}: {e}")
        return False
