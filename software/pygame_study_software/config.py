# Participant info
id = None
wrist_threshold = None
dominant_hand = None    # "L" or "R"
index_trials_thresholds = [None] * 3
finger_threshold = None # mean of the 3 index thresholds in %
index_calib_done_trials = 0

# Display
framerate = 60

# Arduino
com_port_haptid = None
com_port_keyboard = None
baud_rate = 115200

# Wrist calibration
wrist_max_vib_lvl = 30   # starting value in %
wrist_nb_trials = 40    # number of trials
wrist_descending_starting_step = 5   # starting descending step in %
wrist_ascending_starting_step = 0.25  # starting ascending step in %
wrist_coeff = 0.5   # coefficient applied to the step after a change in answer

# Index calibration
index_max_vib_lvl = 5   # starting value in %
index_nb_trials = 40    # number of trials
index_descending_starting_step = 1  # starting descending step in %
index_ascending_starting_step = 0.015   # starting ascending step in %
index_coeff = 0.5   # coefficient applied to the step after a change in answer

# Stochastic resonance
sr_coeff = 0.6  # factor to be applied to the threshold value to get the white noise level

# Tasks tracking
tasks = []
completed_crt_tasks = []
completed_fc_tasks = []

# Force control
target_circle_size = 80