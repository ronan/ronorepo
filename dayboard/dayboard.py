# dayboard.py
# usage: 
#   python dayboard.py [hours] [minutes]
# Run:
#   watch -n 30 'date "+%H %M" --date="5 hours ago" | xargs python dayboard.py'

import json
import math
import os
import sys
import urllib

import requests

TZ                  = "America/Chicago"
LAT                 = "44.841"
LON                 = "-93.1097",

DAY_START           = 6     # 6am
NUM_HOURS           = 18    # 6am-midnight
LEDS_PER_HOUR       = 6     # ~30" of 144/m led strip. 6 leds x 18 hrs = 108 leds per day

LED_START_INDEX     = 10

WLED_JSON_API_URL   = "http://dayboard.local/json"
WEATHER_API_URL     = "https://api.open-meteo.com/v1/forecast"

PAST                = [0, 0, 0]
FUTURE              = [100, 100, 70]

BRIGHTNESS          = 50 # 0-255

TEMPS   = [
            [   1,  27, 105],
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
            [  80,   3,   3],
]

def pp(x):
    from pprint import pprint
    pprint(x)

def get_colors():
    colors = [FUTURE] * NUM_HOURS * LEDS_PER_HOUR

    try:
        print('Fetching weather data...')
        qs = urllib.parse.urlencode({
            "latitude":         "44.841",
            "longitude":        "-93.1097",
            "timezone":         TZ,
            "forecast_days":    "1",
            "hourly":           "apparent_temperature",
            "temperature_unit": "fahrenheit",
        })
        temps = requests.get(f"https://api.open-meteo.com/v1/forecast?{qs}").json()

        for i in range(NUM_HOURS):
            idx = math.floor((temps['hourly']['apparent_temperature'][i + DAY_START]+ 40) / 10)
            colors[i*LEDS_PER_HOUR:(i*LEDS_PER_HOUR)+LEDS_PER_HOUR] = [TEMPS[idx]] * LEDS_PER_HOUR

    except Exception as e:
        print(f"Could not get weather data: {e}")
    
    return colors

def draw_board(hour, minute):
    print(f"Drawing Board: {hour}:{minute}")

    if hour >= DAY_START:
        # Hours
        start = int(((hour - DAY_START) + (minute / 60)) * LEDS_PER_HOUR)
        
        leds = [PAST]*start + get_colors()[start:]

        # Print the colorful little dots to stdout for no reason except it's fun
        print("".join([f'\033[38;2;{led[0]};{led[1]};{led[2]}m•\033[0m' for led in leds]))

        payload = {
            "on": True,
            "bri": BRIGHTNESS,
            "seg": [{ "start": LED_START_INDEX, "i": leds },]
        }
    else:
        payload = {"on": False}
        print("Night mode")

    if payload:
        requests.post(WLED_JSON_API_URL, json=payload)

if len(sys.argv) >= 3:
    hour = int(sys.argv[1])
    minute = int(sys.argv[2])
    draw_board(hour, minute)
else:
    from zoneinfo import ZoneInfo
    from datetime import datetime
    t = datetime.now(ZoneInfo(TZ))
    draw_board(t.hour, t.minute)
