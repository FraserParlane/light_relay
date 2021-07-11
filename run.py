import wiringpi
import time

def run():
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)
    print(serial)
    wiringpi.serialPuts(serial, 'P7')
    timer = 5
    for i in range(7):
        time.sleep(timer)
        print('I')
        wiringpi.serialPuts(serial, 'on')
        time.sleep(timer)
        print('O')
        wiringpi.serialPuts(serial, 'off')


if __name__ == '__main__':
    run()
