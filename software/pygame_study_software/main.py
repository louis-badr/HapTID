import menu
import os
import pygame
import serial.tools.list_ports
import constants


print('\nHapTID experiment software - Haptic Technology for Improved Dexterity\n')

# list available serial ports
ports = serial.tools.list_ports.comports()
for port in sorted(ports):
        print(port)
constants.com_port_haptid = 'COM' + input('\nEnter the HapTID bord COM port n°: ')
constants.com_port_keyboard = 'COM' + input('\nEnter the keyboard COM port n°: ')

# ask for the participant's running order number
constants.id = input("\nEnter the participant's running order number: ")
# create folder for participant if it doesn't exist
if not os.path.exists(f'./P{constants.id}'):
    os.mkdir(f'./P{constants.id}')

# ask for participant dominant hand
constants.dominant_hand = input('\nDominant hand (L/R): ')

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((1280,720))

if __name__ == '__main__':
    app = menu.Menu()
    app.run()