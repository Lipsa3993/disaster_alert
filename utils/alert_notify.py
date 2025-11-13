from twilio.rest import Client
import os

def send_sms(alerts, recipient_number):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")

    if not all([account_sid, auth_token, twilio_number]):
        print("Twilio credentials missing.")
        return False
    if not alerts:
        return False

    message_body = "\n".join(f"- {a}" for a in alerts)
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=recipient_number
        )
        print(f"SMS sent! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False
