# Participant info
id = None
dominant_hand = None
age = None
gender = None
wrist_threshold = -1
finger_vib_threshold = 50
finger_click_threshold = 80

# Task info
train_tasks = []
expe_tasks = []
state = 'calib-wrist'   # next thing to do, either 'calib-wrist', 'calib-finger-click', 'calib-finger-vib', 'training', 'experiment' or None

# Calibration
wrist_max_vib_lvl = 24   # starting value in %
index_max_vib_lvl = 8
index_max_click_lvl = 12
max_nb_trials = 35    # max number of trials
max_chg_points = 7
wrist_staircase_coeff = 0.75
finger_staircase_coeff = 0.5
wrist_desc_start_step = wrist_max_vib_lvl / 4   # starting descending step in %
index_vib_desc_start_step = index_max_vib_lvl / 4
index_click_desc_start_step = index_max_click_lvl / 4
min_step = 0.01

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