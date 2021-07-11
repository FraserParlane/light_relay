import wiringpi
import time

def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)
    wiringpi.serialPuts(serial, 'P3')
    wiringpi.serialPuts(serial, 'OP1131')


if __name__ == '__main__':
    run()
