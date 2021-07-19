import requests
try:
    import wiringpi
except:
    pass
import time


class Lights(object):

    def __init__(self):
        """
        Setup the serial communication lines
        """
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
        self.demo()


def make_request():
    url = 'http://192.168.86.30:5000/command'
    result = requests.post(
        url=url,
        data={'data': 'value'}
    )


if __name__ == '__main__':
    make_request()
