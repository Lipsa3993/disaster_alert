import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

def send_test_email():
    load_dotenv()

    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    recipient = "pambica6@gmail.com"  # send test to yourself

    msg = MIMEText("This is a test email from Disaster Alert System.")
    msg['Subject'] = "Test Email"
    msg['From'] = EMAIL_USER
    msg['To'] = recipient

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Email failed:", e)


if __name__ == "__main__":
    send_test_email()
