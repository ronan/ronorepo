# dayboard.py
# usage: 
#   python dayboard.py [hours] [minutes]
# Run:
#   watch -n 30 'date "+%H %M" | xargs python dayboard.py'

import json
import math
import sys
import urllib
import time

import requests

DAY_START           =   6                     # 6am
NUM_HOURS           =   18                    # 6am-midnight
LEDS_PER_HOUR       =   6                     # ~30" of 144/m led strip. 6 leds x 18 hrs = 108 leds per day

LED_START_INDEX     =   10
GEOCODE_CACHE_TIME  =   60 * 60 * 24 * 7      # Re-check the location every 7 days
WEATHER_CACHE_TIME  =   60 * 60 * 2           # Re-check the weather every 2 hours

WLED_JSON_API_URL   =   "http://dayboard.local/json"

BRIGHTNESS          =   50 # 0-255


COLOR_BG            =   [   0,   0,  0]
COLOR_PAST          =   [   0,   0,  0]
FUTURE              =   [ 100, 100, 70]
DAY_MARKER          =   [ 255,   0,  0]
COLOR_TEMPS         =  [[   1,  27, 105],
                        [   1,  40, 127],
                        [   1,  70, 168],
                        [   1,  92, 197],
                        [   1, 119, 221],
                        [   3, 130, 151],
                        [  23, 156, 149],
                        [  67, 182, 112],
                        [ 121, 201,  52],
                        [ 142, 203,  11],
                        [ 224, 223,   1],
                        [ 252, 187,   2],
                        [ 247, 147,   1],
                        [ 237,  87,   1],
                        [ 229,  43,   1],
                        [ 171,   2,   2],
                        [  80,   3,   3],
                        [  80,   3,   3]]

def pp(x):
    from pprint import pprint
    pprint(x)

def cache(key, value=None, max_age=None):
    now = time.time()
    import shelve
    with shelve.open("dayboard.cache") as db:
        cache_entry = db.get(key, {})
        if value:
            db[key] = {"updated_at": now, "value": value}
        if not max_age or now - cache_entry.get("updated_at", 0) < max_age:
            return cache_entry.get("value")
        return None

def get_geocode():
    print('Reading geolocation from cache...')
    geocode = cache('geocode', max_age=GEOCODE_CACHE_TIME)
    if not geocode:
        print('Geolocating.. Beep. Boop. Bop. 🌎🌍🌏')
        import geocoder
        g = geocoder.ip('me')
        geocode = {
            "latitude":  g.latlng[0],
            "longitude": g.latlng[0],
            "timezone":  g.raw.get('timezone', 'UTC')
        }
        print(f"Geolocated at {geocode['latitude']}, {geocode['longitude']} {geocode['timezone']}")
        cache('geocode', geocode)
    return geocode

def get_colors():
    print('Reading led color data from cache...')
    colors = cache('colors', max_age=WEATHER_CACHE_TIME)
    if not colors:
        colors = [FUTURE] * NUM_HOURS * LEDS_PER_HOUR
        print('Fetching weather from the cloud. 🌦️')
        qs = urllib.parse.urlencode(dict(
            {
                "forecast_days":    "1",
                "hourly":           "apparent_temperature",
                "temperature_unit": "fahrenheit",
            },
            **get_geocode()
            ))
        temps = requests.get(f"https://api.open-meteo.com/v1/forecast?{qs}").json()

        for i in range(NUM_HOURS):
            idx = math.floor((temps['hourly']['apparent_temperature'][i + DAY_START]+ 40) / 10)
            colors[i*LEDS_PER_HOUR:(i*LEDS_PER_HOUR)+LEDS_PER_HOUR] = [COLOR_TEMPS[idx]] * LEDS_PER_HOUR

        cache('colors', colors)
    return colors

def render(hour, minute, day=-1):
    print(f"Drawing Board: {hour}:{minute}")

    if hour >= DAY_START:
        colors = get_colors()
        start = int(((hour - DAY_START) + (minute / 60)) * LEDS_PER_HOUR)
        leds = [COLOR_BG]*10 + [COLOR_PAST]*start + colors[start:]

        if day:
            leds[day] = DAY_MARKER

        payload = {
            "on": True,
            "bri": BRIGHTNESS,
            "seg": [{ "i": leds },]
        }

        # Print the colorful little dots to stdout for no reason except it's fun
        print("".join([f'\033[38;2;{led[0]};{led[1]};{led[2]}m•\033[0m' for led in leds]))
    else:
        payload = {"on": False}
        print("Night mode")

    if payload:
        requests.post(WLED_JSON_API_URL, json=payload)


t    = time.localtime()
args = dict(enumerate(sys.argv))
render( 
    int(args.get(1, t.tm_hour)), 
    int(args.get(2, t.tm_hour)),
    int(args.get(3, t.tm_wday))
)
