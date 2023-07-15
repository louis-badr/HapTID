# HapTID first hardware prototype

This folder contains the first hardware prototype of the HapTID project.
The design objectives of this prototype are:
- to be able to produce sub-threshold vibrations on the wrist ranging from 0 to 500 Hz
- to be able to produce supra-threshold vibrations on each finger
- to be able to produce different signals simultaneously on all actuators
- has wired communication to reduce latency (this is an experimental prototype)

## Parts list
 
### 3D printed parts
Everything was printed with a Prusa i3 MK3S printer with PLA filament with 0.2 mm layer height and no supports.
- `wrist_motor.stl`: enclosure to hold the wrist motor
- `enclosure.stl`: enclosure for the electronic circuit board
### Electronics
- ESP32 WROOM DevKit (38 pins)

### Other parts