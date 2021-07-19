from flask import Flask, request
import requests


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Details at https://github.com/FraserParlane/light_relay</p>"


@app.route("/command", methods=["POST"])
def command():
    print('test')
    print(type(request.data))
    print(request.data)


def make_request(data):
    url = 'http://192.168.86.30:5000'
    result = requests.post(
        url=url,
        data=data
    )

if __name__ == '__main__':
    make_request('test')