# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 11:45:48 2015

@author: ppfaff
"""

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

def input_times(debug=False, open = 0.0, close = 0.0, time_len = 0.0):
    """ Take user inputs for open/closed times. """
    if not debug:
        open = input("Input a desired Open time in msec: ")
        close = input("Input a desired Close time in msec: ")
        time_len = input("Input a desired simulation time in msec: ")
    
    if open:
        mean_open_time = float(open) * 1e-3 # take ms convert to s
    else: 
        mean_open_time = 2e-2 # default
								
    if close:
        mean_close_time = float(close) * 1e-3 # take ms convert to s
    else: 
        mean_close_time = 5e-2 # default

    if time_len:
        interval = float(time_len) * 1e-3 # take ms convert to s
    else: 
        interval = 500e-3 # default
        
    print(mean_open_time, mean_close_time, interval)   
    return mean_open_time, mean_close_time, interval

def get_randoms(mean_open_time, mean_close_time, interval):
    """ Generates open and close times randomly """
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

def record_channel(interval, dt):
    """ Not sure why this must exist """
    def trim_times(open_time, close_time, over_shoot, start_state):
        if start_state and over_shoot > close_time:
            open_time = step_time - over_shoot
            close_time = 0.0
        elif start_state and over_shoot <= close_time:
            close_time = step_time - over_shoot - open_time
        elif not start_state and over_shoot > open_time:
            close_time = step_time - over_shoot
            open_time = 0.0
        elif not start_state and over_shoot <= open_time:
            open_time = step_time - over_shoot - close_time
        return open_time, close_time
    
    def run_channel(open, closed, g_open=1, start_open=False):
        channel = []
        n_open_steps = int(open/dt)
        n_close_steps = int(closed/dt)
        opening = [g_open for i in range(n_open_steps)]
        closing = [0 for i in range(n_close_steps)]
        if start_open:
            channel = opening + closing
        else:
            channel = closing + opening
        return channel

    channel_data = []
    over_shot = False
    cum_time = 0.0
    start_state = randint(0, 1)  # initial state is 0=closed, or 1=open
    for open, close in zip(opens, closes):
        open_time = open * mean_open_time
        close_time = close * mean_close_time
        step_time = open_time + close_time
        cum_time += step_time
        if cum_time > interval:
            over_shoot = cum_time - interval
            open_time, close_time = trim_times(open_time, close_time, over_shoot, start_state)
            over_shot = True
        channel_data += run_channel(open_time, close_time,
                                    start_open=start_state)
        if over_shot:
            break
    return channel_data

def add_noise(channel_data, amp):
    """ Adds noise to the on and off states to make it more biological-looking """
    noise = np.random.normal(size=len(channel_data)) #takes the output from record_channel and makes a tuple of random numbers using Numpy
    scaled_noise = noise * amp #takes your randoms from the last line and scales them down to 5% of what they were
    chan_dat_np = np.array(channel_data)+scaled_noise #creates an array from our channel_data list input and adds our scaled noise to it
    return chan_dat_np #returns the output of the line above as the function output
    
    
""" THIS IS THE MAIN """
if __name__ == "__main__": 
    # Receive inputs for open, closed, and total times
    mean_open_time, mean_close_time, interval = input_times()
    # Concoct random open and closed times    
    opens, closes = get_randoms(mean_open_time, mean_close_time, interval)
    open_avg = opens.mean()
    closed_avg = closes.mean()
    print(open_avg, closed_avg)
    dt = 1e-5
    channel_data = record_channel(interval, dt)
    channel_times = [i*dt for i in range(len(channel_data))]

    # Noise addition
    noise_amp = 0.05
    chan_dat_np = add_noise(channel_data, noise_amp)

    # Data formatting
    data = {'time': channel_times, 'record': channel_data}
    
    # Plotting
    my_record = DataFrame(data)
    #my_record.plot() 
    plt.plot(data['time'], data['record'])
    # plt.axes([0.0, 0.3, 0, 1.5])
    plt.show()
