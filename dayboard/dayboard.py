# dayboard.py
# usage: 
#   python dayboard.py [hours] [minutes]
# Run:
#   watch 'date "+%H %M" --date="5 hours ago" | xargs python dayboard.py'

import math
import sys
import requests

hour = int(sys.argv[1])
minute = int(sys.argv[2])
print(f"Time: {hour}:{minute}")

WLED_JSON_API_URL = "http://dayboard.local/json"

DAY_START = 6                           # 6am
NUM_HOURS = 18                          # 6am-midnight

LEDS_PER_HOUR = 6                       # ~30" of 144/m led strip
DAY_LEDS = NUM_HOURS * LEDS_PER_HOUR    # 108

OFF     = [0,0,0]
PAST    = [0, 0, 0]
FUTURE  = [100, 100, 70]
PRESENT = [255, 255, 255]

if hour >= DAY_START:
    top = (hour - DAY_START) * LEDS_PER_HOUR
    top += math.ceil((minute / 60) * LEDS_PER_HOUR)
    tail = (DAY_LEDS-top)

    print(f"LEDs: {top} x {tail}")
    payload = {
        "on": True,
        "bri": 100,
        "live": False,
        "seg": [
            {
                "start": 10,
                "len": DAY_LEDS,
                "col": [255,255,255],
                "i": [PAST]*top + [PRESENT] + [FUTURE]*tail
            },
        ]
    }

    # from pprint import pprint
    # pprint(payload)
    response = requests.post(WLED_JSON_API_URL, json=payload)
else:
    response = requests.post(WLED_JSON_API_URL, json={"on": False})
    print("Night mode")
