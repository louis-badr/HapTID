import config
import csv
import menu
import os
import pygame
import serial.tools.list_ports


print('\nHapTID experiment software - Haptic Technology for Improved Dexterity\n')

# list available serial ports
ports = serial.tools.list_ports.comports()
for port in sorted(ports):
        print(port)
config.com_port_haptid = 'COM' + input('\nEnter the HapTID device COM port n°: ')
config.com_port_keyboard = 'COM' + input('\nEnter the keyboard COM port n°: ')

# ask for the participant's running order number
config.id = input("\nEnter the participant's running order number: ")
# create folder for participant if it doesn't exist
if not os.path.exists(f'./P{config.id}'):
    os.mkdir(f'./P{config.id}')
    # # create a wrist calibration jsonl file for the participant
    # with open(f'./P{config.id}/P{config.id}-wrist-calib.jsonl', 'w') as file:
    #     file.write('')
    # # create an index calibration jsonl file for the participant
    # with open(f'./P{config.id}/P{config.id}-index-calib.jsonl', 'w') as file:
    #     file.write('')
# type the threshold for the participant
config.wrist_threshold = input(f'\nWrist threshold for participant {config.id}: ')
if config.wrist_threshold == '':
    config.wrist_threshold = None
else:
    config.wrist_threshold = float(config.wrist_threshold)
# type the finger threshold for the participant
config.finger_threshold = input(f'\nFinger threshold for participant {config.id}: ')
if config.finger_threshold == '':
    config.finger_threshold = None
else:
    config.finger_threshold = float(config.finger_threshold)

# ask for participant dominant hand
config.dominant_hand = input('\nDominant hand (L/R): ')

# create an array of the tasks to be performed from the CSV
with open('./running_order_table.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    rows = list(csv_reader)
    # add the task to the list if the participant number is correct
    for row in rows:
        if row[0] == config.id:
            config.tasks.append(row[1:])
            print(f'\nTask added: {row[1:]}')
    # print the number of tasks left
    print(f'\n{len(config.tasks)} tasks left to perform')

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((1280,720))

if __name__ == '__main__':
    app = menu.Menu()
    app.run()