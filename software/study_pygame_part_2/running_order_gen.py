import csv
import numpy
import random
import itertools

nb_participants = 20
nb_repetitions = 5
final_array = []

# Participant #; Exercise type; Task #; Noise PT coeff; Finger to press; Warning signal type; Imperative signal type

ws_type = ['visual', 'tactile-click', 'none']
is_type = ['visual', 'tactile-click', 'tactile-vibration']
finger = ['thumb', 'index', 'middle', 'ring', 'little']

# all possible combinations of the signal types
signal_combinations = list(itertools.product(ws_type, is_type))

for i in range(nb_participants):
    # shuffle the signal combinations
    random.shuffle(signal_combinations)
    tasks = []
    for comb in signal_combinations:
        series = []
        for j in range(5):
            for k in range(nb_repetitions):
                series.append([comb[0], comb[1], finger[j]])
        random.shuffle(series)
        tasks.extend(series)
    c = 1
    for task in tasks:
        final_array.append([i+1, 'CRT', c, 0, task[2], task[0], task[1]])
        c += 1
    for task in tasks:
        final_array.append([i+1, 'CRT', c, 0.8, task[2], task[0], task[1]])
        c += 1
    for task in tasks:
        final_array.append([i+1, 'CRT', c, 0, task[2], task[0], task[1]])
        c += 1

with open(f'running_order.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # write the tasks in the CSV file with a break line every 25 tasks
    for i in range(len(final_array)):
        writer.writerow(final_array[i])
        if final_array[i][2] % 25 == 0 and i+1 != len(final_array):
            writer.writerow(['break']*7)