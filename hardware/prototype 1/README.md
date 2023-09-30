# HapTID first hardware prototype

This folder contains the first hardware prototype of the HapTID project.
The design objectives of this prototype are:
- be able to produce sub-threshold vibrations on the wrist ranging from 0 to 500 Hz
- be able to produce supra-threshold vibrations on each finger
- be able to produce different signals simultaneously on all actuators
- has wired communication to reduce latency (this is an experimental prototype)

## Parts list
 
### 3D printed parts

The enclosures were printed with a Prusa i3 MK3S in PLA filament with 0.2 mm layer height and no supports.
- `wrist_motor_enclosure.3mf`: enclosure to hold the wrist motor
- `electronics_enclosure.3mf`: enclosure for the electronic circuit boards
The flexible rings can be casted in silicone with a 3D printed mold, here they were 3D printed with Formlabs Flexible 80A resin.
- `flex_ring.3mf`

### Electronics

- Custom Prototype 1 PCB
- ESP32 WROOM DevKit (38 pins)
- x6 2.5mm audio jack connectors
- x6 VLV101040A motors by Vybronics
- x1 HD-VA3222 motor by PUI Audio

### Other parts

- A velcro strap (38mm wide here)
- x4 M2x10mm screws to secure the PCB

## Assembly guide