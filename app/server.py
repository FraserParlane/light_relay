import flask
from flask import Flask, request
import requests

app = Flask(__name__)

a = 'defined'

@app.route("/")
def hello_world():
    return "<p>Details at https://github.com/FraserParlane/light_relay</p>"


@app.route("/command", methods=["POST"])
def command():
    """
    Receive a command to pass to the relay.
    :return:
    """
    print(request.form, flush=True)
    print(a, flush=True)
    return flask.Response(status=200)


def make_request():
    url = 'http://192.168.86.30:5000/command'
    result = requests.post(
        url=url,
        data={'data': 'value'}
    )



if __name__ == '__main__':
    make_request()
