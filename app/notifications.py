from pushbullet import Pushbullet
from twilio.rest import Client
from gevent import sleep

# Set the pushbullet API key
pb = Pushbullet('o.RuyUUVhDC9HOP7E80jxpKVvfaf4KShvR')

# Set the Twilio API Authentication
account_sid = "ACc2b7afbebcfaf51c88108150f3adaf7c"
auth_token = "fb6adbc88b2407b1d479e65a74ed4125"

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
        to="+12158331298",
        from_="+12153467365",
        body=msg
    )

    print(message)
