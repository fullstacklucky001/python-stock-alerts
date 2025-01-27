import os
import twilio
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Your Twilio credentials (replace with your own)
twilio_account_sid = os.getenv('twilio_account_sid')
twilio_auth_token = os.getenv('twilio_auth_token')
twilio_messaging_service_sid = os.getenv('messaging_service_sid')
twilio_my_number = os.getenv('twilio_my_number')

# Create an instance of the Client
client = Client(twilio_account_sid, twilio_auth_token)


message = client.messages.create(
    body="Hey this is from Twilio.",
    messaging_service_sid=twilio_messaging_service_sid,
    to=twilio_my_number
)

print(message)

# # Print message SID (if needed to track the message)
# print(f"Message sent with SID: {message.sid}")