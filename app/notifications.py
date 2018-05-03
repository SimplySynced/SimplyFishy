from pushbullet import Pushbullet
from twilio.rest import Client
from gevent import sleep

# Set the pushbullet API key
pb = Pushbullet('')

# Set the Twilio API Authentication
account_sid = ""
auth_token = ""

twil = Client(account_sid, auth_token)

def send(msg):
    # Send Pushbullet Note
    pb.push_note('Simply Fishy', msg)

    sleep(5)

    # Send SMS via Twilio
    message = twil.messages.create(
        to="+1111111111",
        from_="+1111111111",
        body=msg
    )

    print(message)

