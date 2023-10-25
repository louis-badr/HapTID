# HapTID - Haptic Technology for Improved Dexterity

HapTID is a study on how vibrotactile stimulations can improve manual dexterity in healthy subjects. In this repository you will find:

- Hardware :
    - The parts list and assembly guide of the device
    - CAD files for the 3D printed parts
    - Electronic schematics and PCB design files

- Software :
    - A GUI to test motors via I2S
    - A GUI for the study on healthy subjects
    - A script to generate the running order of the tasks and parameters for the study
    - A script to convert WAV files to C arrays compatible with the HapTID firmware

- Firmware :
    - An Arduino sketch for the GUI to test motors via I2S
    - An Arduino sketch for the study on healthy subjects
    - Arduino sketches to test motor vibrations using an accelerometer