import config
import csv
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

# get the stim order from the csv file 
with open('./running_order.csv', mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        if row[0] == config.id:
            config.stim_order = row[1:]
            print(f'\nParticipant {config.id} will perform the assessments in the following order: {config.stim_order}')
            break

# generate the paremeters for the assessments
for i in range(3):
    for stim in config.stim_order:
        if stim == '80':
            config.stim_order_params.append(['80', config.index_max_vib_lvl, config.max_nb_trials, config.max_chg_points, config.index_vib_desc_start_step, config.index_staircase_coeff])
        elif stim == '250':
            config.stim_order_params.append(['250', config.index_max_vib_lvl, config.max_nb_trials, config.max_chg_points, config.index_vib_desc_start_step, config.index_staircase_coeff])
        elif stim == 'click':
            config.stim_order_params.append(['click', config.index_max_click_lvl, config.max_nb_trials, config.max_chg_points, config.index_click_desc_start_step, config.index_staircase_coeff])

# ask for participant dominant hand
config.dominant_hand = input('\nDominant hand (L/R): ')

config.current_assess = input(f'\nIf you want to skip assessments, type the number of the assessment you want to start from (2-10): ')
if config.current_assess == '':
    config.current_assess = 0
else:
    config.current_assess = int(config.current_assess)
if config.current_assess >= 1 and config.current_assess <= 10:
    config.current_assess = int(config.current_assess) - 1
    config.wrist_threshold = input(f'\nWrist threshold for participant {config.id}: ')
    config.wrist_threshold = float(config.wrist_threshold)

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
    app = threshold_assess.Threshold_assess(*config.stim_order_params[config.current_assess])
    app.run()