from flask import Flask, request
from lights import Lights
import requests
import flask

app = Flask(__name__)

# Define the light control class
lights = Lights()


@app.route("/")
def hello_world():
    """
    Home page.
    :return: Text
    """
    return "<p>Details at https://github.com/FraserParlane/light_relay</p>"


@app.route("/command", methods=["POST"])
def command():
    """
    Receive a command to pass to the relay.
    :return: Status 200
    """
    print(request.form, flush=True)
    lights.command(request.form)
    return flask.Response(status=200)
