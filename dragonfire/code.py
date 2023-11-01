# pyright: reportShadowedImports=false, reportMissingImports=false
import time, board, neopixel, random

num_leds_dragon_belly = 5
num_leds_dragon_fire = 50
num_leds_bonfire = 25
num_leds = 100
num_leds_cauldron = 25

FIRST_LED_BONFIRE = num_leds_dragon_fire
FIRST_LED_CAULDRON = FIRST_LED_BONFIRE + num_leds_bonfire

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

def clamp(x, mn, mx):
    return max(mn, min(mx, x))

def fire(temp):
    temp = int(temp * 1024)

    r_max = 250
    g_max = 120
    b_max = 120

    return (
        gamma[min(r_max, max(0, temp))],
        gamma[min(g_max, max(0, temp - r_max))],
        gamma[min(b_max, max(0, temp - r_max - g_max))]
    )

    return (r, g, b)

temps = [0.0] * num_leds
leds = neopixel.NeoPixel(led_pin, num_leds, brightness=.9, auto_write=False)
# leds.fill(fire(0.3))
# leds.show()
# time.sleep(3.0)

# while True:
#     for i in range(100):
#         temp = float(i)/100
#         leds.fill(fire(temp))
#         leds.show()
#         time.sleep(0.1)

# for i in range(num_leds):
#     temp = float(i)/num_leds
#     leds[i] = fire(temp)
# leds.show()

BELLY_MIN_TEMP = 0.1
BELLY_MAX_TEMP = 0.9
DRAGON_FLAME_MIN_TEMP = 0.3
BONFIRE_MIN_TEMP = 0.3

INVERSE_FRAME_RATE = .0333
SPARK_TEMP = 0.3
SPARK_RATE = 1.5
SPREAD_RATE = 15.0
COOLDOWN_RATE = .003

last_time = time.monotonic()
while True:
    now = time.monotonic()
    delta = now - last_time

    if delta > INVERSE_FRAME_RATE:
        last_time = now

        for i in range(1, num_leds_dragon_belly):
            if random.random() < (SPARK_RATE * delta):
                temps[i] += SPARK_TEMP
            temps[i] = clamp(temps[i], BELLY_MIN_TEMP, BELLY_MAX_TEMP)

        for i in range(1, num_leds):
            j = i - 1 % num_leds

            spread   = temps[j] * SPREAD_RATE * delta
            cooldown = temps[i] * COOLDOWN_RATE * delta
            temps[j] = temps[j] - spread
            temps[i] = temps[i] + spread - cooldown

            if i >= FIRST_LED_BONFIRE:
                temps[i] = max(temps[i], BONFIRE_MIN_TEMP)

            leds[i] = fire(temps[i])

            if i >= FIRST_LED_CAULDRON:
                leds[i] = fire(0.2 + (random.random() * .2))
                leds[i] = (leds[i][2], leds[i][0], leds[i][1])

        leds.show()
