import os
import warnings
import functools
import numpy as np
PATH = str(os.path.dirname(os.path.realpath('__file__')))
DATABASE = '{}/database/'.format(PATH)

# VARIABLES REINFORCEMENT LEARNING
params = None  # body part and layer for each step to have a complete outfit
n_clothes_forced = None
n_step = 4
exploration_factor = 0.33


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func


def set_weather_params(conditions):
    global n_clothes_forced
    global params

    if not conditions:
        n_clothes_forced = np.random.randint(2, 5)
        params = [(['bp_1'], 1), (['bp_5', 'bp_6', 'bp_7'], 1), (['bp_1'], 2), (['bp_1'], 3)]
    else:
        temperature = conditions["temperature"]
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
            n_clothes_forced = 3
            params = [(['bp_1'], 1), (['bp_5', 'bp_6', 'bp_7'], 1), (['bp_1'], 2), (['bp_1'], 3)]
