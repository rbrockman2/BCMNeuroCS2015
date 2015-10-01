"""Worked on by Gabe S. and Elizabeth L."""

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

def add_noise(channel_data, amp):
    """ Adds noise to the on and off states to make it more biological-looking """
    noise = np.random.normal(size=len(channel_data)) #takes the output from record_channel and makes a tuple of random numbers using Numpy
    scaled_noise = noise * amp #takes your randoms from the last line and scales them down to 5% of what they were
    chan_dat_np = np.array(channel_data)+scaled_noise #creates an array from our channel_data list input and adds our scaled noise to it
    return chan_dat_np #returns the output of the line above as the function's output