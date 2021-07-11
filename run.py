import wiringpi
import time


def send_command(serial, command):
    # Send a UART command
    wiringpi.serialPuts(serial, command)
    time.sleep(0.1)


def send_trigger():
    # Send a relay trigger
    wiringpi.digitalWrite(6, 1)
    time.sleep(0.1)
    wiringpi.digitalWrite(6, 0)


def run():

    # Set up wiringpi
    wiringpi.wiringPiSetupGpio()

    # Set up the UART data connection
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)

    # Set up the trigger
    wiringpi.pinMode(6, 1)

    # Configure
    send_command(serial, 'P1')
    send_command(serial, 'OP:0001')

    while True:
        send_trigger()
        time.sleep(2)



if __name__ == '__main__':
    run()
