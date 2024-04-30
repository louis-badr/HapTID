import csv
import random
import itertools

nb_participants = 25
stim  = ['80', '250', 'click']   # assessments to be performed - 80Hz, 250Hz and click stimuli
final_array = []

# make all the possible combinations of the stimuli
combinations = list(itertools.permutations(stim, 3))
# repeat the combinations for the number of participants
final_array = combinations * (nb_participants // len(combinations) + 1)
# remove the last 5 combinations
final_array = final_array[:-5]
# shuffle the array
random.shuffle(final_array)
# add the participant number to the array
for i in range(len(final_array)):
    final_array[i] = [i+1] + list(final_array[i])

with open(f'running_order.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    # write the header
    writer.writerow(['Participant #', 'Stim #1', 'Stim #2', 'Stim #3'])
    # write the tasks in the CSV file
    for task in final_array:
        writer.writerow(task)