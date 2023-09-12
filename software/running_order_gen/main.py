import csv
import itertools
import random

#* Generation parameters

# number of participants
nb_participants = 2
# number of trials per condition for the Choice Reaction Time (CRT) task
nb_trials_crt = 1
# number of trials per condition for the Force Control (FC) task
nb_trials_fc = 1

#* Task parameters

# CRT task parameters
crt_param = [
    # finger to press with
    ['thumb','index','middle','ring','little'],
    # warning signal type
    ['none', 'visual', 'tactile'],
    # imperative signal type
    ['visual', 'tactile'],
]

# FC task parameters
fc_param = [
    # force target (N)
    ['4','6','8'],
    # target indicator type
    ['visual', 'tactile'],
]

#* List all tasks

# CRT task
# create all possible combinations of CRT task parameters
crt_tasks = list(itertools.product(*crt_param))
# repeat the list of combinations to have enough trials
crt_tasks = crt_tasks * nb_trials_crt

# FC task
# create all possible combinations of FFC task parameters
fc_tasks = list(itertools.product(*fc_param))
# repeat the list of combinations to have enough trials
fc_tasks = fc_tasks * nb_trials_fc

#* Write the CSV file

task_nb = 1

with open(f'running_order_table.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # write the header
    writer.writerow(['Participant #', 'Task #', 'Task type', 'Wrist vibration', 'Param 1', 'Param 2', 'Param 3'])
    # for each participant
    for i in range(nb_participants):
        # randomize the order of the series of tasks
        series = random.sample(['CRT', 'FC'], 2)
        series *= 2
        # for each series
        for j in range(len(series)):
            # randomize the order of the corresponding tasks
            if series[j] == 'CRT':
                tasks = random.sample(crt_tasks, len(crt_tasks))
            if series[j] == 'FC':
                tasks = random.sample(fc_tasks, len(fc_tasks))
            # write the tasks in the CSV file
            if j <= 1:
                # wrist noise vibration off
                for k in range(len(tasks)):
                    writer.writerow([i+1, task_nb, series[j], 'off'] + list(tasks[k]))
                    task_nb += 1
            if j > 1:
                # wrist noise vibration on
                for k in range(len(tasks)):
                    writer.writerow([i+1, task_nb, series[j], 'on'] + list(tasks[k]))
                    task_nb += 1