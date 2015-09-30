import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

def get_randoms(mean_open_time, mean_close_time, interval):
    """ Generates open and close times randomly 
        Carli and Jiakun are gonna make this the greatst random number generator ever!
    """
    too_short = True
    samples = 10
    while too_short:
        # Repeats until we get enough samples
        opens = np.random.exponential(size=samples)
        closes = np.random.exponential(size=samples)
        time_covered = mean_open_time * sum(opens) + mean_close_time * sum(closes)
        if time_covered >= interval:
            too_short = False
        else:
            samples *= 2
    return opens, closes