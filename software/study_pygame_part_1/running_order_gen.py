import csv
import random

nb_participants = 30
stim  = ['80', '250', 'click']   # assessments to be performed - 80Hz, 250Hz and click stimuli
final_array = []

for i in range(nb_participants):
    # normal randomization
    stim_order = random.sample(stim, len(stim))
    final_array.append([i+1, stim_order[0], stim_order[1], stim_order[2]])

with open(f'running_order.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # write the header
    writer.writerow(['Participant #', 'Stim #1', 'Stim #2', 'Stim #3'])
    # write the tasks in the CSV file
    for task in final_array:
        writer.writerow(task)