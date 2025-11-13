from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get Twilio credentials from environment
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')
recipient_number = '+919348223325'  # Replace with your recipient number with country code

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send SMS
try:
    message = client.messages.create(
        body="Hello! This is a test message from Twilio.",
        from_=twilio_number,
        to=recipient_number
    )
    print("Message sent! SID:", message.sid)
except Exception as e:
    print("Failed to send SMS:", e)
