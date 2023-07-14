import menu
import os
import pygame
import serial.tools.list_ports
import constants

print('\nHapTID - Haptic Technology for Improved Dexterity\n')
# list available serial ports
ports = serial.tools.list_ports.comports()
for port in sorted(ports):
        print(port)
constants.com_port = 'COM' + input('\nEnter COM port n°: ')

# ask for participant ID in the format : order + first letters of last and first name
constants.id = input('\nEnter participant ID (ex:01BL): ')
# create folder for participant if it doesn't exist
if not os.path.exists(f'./{constants.id}'):
    os.mkdir(f'./{constants.id}')

# ask for participant dominant hand
constants.dominant_hand = input('\nDominant hand (L/R): ')

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((1280,720))

if __name__ == '__main__':
    app = menu.Menu()
    app.run()