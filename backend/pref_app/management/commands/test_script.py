from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
account_sid = 'ACcb94a77d070d8e1e065eb9c0e9647142'
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)
message = client.messages.create(
messaging_service_sid='MG111ded7875b2fa3b99d8688c939a8843',
    body='hello world',
    to=f'+19786262746'
)

