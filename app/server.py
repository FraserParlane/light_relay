from flask import Flask, request
try:
    import wiringpi
except:
    pass
import time
import flask

app = Flask(__name__)


# Define the light control class
class Lights(object):

    def __init__(self):
        """
        Setup
        """

        # Define if auto lights on should occur
        self.auto = True

        # Setup the serial communication lines
        self.delay = 0.5
        wiringpi.wiringPiSetupGpio()
        self.serial = wiringpi.serialOpen('/dev/ttyS0', 9600)
        wiringpi.pinMode(6, 1)

    def send_command(self, command):
        """
        Send a command over UART to relay.
        :param command: Command
        :return: None
        """
        wiringpi.serialPuts(self.serial, command)
        time.sleep(self.delay)

    def send_trigger(self):
        """
        Send a LOW trigger to the relay to begin a sequence
        :return: None
        """
        wiringpi.digitalWrite(6, 1)
        time.sleep(self.delay)
        wiringpi.digitalWrite(6, 0)

    def demo(self):
        """
        Flash the lights to confirm communication
        :return: None
        """

        self.send_command('P1')
        for i in range(2):
            self.send_command('OP: 0001')
            self.send_trigger()
            time.sleep(2 - self.delay)

    def command(self, command):
        """
        Commands have the following keys:
            'type': either 'command' or 'trigger'.
            
        :param command:
        :return: None
        """

        # Define the command to run
        command = dict(command)
        method = list(command.keys())[0]
        kwargs = list(command.values())[0]

        # Log
        print(f'command: {command}', flush=True)
        print(f'method: {method}', flush=True)
        print(f'kwargs: {kwargs}', flush=True)

# Instantiate the lights control class
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
