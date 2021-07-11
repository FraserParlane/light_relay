import wiringpi
import time

def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)
    print(serial)
    while True:
        time.sleep(0.5)
        print('I')
        wiringpi.serialPuts(serial, 'on')
        time.sleep(0.5)
        print('O')
        wiringpi.serialPuts(serial, 'off')


if __name__ == '__main__':
    run()
