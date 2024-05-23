# HapTID firmware

This is the Arduino sketch made to run for the study on healthy subjects (works with pygame_study_software).
The ESP32 listens to the serial port for a value:

- 0 to stop all vibrations

- between 1 and 100000 to control the noise level on output 1 (from 0.001% to 100%)

- between 100001 and 200000 to control the 80Hz tone level on ouput 3
- between 200001 and 300000 to control the 80Hz tone level on output 5
- between 300001 and 400000 to control the 250Hz tone level on output 3
- between 400001 and 500000 to control the 250Hz tone level on output 5

- between -1 and -100000 to control the click level on output 1
- between -100001 and -199999 to control the click level on output 2
- between -200001 and -299999 to control the click level on output 3
- between -300001 and -399999 to control the click level on output 4
- between -400001 and -499999 to control the click level on output 5
- between -500001 and -599999 to control the click level on output 6
- between -600001 and -699999 to control the click level for a click on all outputs at the same time

- between -700001 and -799999 to play a sine click on output 1
- between -800001 and -899999 to play a sine click on output 2
- between -900001 and -999999 to play a sine click on output 3
- between -1000001 and -1099999 to play a sine click on output 4
- between -1100001 and -1199999 to play a sine click on output 5
- between -1200001 and -1299999 to play a sine click on output 6


There is also a .wav file converter modified from https://github.com/rgrosset/pico-pwm-audio by Robin Grosset.