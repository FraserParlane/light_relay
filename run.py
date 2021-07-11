import wiringpi
import time

def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)
    while True:
        print(serial)
        time.sleep(0.5)
        wiringpi.serialPuts(serial, 'P2')
        time.sleep(0.5)
        wiringpi.serialPuts(serial, 'off')

if __name__ == '__main__':
    run()