import wiringpi

def run():
    wiringpi.wiringPiSetup()
    serial = wiringpi.serialOpen('/dev/ttyAMA0', 9600)
    print(serial)

if __name__ == '__main__':
    run()