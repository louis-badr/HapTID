import csv
import itertools
import numpy as np
import random

nb_participants = 3
nb_repetitions_crt = 5
final_array = []

def print_clearly(list):
    for elem in list:
        # print with tabs between elements
        print(*elem, sep='\t')

#* CRT task parameters for each sub-unit
crt_sub_units_params = [
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['none'],
        # imperative signal type
        ['visual'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['none'],
        # imperative signal type
        ['tactile-click'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['none'],
        # imperative signal type
        ['tactile-vibration'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['visual'],
        # imperative signal type
        ['visual'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['visual'],
        # imperative signal type
        ['tactile-click'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['visual'],
        # imperative signal type
        ['tactile-vibration'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['tactile-click'],
        # imperative signal type
        ['visual'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['tactile-click'],
        # imperative signal type
        ['tactile-click'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # finger to press with
        ['thumb','index','middle','ring','little'],
        # warning signal type
        ['tactile-click'],
        # imperative signal type
        ['tactile-vibration'],
    ],
]

#* Combine all sub-units parameters to create all possible CRT tasks
crt_sub_units = []  # list of all possible CRT tasks by sub-unit
for sub_unit_params in crt_sub_units_params:
    crt_sub_unit = list(itertools.product(*sub_unit_params))
    # repeat the list of combinations to have enough trials
    crt_sub_unit = crt_sub_unit * nb_repetitions_crt
    crt_sub_units.append(crt_sub_unit)

#* FC task parameters for each sub-unit
fc_sub_units_params = [
    [
        # stochastic vibrations
        ['off'],
        # force target (N)
        ['4','6','8'],
        # target indicator type
        ['visual'],
    ],
    [
        # stochastic vibrations
        ['off'],
        # force target (N)
        ['4','6','8'],
        # target indicator type
        ['tactile'],
    ],
]

#* Combine all sub-units parameters to create all possible FC tasks
fc_sub_units = []  # list of all possible FC tasks by sub-unit
for sub_unit_params in fc_sub_units_params:
    fc_sub_unit = list(itertools.product(*sub_unit_params))
    # repeat the list of combinations to have enough trials
    fc_sub_unit = fc_sub_unit * nb_repetitions_crt
    fc_sub_units.append(fc_sub_unit)

def generate_crt_tasks(no_participants):
    #* Unit 1
    crt_unit_1 = crt_sub_units
    # shuffle each sub-unit
    for sub_unit in crt_unit_1:
        random.shuffle(sub_unit)
    # shuffle the order of sub-units
    random.shuffle(crt_unit_1)
    # concatenate the sub-units
    crt_unit_1 = list(itertools.chain(*crt_unit_1))
    # convert tuples to lists
    crt_unit_1 = [list(elem) for elem in crt_unit_1]

    #* Unit 2
    crt_unit_2 = crt_sub_units
    # shuffle each sub-unit
    for sub_unit in crt_unit_2:
        random.shuffle(sub_unit)
    # shuffle the order of sub-units
    random.shuffle(crt_unit_2)
    # concatenate the sub-units
    crt_unit_2 = list(itertools.chain(*crt_unit_2))
    # convert tuples to lists
    crt_unit_2 = [list(elem) for elem in crt_unit_2]
    # replace 'off' by 'on' for stochastic vibrations
    for task in crt_unit_2:
        task[0] = 'on'

    #* Unit 3
    crt_unit_3 = crt_sub_units
    # shuffle each sub-unit
    for sub_unit in crt_unit_3:
        random.shuffle(sub_unit)
    # shuffle the order of sub-units
    random.shuffle(crt_unit_3)
    # concatenate the sub-units
    crt_unit_3 = list(itertools.chain(*crt_unit_3))
    # convert tuples to lists
    crt_unit_3 = [list(elem) for elem in crt_unit_3]

    #* Assemble
    crt_tasks = crt_unit_1 + crt_unit_2 + crt_unit_3
    # add the task number, type and participant number
    for i, task in enumerate(crt_tasks):
        task.insert(0, i+1)
        task.insert(0, 'CRT')
        task.insert(0, no_participants)
    # add a break every 25 trials without using numpy
    for i in range(25, len(crt_tasks), 26):
        crt_tasks.insert(i, ['break']*len(crt_tasks[0]))
    return crt_tasks

def generate_fc_tasks(no_participants):
    #* Unit 1
    fc_unit_1 = fc_sub_units
    # shuffle each sub-unit
    for sub_unit in fc_unit_1:
        random.shuffle(sub_unit)
    # shuffle the order of sub-units
    random.shuffle(fc_unit_1)
    # concatenate the sub-units
    fc_unit_1 = list(itertools.chain(*fc_unit_1))
    # convert tuples to lists
    fc_unit_1 = [list(elem) for elem in fc_unit_1]
    #* Unit 2
    fc_unit_2 = fc_sub_units
    # shuffle each sub-unit
    for sub_unit in fc_unit_2:
        random.shuffle(sub_unit)
    # shuffle the order of sub-units
    random.shuffle(fc_unit_2)
    # concatenate the sub-units         
    fc_unit_2 = list(itertools.chain(*fc_unit_2))
    # convert tuples to lists
    fc_unit_2 = [list(elem) for elem in fc_unit_2]
    # replace 'off' by 'on' for stochastic vibrations
    for task in fc_unit_2:
        task[0] = 'on'
    #* Unit 3
    fc_unit_3 = fc_sub_units
    # shuffle each sub-unit
    for sub_unit in fc_unit_3:
        random.shuffle(sub_unit)
    # shuffle the order of sub-units
    random.shuffle(fc_unit_3)
    # concatenate the sub-units
    fc_unit_3 = list(itertools.chain(*fc_unit_3))
    # convert tuples to lists
    fc_unit_3 = [list(elem) for elem in fc_unit_3]
    #* Assemble
    fc_tasks = fc_unit_1 + fc_unit_2 + fc_unit_3
    # add the task number, type and participant number
    for i, task in enumerate(fc_tasks):
        task.insert(0, i+1)
        task.insert(0, 'FC')
        task.insert(0, no_participants)
    # add a break every trial without using numpy
    for i in range(1, len(fc_tasks)*2, 2):
        fc_tasks.insert(i, ['break']*len(fc_tasks[0]))
    return fc_tasks


for paricipant in range(nb_participants):
    # generate a random number, 0 or 1
    rand = random.randint(0,1)
    if rand == 0:
        final_array += generate_crt_tasks(paricipant+1)
        final_array += generate_fc_tasks(paricipant+1)
    else:
        final_array += generate_fc_tasks(paricipant+1)
        final_array += generate_crt_tasks(paricipant+1)

#* Print
print_clearly(final_array)

#* Write to csv

with open(f'running_order_table.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # write the header
    writer.writerow(['Participant #', 'Exercise', 'Task #', 'Wrist vibration', 'Param 1', 'Param 2', 'Param 3'])
    # write the tasks in the CSV file
    for task in final_array:
        writer.writerow(task)