from pushbullet import Pushbullet
from twilio.rest import Client
from gevent import sleep

# Set the pushbullet API key
pb = Pushbullet('pbid')

# Set the Twilio API Authentication
account_sid = "asid"
auth_token = "auth"

twil = Client(account_sid, auth_token)


def send(msg):

    # Send to Pushbullet
    pushbullet(msg)

    sleep(5)

    # Send to Twilio
    twilio(msg)


def pushbullet(msg):
    # Send Pushbullet Note
    pb.push_note('Simply Fishy', msg)


def twilio(msg):

    message = twil.messages.create(
        to="twilto",
        from_="twilfrom",
        body=msg
    )

    print(message)
