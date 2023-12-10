# HapTID firmware

This is the Arduino sketch made to run for the study on healthy subjects (works with pygame_study_software).
The ESP32 listens to the serial port for an integer:
- 0 to stop the noise or tone
- between 1 and 100 to control the wrist noise level
- between 101 and 200 to control the index 150Hz tone level
- between 201 and 300 to control the index 190Hz tone level
- between 301 and 306 for clicks, wrist then left to right fingers

There is also a .wav file converter code modified from https://github.com/rgrosset/pico-pwm-audio by Robin Grosset.