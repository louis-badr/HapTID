# Participant info
id = None
dominant_hand = None
age = None
gender = None
wrist_threshold = -1
finger_vib_threshold = 50

# Task info
train_tasks = []
expe_tasks = []

# Display
framerate = 60

# Arduino
baud_rate = 115200
com_port_haptid = None
ser_haptid = None
com_port_keyboard = None
ser_keyboard = None

# CRT parameters
visual_signal_duration = 50
max_reaction_time = 3000

# PT assessment parameters
wrist_max_vib_lvl = 24
max_nb_trials = 35
max_chg_points = 7
wrist_staircase_coeff = 0.75
wrist_desc_start_step = wrist_max_vib_lvl / 4
min_step = 0.01

assess_params = [
    # stim_type, sr, max_vib_lvl, max_nb_trials, max_chg_points, desc_start_step, staircase_coeff
    ['noise', wrist_max_vib_lvl, max_nb_trials, max_chg_points, wrist_desc_start_step, wrist_staircase_coeff],
]