from flask import Flask, request
import requests


app = Flask(__name__)


@app.route("/")
def hello_world():
    printer('Home pinged')
    return "<p>Details at https://github.com/FraserParlane/light_relay</p>"


@app.route("/command", methods=["POST"])
def command():
    printer('Command received')
    printer(request.form)


def printer(msg):
    print(msg, flush=True)


def make_request():
    url = 'http://192.168.86.30:5000/command'
    result = requests.post(
        url=url,
        data={'data': 'value'}
    )


if __name__ == '__main__':
    make_request()
