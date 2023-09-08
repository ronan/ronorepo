# watch 'date "+%H %M" --date="5 hours ago" | xargs python dayboard.py'

import socket
import math
import sys

hour = int(sys.argv[1])
minute = int(sys.argv[2])

print(f"{hour}:{minute}")

UDP_IP = socket.gethostbyname("dayboard.local")
UDP_PORT = 19446

DAY_START = 6                           # 6am
NUM_HOURS = 18                          # 6am-midnight

LEDS_PER_HOUR = 6                       # ~30" of 144/m led strip
DAY_LEDS = NUM_HOURS * LEDS_PER_HOUR    # 108

OFF = [0,0,0]
PAST = [0, 0, 0]
FUTURE = [60, 60, 30]
PRESENT = [0, 255, 0]

if hour > DAY_START:
    dot = (hour - DAY_START) * LEDS_PER_HOUR
    dot += math.ceil((minute / 60) * LEDS_PER_HOUR)

    print(f"{dot} x {(DAY_LEDS-dot)}")
    m = (PAST * dot) + PRESENT + (FUTURE * (DAY_LEDS-dot))
else:
    m = OFF * (DAY_LEDS + 1)
    print("Night mode")

print(f'UDP target: {UDP_IP}:{UDP_PORT}')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(m), (UDP_IP, UDP_PORT))
