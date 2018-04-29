import simplyfishy
import gpio_control
from flask_socketio import SocketIO

# SocketIO setup
socketio = SocketIO(simplyfishy, async_mode='gevent')

if __name__ == '__main__':
    socketio.run(simplyfishy.simplyfishy, debug=True, host='0.0.0.0')