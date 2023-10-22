import time, board, neopixel, random
from ulab import numpy as np

num_leds = 50
led_pin = board.D3

gamma = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
    2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5,
    5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10,
    10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
    17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
    25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
    37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
    51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
    69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
    90, 92, 93, 95, 96, 98, 99, 101, 102, 104, 105, 107, 109, 110,
    112, 114, 115, 117, 119, 120, 122, 124, 126, 127, 129, 131, 133,
    135, 137, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158,
    160, 162, 164, 167, 169, 171, 173, 175, 177, 180, 182, 184, 186,
    189, 191, 193, 196, 198, 200, 203, 205, 208, 210, 213, 215, 218,
    220, 223, 225, 228, 231, 233, 236, 239, 241, 244, 247, 249, 252,
    255
]

fire_colors = (
    (  0,  0,  0),
    ( 18,  0,  0),
    ( 18,  0,  0),
    (113,  0,  0),
    (113,  0,  0),
    (142,  3,  1),
    (175, 17,  1),
    (213, 44,  2),
    (255, 82,  4),
    (255,115,  4),
    (255,156,  4),
    (255,203,  4),
    (255,255,  4),
    (255,255, 71),
    (255,255,255),
    (255,255,255)
)
def fire(temp):
    index = int(temp * 1024)
    if temp < 255:
        r = gamma[temp]
        g = b = 0
    elif temp < 40:
        r = 255
        g = gamma[temp - 255]
        b = 0
    elif temp < 76:
        r = g = 255
        b = gamma[temp - 510]
    else:
        r = g = b = 255
        g = b = 200
    return (r, g, b)

    # index = int(temp * 16)
    # index = max(0, min(14, index))
    # return fire_colors[index]
    
temps = [0.0] * num_leds
leds = neopixel.NeoPixel(led_pin, num_leds, brightness=.5, auto_write=False)

last_time = time.monotonic()
while True:
    now = time.monotonic()
    delta = now - last_time
    last_time = now

    for i in range(0, num_leds):
        j = i - 1 % num_leds
        spread = temps[j] * 50.0 * delta
        temps[j] = temps[j] - spread
        temps[i] = temps[i] + spread

        cooldown = 0.3 * delta * random.random()
        temps[i] = max(0, temps[i] - cooldown)

        if i <= 5 and random.random() < (2 * delta):
            temps[i] = min(1.0, temps[i] + 1.0)

        leds[i] = fire(temps[i])
        if i < 5:
            leds[i] = fire(0.3 + (random.random() * .1))
    leds.show()
