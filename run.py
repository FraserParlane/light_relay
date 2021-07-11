from suntime import Sun
try:
    import wiringpi
except:
    pass
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
        print(f'Location updated: {latlon}')

    except:
        print('Location update failed.')


def get_location():
    # Get the current location
    with open('latlon', 'r') as f:
        latlon = f.read()
    lat, lon = latlon.split(',')
    lat = float(lat)
    lon = float(lon)
    print(f'Location retrieved: {lat},{lon}')
    return lat, lon


def utc_to_local(dt):
    # Convert UTC to localtime
    return dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)


def strip_timezone(dt):
    # Convert an aware datetime object into a naive one
    strformat = "%H:%M:%S"
    return datetime.datetime.strptime(dt.strftime(strformat), strformat)


def get_sunrise_sunset():
    # Get the sunset and sunrise for current location

    lat, lon = get_location()
    sun = Sun(lat, lon)
    sunrise = sun.get_sunrise_time()
    sunset = sun.get_sunset_time()

    # Convert into local timezone
    sunrise = utc_to_local(sunrise)
    sunset = utc_to_local(sunset)

    # Strip time
    sunrise = sunrise.time()
    sunset = sunset.time()

    print(f'first (sunrise): {sunrise}')
    print(f'second (sunset): {sunset}')
    return sunrise, sunset


def get_now():
    # Get the current aware time
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    now = datetime.datetime.now()
    now = now.replace(tzinfo=timezone)
    return now.time()


def dur_in_seconds(sunrise, sunset, offset=0):
    date0 = datetime.date(1, 1, 1)
    date1 = datetime.date(1, 1, 1 + offset)
    sunrise_f = datetime.datetime.combine(date0, sunrise)
    sunset_f = datetime.datetime.combine(date1, sunset)
    length = sunset_f - sunrise_f
    return length.seconds


def minutes_to_relay_format(minutes):
    # Convert the number of minutes to the format of the relay
    smin = str(minutes).zfill(4)
    string = smin[0] + smin[1] + '..' + smin[2] + '.' + smin[3] + '.'
    return string


def warmup(serial):
    # Flash the lights to indicate successful warmup
    send_command(serial, 'P1')
    send_command(serial, f'OP: 0001')
    send_trigger()
    time.sleep(2)


def sunshine():
    # Emulate sunshine

    # Wait for the pi to fully start up
    print('Waiting for Pi to warm up')
    # time.sleep(10)

    # Update location
    print('Updating location')
    update_location()

    # Set up wiringpi
    print('Setting up GPIO')
    wiringpi.wiringPiSetupGpio()
    serial = wiringpi.serialOpen('/dev/ttyS0', 9600)
    wiringpi.pinMode(6, 1)

    # Send a warm up flash
    print('Running warmup')
    warmup(serial)

    # Configure
    send_command(serial, 'P1')

    while True:

        # Get now
        now = get_now()
        sunrise, sunset = get_sunrise_sunset()
        print(f'Sunrise: {sunrise}')
        print(f'Sunset: {sunset}')

        # If it is during the day
        if sunrise < now < sunset:

            print('Daytime triggered')

            # Determine how long the lamp should be on
            length_sec = dur_in_seconds(now, sunset)
            length_min = int(length_sec / 60)
            length_h = length_sec / 60 / 60
            print(f'On time sec: {length_sec}')
            print(f'On time min: {length_min}')
            print(f'On time h: {length_h}')
            relay_min = minutes_to_relay_format(length_min)
            print(f'Relay format: {relay_min}')

            # Start the relay
            send_command(serial, f'OP:e{relay_min}')
            send_trigger()

            # Wait for day to end, plus an hour
            time.sleep(length_sec + 60 * 60)

        # TODO write better logic so there's a timer for the night

        # Else, wait for sunrise
        else:
            length_sec = dur_in_seconds(now, sunrise, offset=1)
            print(f'Waiting {length_sec}')
            time.sleep(length_sec)

if __name__ == '__main__':
    sunshine()
