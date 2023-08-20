import socket
import datetime
import time
import math
import sys

hour = int(sys.argv[1])
minute = int(sys.argv[2])


UDP_IP = "192.168.1.23"
UDP_PORT = 19446

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)


UTC_OFFSET = -5

DAY_START = 6
NUM_HOURS = 18
TOTAL_LEDS = 144
LEDS_PER_HOUR = 4

DAY_LED_OFFSET = 10
DAY_LEDS = NUM_HOURS * LEDS_PER_HOUR

OFF = [0,0,0]
PAST = [0,0,4]
FUTURE = [10,10,10]
MARKER = [30,30,70]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"{hour}:{minute}")

#now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=UTC_OFFSET)))
dot = (hour - DAY_START) * LEDS_PER_HOUR
dot += math.ceil((minute / 60) * LEDS_PER_HOUR)

print("Dot: %s" % dot)
print(f"{DAY_LED_OFFSET} {dot} {(DAY_LEDS-dot)} {TOTAL_LEDS-DAY_LED_OFFSET-DAY_LEDS}")

m = (OFF * DAY_LED_OFFSET) + (PAST * dot) + MARKER + (FUTURE * (DAY_LEDS-dot)) + (OFF * (TOTAL_LEDS-DAY_LED_OFFSET-DAY_LEDS))
print(m)

sock.sendto(bytes(m), (UDP_IP, UDP_PORT))


