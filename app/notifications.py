from pushbullet import Pushbullet
from twilio.rest import Client

# Set the pushbullet API key
pb = Pushbullet('**')

# Set the Twilio API Authentication
account_sid = "**"
auth_token = "**"

twil = Client(account_sid, auth_token)

def send(msg):
    # Send Pushbullet Note
    pb.push_note('Simply Fishy', msg)



    # Send SMS via Twilio
    message = twil.messages.create(
        to="+1111",
        from_="+1111",
        body=msg
    )

    print(message)
