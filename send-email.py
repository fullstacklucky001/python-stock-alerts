from __future__ import print_function

import base64
import os.path
import smtplib

from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os
import sys

load_dotenv()  # load environment variables from .env file
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

# user token storage
USER_TOKENS = './tmp/google_token.json'

# application credentials
CREDENTIALS = './tmp/credentials.json'

def getToken() -> str:
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(USER_TOKENS):
        creds = Credentials.from_authorized_user_file(USER_TOKENS, SCOPES)
        creds.refresh(Request())
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(USER_TOKENS, 'w') as token:
            token.write(creds.to_json())

    return creds.token


def generate_oauth2_string(username, access_token) -> str:
    auth_string = 'user=' + username + '\1auth=Bearer ' + access_token + '\1\1'
    return base64.b64encode(auth_string.encode('ascii')).decode('ascii')

def send_email(msg):
    host = "smtp.gmail.com"
    port = 587
    access_token = getToken()
    username = os.getenv("from_email")
    auth_string = generate_oauth2_string(username, access_token)

    msg = MIMEText(msg)
    msg['Subject'] = 'Stock Alert'
    msg['From'] = username
    msg['To'] = ', ' + os.getenv("cell_number")

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(username, [os.getenv("cell_number")], msg.as_string())
    server.quit()

print(sys.argv[1])
send_email(sys.argv[1])