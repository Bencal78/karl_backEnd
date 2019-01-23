import os
PATH = str(os.path.dirname(os.path.realpath('__file__')))
DATABASE = '{}/database/'.format(PATH)

# VARIABLES REINFORCEMENT LEARNING
params = [(1, 1), (1, 1), (1, 2), (1, 3)]  # body part and layer for each step to have a complete outfit
n_step = 4