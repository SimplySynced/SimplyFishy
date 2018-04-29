from flask import Flask, render_template
from flask_socketio import SocketIO
import gpio_control
from gevent import monkey
monkey.patch_all()

simplyfishy = Flask(__name__)
simplyfishy.config['SECRET_KEY'] = 'secret!'

# SocketIO setup
socketio = SocketIO(simplyfishy, async_mode='gevent')


# Routes
@simplyfishy.route('/')
def index():
    return render_template('home.html')


@socketio.on('my_message')
def mymessage(message):
    print('received message: ' + message)
    # emit('my_response', 'test')


if __name__ == '__main__':
    socketio.run(simplyfishy, debug=True, host='0.0.0.0')


