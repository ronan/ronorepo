# watch 'date "+%H %M" --date="5 hours ago" | xargs python udp.py'

import socket
import math
import sys

hour = int(sys.argv[1])
minute = int(sys.argv[2])

UDP_IP = socket.gethostbyname("dayboard.local")
UDP_PORT = 19446

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)

DAY_START = 6
NUM_HOURS = 18
TOTAL_LEDS = 108
LEDS_PER_HOUR = 6

DAY_LED_OFFSET = 0
DAY_LEDS = NUM_HOURS * LEDS_PER_HOUR

OFF = [0,0,0]
PAST = [0, 0, 0]
FUTURE = [60, 60, 30]
PRESENT = [0, 255, 0]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"{hour}:{minute}")

dot = (hour - DAY_START) * LEDS_PER_HOUR
dot += math.ceil((minute / 60) * LEDS_PER_HOUR)

print(f"{DAY_LED_OFFSET} {dot} x {(DAY_LEDS-dot)} {TOTAL_LEDS-DAY_LED_OFFSET-DAY_LEDS}")

m = (OFF * DAY_LED_OFFSET) + (PAST * dot) + PRESENT + (FUTURE * (DAY_LEDS-dot)) + (OFF * (TOTAL_LEDS-DAY_LED_OFFSET-DAY_LEDS))

if hour < 6:
    print("Night mode")
    m = OFF * TOTAL_LEDS

sock.sendto(bytes(m), (UDP_IP, UDP_PORT))
