import wiringpi
import time

def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)
    print(serial)
    timer = 0.3
    while True:
        time.sleep(timer)
        print('I')
        wiringpi.serialPuts(serial, 'on')
        time.sleep(timer)
        print('O')
        wiringpi.serialPuts(serial, 'off')


if __name__ == '__main__':
    run()
