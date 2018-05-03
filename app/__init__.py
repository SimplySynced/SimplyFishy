from flask import Flask
from flask_socketio import SocketIO
from gevent import monkey
monkey.patch_all()

# Flask Setup & Config
simplyfishy = Flask(__name__)
simplyfishy.config['SECRET_KEY'] = 'secret!'

# SocketIO setup
socketio = SocketIO(simplyfishy, async_mode='gevent')

from app import routes
from app import gpio_control


if __name__ == '__main__':
    socketio.run(simplyfishy, debug=True, host='0.0.0.0')
