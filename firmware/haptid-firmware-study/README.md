# HapTID firmware

This is the Arduino sketch made to run for the study on healthy subjects (works with pygame_study_software).
The ESP32 listens to the serial port for an integer:
- 0 to stop the noise or tone
- between 1 and 100000 to control the wrist noise level (between 0.001 and 100.000%)
- between 100001 and 200000 to control the index 150Hz tone level for the left hand
- between 200001 and 300000 to control the index 150Hz tone level for the right hand
- between 300001 and 400000 to control the index 190Hz tone level for the left hand
- between 400001 and 500000 to control the index 190Hz tone level for the right hand
- between -1 and -7 to play a click, in order: on the wrist, a finger (left to right) or on all fingers at the same time

There is also a .wav file converter code modified from https://github.com/rgrosset/pico-pwm-audio by Robin Grosset.