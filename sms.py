import os
import twilio
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Your Twilio credentials (replace with your own)
twilio_account_sid = os.getenv('twilio_account_sid')
twilio_auth_token = os.getenv('twilio_auth_token')
twilio_number = os.getenv('twilio_number')
twilio_my_number = os.getenv('twilio_my_number')

# Create an instance of the Client
client = Client(twilio_account_sid, twilio_auth_token)


message = client.messages.create(
    body="Hey this is from Twilio.",
    from_=twilio_number,
    to=twilio_my_number
)

print(message)

# Print message SID (if needed to track the message)
print(f"Message sent with SID: {message.sid}")