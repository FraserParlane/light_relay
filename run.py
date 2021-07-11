from suntime import Sun
import wiringpi
import datetime
import time
import os


def send_command(serial, command):
    # Send a UART command
    wiringpi.serialPuts(serial, command)
    time.sleep(0.5)


def send_trigger():
    # Send a relay trigger
    wiringpi.digitalWrite(6, 1)
    time.sleep(0.5)
    wiringpi.digitalWrite(6, 0)


def demo():
    # Should cause the relay to flash

    # Set up wiringpi
    wiringpi.wiringPiSetupGpio()

    # Set up the UART data connection
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)

    # Set up the trigger
    wiringpi.pinMode(6, 1)

    # Configure
    send_command(serial, 'P1')
    send_command(serial, 'OP: 0001')

    while True:
        send_trigger()
        time.sleep(2)


def update_location():
    # Save the current location to file
    try:
        latlon = os.popen('curl ipinfo.io/loc').read().rstrip()
        with open('latlon', 'w') as f:
            f.write(latlon)
        print(f'Location updated ({latlon})')
    except:
        print('Location update failed.')


def get_location():
    # Get the current location
    update_location()
    with open('latlon', 'r') as f:
        latlon = f.read()
    lat, lon = latlon.split(',')
    lat = float(lat)
    lon = float(lon)
    print(f'Location retrieved {lat},{lon}')
    return lat, lon

def get_sunset_sunrise():
    # Get the sunset and sunrise for current location

    lat, lon = get_location()
    sun = Sun(lat, lon)
    sunrise = sun.get_sunrise_time()
    sunset = sun.get_sunset_time()
    return sunrise, sunset

def sunshine():

    # Emulate sunshine
    sunset, sunrise = get_sunset_sunrise()
    print(sunset)
    print(sunrise)






if __name__ == '__main__':
    # sunshine()
    demo()