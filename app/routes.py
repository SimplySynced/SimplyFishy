import RPi.GPIO as GPIO
from flask import render_template, request, redirect
from flask_socketio import SocketIO, emit
from app import simplyfishy
from app import db
from app import gpio_control as gc
from app.models import Settings

# SocketIO setup
socketio = SocketIO(simplyfishy, async_mode='gevent')

# Routes
@simplyfishy.route('/')
def index():
    # For each pin, read the pin state and store it in the pins dictionary:
    for outlet in gc.outletsOrdered:
        gc.outletsOrdered[outlet]['state'] = GPIO.input(outlet)
    for float_switch in gc.float_switches:
        gc.float_switches[float_switch]['state'] = GPIO.input(float_switch)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'outlets': gc.outletsOrdered,
        'float_switches': gc.float_switches
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('home.html', **templateData)


@simplyfishy.route('/config')
def config():
    settings = Settings.query.all()
    settingsData = {
        setting.setting_name: setting.setting_value for setting in settings
    }
    return render_template('config.html', **settingsData)

@simplyfishy.route('/config/update', methods=["POST"])
def update():
    items = request.form.items()
    for setting_name, setting_value in items:
        setting = Settings.query.filter_by(setting_name=setting_name).first()
        setting.setting_value = setting_value
        db.session.commit()
    return redirect ("/config")

@simplyfishy.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Turn on pin
        GPIO.output(changePin, GPIO.HIGH)
    if action == "off":
        # Turn off pin
        GPIO.output(changePin, GPIO.LOW)

    # For each pin, read the pin state and store it in the pins dictionary:
    for outlet in gc.outlets:
        gc.outlets[outlet]['state'] = GPIO.input(outlet)

    return ''

# SocketIO
@socketio.on('my_message')
def mymessage(message):
    print('received message: ' + message)
    # emit('my_response', 'test')


@socketio.on('read_temp')
def return_temp():
    # print(read_temp())
    emit('tempprobe_1', {'data': read_temp()}, namespace='/', broadcast=True)


def read_temp_raw():
    f = open(gc.device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 0)
        return temp_f