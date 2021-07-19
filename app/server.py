from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Details at https://github.com/FraserParlane/light_relay</p>"


@app.route("/command", methods=["POST"])
def command():
    print(request.data)