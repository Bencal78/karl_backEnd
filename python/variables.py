import os
PATH = str(os.path.dirname(os.path.realpath('__file__')))
DATABASE = '{}/database/'.format(PATH)

# VARIABLES REINFORCEMENT LEARNING
params = [("bp_1", 1), ("bp_5", 1), ("bp_1", 2), ("bp_1", 3)]  # body part and layer for each step to have a complete outfit
n_step = 4