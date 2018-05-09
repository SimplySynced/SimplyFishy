from gevent import monkey
monkey.patch_all()
from flask import Flask
from flask_socketio import SocketIO
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Flask Setup & Config
simplyfishy = Flask(__name__)
simplyfishy.config['SECRET_KEY'] = 'secret!'
simplyfishy.config.from_object(Config)
db = SQLAlchemy(simplyfishy)
migrate = Migrate(simplyfishy, db)


# SocketIO setup
socketio = SocketIO(simplyfishy, async_mode='gevent')


from app import routes, gpio_control, models


if __name__ == '__main__':
    socketio.run(simplyfishy, debug=True, host='0.0.0.0')
