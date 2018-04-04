from flask import Flask, render_template, request
import gpio_control

simplyfishy = Flask(__name__)

@simplyfishy.route('/')
def index():
    return 'Simply Fishy!'

if __name__ == '__main__':
    simplyfishy.run(host='0.0.0.0')
