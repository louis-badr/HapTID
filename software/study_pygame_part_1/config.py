# Participant info
id = None
dominant_hand = None    # "L" or "R"
wrist_threshold = None

# Display
framerate = 60

# Arduino
com_port_haptid = None
com_port_keyboard = None
baud_rate = 115200

# Stochastic resonance
sr_coeff = 0.6  # factor to be applied to the threshold value to get the white noise level

stim_order = None

current_assess = 0

wrist_max_vib_lvl = 25   # starting value in %
index_max_vib_lvl = 5   # starting value in %
index_max_click_lvl = 100
max_nb_trials = 40    # max number of trials
max_chg_points = 10
wrist_staircase_coeff = 0.6
index_staircase_coeff = 0.6
wrist_desc_start_step = wrist_max_vib_lvl / 5   # starting descending step in %
index_desc_start_step = index_max_vib_lvl / 5

stim_order_params = [
    # stim_type, sr, max_vib_lvl, max_nb_trials, max_chg_points, desc_start_step, staircase_coeff
    ['noise', 'off', wrist_max_vib_lvl, max_nb_trials, max_chg_points, wrist_desc_start_step, wrist_staircase_coeff],
]
