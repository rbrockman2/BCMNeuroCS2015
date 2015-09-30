import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

def add_noise(channel_data, amp):
    """ Adds noise to the on and off states to make it more biological-looking """
    noise = np.random.normal(size=len(channel_data))
    scaled_noise = noise * amp
    chan_dat_np = np.array(channel_data)+scaled_noise
    return chan_dat_np