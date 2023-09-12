import csv
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

# create an array of the tasks to be performed from the CSV
with open('./running_order_table.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    rows = list(csv_reader)
    # add the task to the list if the participant number is correct
    for row in rows:
        if row[0] == constants.id:
            constants.tasks.append(row[1:])

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((1280,720))

if __name__ == '__main__':
    app = menu.Menu()
    app.run()