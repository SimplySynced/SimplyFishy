import simplyfishy
import gpio_control

if __name__ == '__main__':
    socketio.run(simplyfishy, debug=True, host='0.0.0.0')

