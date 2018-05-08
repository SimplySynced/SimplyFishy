import RPi.GPIO as GPIO
from flask import render_template
from flask_socketio import SocketIO, emit
from app import simplyfishy
from app import gpio_control as gc

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
    outletsData = {
        'outlets': gc.outletsOrdered
    }
    floatswData = {
        'float_switches': gc.float_switches
    }
    # Pass the template data into the template main.html and return it to the user
    return render_template('home.html', **outletsData, **floatswData)


@simplyfishy.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = gc.outlets[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."
    if action == "toggle":
        # Read the pin and set it to whatever it isn't (that is, toggle it):
        GPIO.output(changePin, not GPIO.input(changePin))
        message = "Toggled " + deviceName + "."

    # For each pin, read the pin state and store it in the pins dictionary:
    for outlet in gc.outlets:
        gc.outlets[outlet]['state'] = GPIO.input(outlet)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'message': message,
        'pins': gc.outlets
    }

    return render_template('home.html', **templateData)


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
