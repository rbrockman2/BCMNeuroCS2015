# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:45:26 2015

@author: carlidomenico
"""
import numpy as np
import math
from pandas import DataFrame
from random import randint
debug = True
import matplotlib.pyplot as plot

#time = float(input('Give me a time'))
amp = 0.05 #check consistency


def add_noise(channel_data, amp):
    """ATTN: there is unit testing stuff in here you will need to get rid of for actual inputs"""
    """ Adds noise to the on and off states to make it more biological-looking """
    noise = np.random.normal(size=len(channel_data)) #takes the output from record_channel and makes a tuple of random numbers using Numpy
    scaled_noise = noise * amp #takes your randoms from the last line and scales them down to 5% of what they were
    chan_dat_np = np.array(channel_data)+scaled_noise #creates an array from our channel_data list input and adds our scaled noise to it
    return chan_dat_np #returns the output of the line above as the function's output


def make_pretty_plot(current, time, dt = 10^-5):
    # Gabe and Carli take on the world of magic and marvel, a world of plot perfection
     
    x_axis = []    
    i = 0    
    while i < time: # create x_axis list in correct time steps
        x_axis += [i] 
        i += dt
        
    nano_current = []
    for item in current: 
        item = item*(10**9) # convert to nanoamps for graph prettiness
        nano_current += item
    y_axis = nano_current
    
    plot.plot(x_axis, y_axis, label='time', marker='o', color='maroon', linestyle = '-')
    plot.xlabel('Time (msec)')
    plot.ylabel('Net current (nA)')
    plot.title('Title Title Title')
    plot.grid()
    plot.show()
    #plot.savefig('program_output.pdf')

channel_data = [1,2,3,4,5,6,7,8]
noise_currents = add_noise(channel_data, amp)
x = make_pretty_plot(noise_currents, time, dt)

