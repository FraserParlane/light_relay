import wiringpi
import time

def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)
    wiringpi.serialPuts(serial, 'P2')
    wiringpi.serialPuts(serial, 'OP:1111')


if __name__ == '__main__':
    run()
