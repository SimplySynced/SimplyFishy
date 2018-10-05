from pushbullet import Pushbullet
from twilio.rest import Client
from app.models import Settings
from gevent import monkey
monkey.patch_all()

pb_api = Settings.query.filter_by(setting_name='pushbullet_api').one()
tas = Settings.query.filter_by(setting_name='twilio_account_sid').one()
tat = Settings.query.filter_by(setting_name='twilio_auth_token').one()

# Set the pushbullet API key
pb = Pushbullet(pb_api.setting_value)


# Set the Twilio API Authentication
twil = Client(tas.setting_value, tat.setting_value)


def send(msg):

    # Send to Pushbullet
    if Settings.query.filter_by(setting_name='pushbullet_enabled').one()==0:
        pushbullet(msg)

    # Send to Twilio
    if Settings.query.filter_by(setting_name='twilio_enabled').one()==0:
        twilio(msg)


def pushbullet(msg):
    # Send Pushbullet Note
    pb.push_note('Simply Fishy', msg)


def twilio(msg):
    twilto = Settings.query.filter_by(setting_name='twilio_to_num').one()
    twilfrom = Settings.query.filter_by(setting_name='twilio_from_num').one()

    message = twil.messages.create(
        to=twilto.setting_value,
        from_=twilfrom.setting_value,
        body=msg
    )

    print(message)
