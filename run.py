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
    with open('latlon', 'r') as f:
        latlon = f.read()
    lat, lon = latlon.split(',')
    lat = float(lat)
    lon = float(lon)
    print(f'Location retrieved {lat},{lon}')
    return lat, lon


def utc_to_local(dt):
    # Convert UTC to localtime
    return dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)


def strip_timezone(dt):
    # Convert an aware datetime object into a naive one
    strformat = "%H:%M:%S"
    return datetime.datetime.strptime(dt.strftime(strformat), strformat)


def get_sunset_sunrise():
    # Get the sunset and sunrise for current location

    lat, lon = get_location()
    sun = Sun(lat, lon)
    sunrise = sun.get_sunrise_time()
    sunset = sun.get_sunset_time()

    # Convert into local timezone
    sunrise = utc_to_local(sunrise)
    sunset = utc_to_local(sunset)

    return sunrise.time(), sunset.time()


def get_now():
    # Get the current aware time
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    now = datetime.datetime.now()
    now = now.replace(tzinfo=timezone)
    return now.time()


def day_in_seconds(sunrise, sunset):
    date = datetime.date(1, 1, 1)
    sunrise_f = datetime.datetime.combine(date, sunrise)
    sunset_f = datetime.datetime.combine(date, sunset)
    length = sunset_f - sunrise_f
    return length.seconds


def minutes_to_relay_format(minutes):
    # Convert the number of minutes to the foramt of the relay
    smin = str(minutes).zfill(4)
    string = [smin[0], '.', smin[1], '.', smin[2], '.', smin[3]]
    return ''.join(string)


def warmup(serial):
    # Flash the lights to indicate successful warmup
    send_command(serial, 'P1')
    send_command(serial, f'OP: 0001')
    send_trigger()
    time.sleep(2)


def sunshine():
    # Emulate sunshine

    # Wait for the pi to fully start up
    time.sleep(10)

    # Update location
    update_location()

    # Set up wiringpi
    wiringpi.wiringPiSetupGpio()

    # Set up the UART data connection
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)

    # Set up the trigger
    wiringpi.pinMode(6, 1)

    # Send a warm up flash
    warmup(serial)

    # Configure
    send_command(serial, 'P1')

    while True:

        # Get now
        now = get_now()
        sunrise, sunset = get_sunset_sunrise()

        # If it's after sunrise and the bulb is off
        if sunrise < now < sunset:

            # Determine how long the lamp should be on
            length_sec = day_in_seconds(sunrise, sunset)
            length_min = int(length_sec / 60)
            relay_min = minutes_to_relay_format(length_min)

            # Start the relay
            send_command(serial, f'OP: {relay_min}')
            send_trigger()

            # Wait for day to end, plus an hour
            time.sleep(length_sec + 60 * 60)

        # Else, wait for sunrise
        else:
            time.sleep(60)


if __name__ == '__main__':
    sunshine()
