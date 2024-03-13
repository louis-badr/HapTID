# Participant info
id = None
wrist_threshold = None
dominant_hand = None
finger_threshold = None
index_calib_done_trials = 0

# Display
framerate = 60

# Arduino
com_port_haptid = None
com_port_keyboard = None
baud_rate = 115200

# Wrist calibration
wrist_max_vib_lvl = 30   # in %
wrist_nb_trials = 40
wrist_descending_starting_step = 5   # in %
wrist_ascending_starting_step = 0.25   # in %
wrist_coeff = 0.5

sr_coeff = 0.6

# index calibration
index_max_vib_lvl = 5   # in %
index_nb_trials = 40
index_descending_starting_step = 1   # in %
index_ascending_starting_step = 0.015   # in %
index_coeff = 0.5

# Tasks tracking
tasks = []
completed_crt_tasks = []
completed_fc_tasks = []

# Force control
target_circle_size = 80