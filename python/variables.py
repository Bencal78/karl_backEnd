import os
PATH = str(os.path.dirname(os.path.realpath('__file__')))
DATABASE = '{}/database/'.format(PATH)

# VARIABLES REINFORCEMENT LEARNING
params = None  # body part and layer for each step to have a complete outfit
n_clothes_forced = None
n_step = 4
exploration_factor = 0.2



def set_weather_params(temperature):
    global n_clothes_forced
    global params

    if temperature > 24:
        n_clothes_forced = 2
        params = [(['bp_1'], 1), (['bp_5'], 1), (['bp_1'], 2), (['bp_1'], 3)]
    elif temperature > 16:
        n_clothes_forced = 2
        params = [(['bp_1'], 1), (['bp_5', 'bp_6', 'bp_7'], 1), (['bp_1'], 2), (['bp_1'], 3)]
    elif temperature > 10:
        n_clothes_forced = 3
        params = [(['bp_1'], 1), (['bp_5', 'bp_6', 'bp_7'], 1), (['bp_1'], 2), (['bp_1'], 3)]
    else:
        n_clothes_forced = 4
        params = [(['bp_1'], 1), (['bp_5', 'bp_6', 'bp_7'], 1), (['bp_1'], 2), (['bp_1'], 3)]
