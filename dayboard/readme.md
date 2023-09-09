# Dayboard

This project is a visual clock designed to help with my specific form of time blindness. It's just a whiteboard with a line of lights which represent the current time. 

My day is a line:

```
       8am: start work
    ...
    ...
      noon: eat stuff
    ...
    2:30pm: be late for a meeting
    3:00pm: run over on my last meeting
    ...
       6pm: stop work
    ...
    ...
       8pm: remember to make dinner
```

Not a circle:

```
          _______
         /  12   \
        |    |    |
        |9   |   3|
        |     \   |
        |         |
         \___6___/

```

It helps to see time passing linearly. It also helps to be able to write stuff on it.

## Hardware
The concept is based around sticking a strip of [Neopixels](https://www.adafruit.com/product/1506) to a whiteboard and connecting that to an ESP32 running [WLED](https://kno.wled.ge).

The logic is currently contained in a Python script that runs on an external server or on my laptop. This allows me to noodle with it a bit more easily without having to reflash the microcontroller over and over. It also allows me to not deal with timezone issues or real-time clock issues on a microcontroller.

Ultimately the code could be ported CircuitPython/MicroPython or to an Arduino sketch for simpler more permanent installations.

## TODO

- [x] Add hourly temperature forcast using colors
- [ ] Run the logic on the esp directly