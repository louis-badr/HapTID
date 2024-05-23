import config
import csv
import menu
import os
import pygame
import serial.tools.list_ports


print('\nHapTID experiment software - Haptic Technology for Improved Dexterity\n')

# ask for the participant's running order number
config.id = input("\nEnter the participant's running order number: ")

# convert the training csv file into an array
with open('./running_order_crt_train.csv', mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        config.train_tasks.append(row)

# convert the real experiment csv file into an array and keep only the tasks for the participant's running order
with open('./running_order.csv', mode='r') as file:
    reader = csv.reader(file, delimiter=';')
    # keep everything between the first appearance of the participant's running order number and the last one
    found = False
    for row in reader:
        if row[0] == config.id:
            found = True
        if row[0] == str(int(config.id) + 1):
            found = False
        if found:
            config.expe_tasks.append(row)
# remove the last break
config.expe_tasks.pop()

# create folder for participant if it doesn't exist
if not os.path.exists(f'./participants_data/P{config.id}'):
    os.mkdir(f'./participants_data/P{config.id}')

# ask for participant dominant hand
config.dominant_hand = input('\nDominant hand (L/R): ')

# ask for participant age	
config.age = input('\nAge: ')

# ask for participant gender
config.gender = input('\nGender (M/F/O): ')

config.task_skip = input(f'\nIf you want to start from a specific task, enter the task number, otherwise press Enter: ')
if config.task_skip != '' and config.task_skip != '0':
    config.task_skip = int(config.task_skip)
    # remove all tasks with a task number lower than the one entered
    config.expe_tasks = [task for task in config.expe_tasks if task[0] == 'break' or int(task[2]) >= config.task_skip]
    # remove all breaks at the beginning
    while config.expe_tasks[0][0] == 'break':
        config.expe_tasks.pop(0)

# list available serial ports
ports = serial.tools.list_ports.comports()
for port in sorted(ports):
    print(port)
config.com_port_haptid = 'COM' + input('\nEnter the HapTID device COM port n°: ')
config.com_port_keyboard = 'COM' + input('Enter the keyboard COM port n°: ')
# arduino things
config.ser_haptid = serial.Serial(config.com_port_haptid, config.baud_rate, timeout=.1)
config.ser_keyboard = serial.Serial(config.com_port_keyboard, config.baud_rate, timeout=.1)
# dirty fix to make sure the arduino is ready to receive data
config.ser_haptid.close()
config.ser_haptid.open()
config.ser_keyboard.close()
config.ser_keyboard.open()
config.ser_haptid.write('0'.encode()) 

# initialize pygame
pygame.init()

#screen = pygame.display.set_mode((1280,720))
# fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

if __name__ == '__main__':
    menu.Menu().run()