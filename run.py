import wiringpi
import time


def send_command(serial, command):
    wiringpi.serialPuts(serial, command)
    time.sleep(0.5)


def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)
    for i in range(9):
        send_command(serial, f'OP:000{i}')


if __name__ == '__main__':
    run()
