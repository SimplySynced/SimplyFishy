import RPi.GPIO as GPIO
import glob
from app import simplyfishy
from flask_socketio import emit
from collections import OrderedDict

# Set the GPIO mode to Broadcom
GPIO.setmode(GPIO.BCM)

# Create a dictionary for the outlets and their status:
outlets = OrderedDict({
    # 4:  {'name': 'Outlet 1', 'state': 3},
    14: {'name': 'Outlet 2', 'state': 3},
    15: {'name': 'Outlet 3', 'state': 3},
    17: {'name': 'Outlet 4', 'state': 3},
    18: {'name': 'Outlet 5', 'state': 3},
    27: {'name': 'Outlet 6', 'state': 3},
    22: {'name': 'Outlet 7', 'state': 3},
    23: {'name': 'Outlet 8', 'state': 3}
})

# Set each pin as an output and make it low:
for outlet in outlets:
    GPIO.setup(outlet, GPIO.OUT)
    GPIO.output(outlet, GPIO.LOW)


# Define functions for turning outlets on and off
def outlet_on(out_num):
    GPIO.output(out_num, GPIO.HIGH)
    outlets[out_num]['state'] = GPIO.HIGH
    print(outlets[out_num]['name'] + " is now on!")


def outlet_off(out_num):
    GPIO.output(out_num, GPIO.LOW)
    outlets[out_num]['state'] = GPIO.LOW
    print(outlets[out_num]['name'] + " is now off!")

# Create a dictionary for sensors ans their status
float_switches = OrderedDict({
    24: {'name': 'Float Switch 1', 'state': GPIO.LOW},
    25: {'name': 'Float Switch 2', 'state': GPIO.LOW}
})

# Setup float switches
for float_switch in float_switches:
    GPIO.setup(float_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Define callback function for event detection
def floatsw(channel):
    with simplyfishy.app_context():
        if GPIO.input(channel):
            print(float_switches[channel]['name'] + " deactivated!")
            emit('float_sw', {'data': 'ATO level is Ok.'}, namespace='/', broadcast=True)
        else:
            print(float_switches[channel]['name'] + " activated!")
            emit('float_sw', {'data': 'ATO water level is low!'}, namespace='/', broadcast=True)


GPIO.add_event_detect(24, GPIO.BOTH, callback=floatsw, bouncetime=1000)
GPIO.add_event_detect(25, GPIO.BOTH, callback=floatsw, bouncetime=1000)

# Setup Temp Probes
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
