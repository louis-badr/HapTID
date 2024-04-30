import config
import csv
import menu
import os
import pygame
import serial.tools.list_ports
import threshold_assess


print('\nHapTID experiment software - Haptic Technology for Improved Dexterity\n')

# ask for the participant's running order number
config.id = input("\nEnter the participant's running order number: ")
# create folder for participant if it doesn't exist
if not os.path.exists(f'./participants_data/P{config.id}'):
    os.mkdir(f'./participants_data/P{config.id}')

# ask for participant dominant hand
config.dominant_hand = input('\nDominant hand (L/R): ')
# ask for participant age	
config.age = input('\nAge: ')
# ask for participant gender
config.gender = input('\nGender (M/F/O): ')

# list available serial ports
ports = serial.tools.list_ports.comports()
for port in sorted(ports):
        print(port)
config.com_port_haptid = 'COM' + input('\nEnter the HapTID device COM port n°: ')
# arduino things
config.ser_haptid = serial.Serial(config.com_port_haptid, 115200, timeout=.1)
# dirty fix to make sure the arduino is ready to receive data
config.ser_haptid.close()
config.ser_haptid.open() 

# initialize pygame
pygame.init()

#screen = pygame.display.set_mode((1280,720))
# fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

if __name__ == '__main__':
    app = menu.Menu()
    app.run()