# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:18:24 2015

@author: Titan
"""

import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
from random import random
debug = False

def noiseless_channel(open_lifetime, closed_lifetime, time, dt):  # added dt as input to this function instead of having default value
    def input_times(open = 0.0, close = 0.0, time_len = 0.0):
        """ Take user inputs for open/closed times in msec."""
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
            
        #print(mean_open_time, mean_close_time, interval)   
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
    
    def record_channel(time, interval, dt, open_lifetime, closed_lifetime):
        """ Not sure why this must exist """
        '''def trim_times(open_time, close_time, over_shoot, start_state):
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
            return open_time, close_time'''
        
#        def run_channel(open, closed, g_open=1, start_open=False):
#            channel = []
#            n_open_steps = int(open/dt)
#            n_close_steps = int(closed/dt)
#            opening = [g_open for i in range(n_open_steps)]
#            closing = [0 for i in range(n_close_steps)]
#            if start_open:
#                channel = opening + closing
#            else:
#                channel = closing + opening
#            print('channel length', len(channel))
#            return channel
#    
#        channel_data = []
#        over_shot = False
#        cum_time = 0.0
#        start_state = randint(0, 1)  # initial state is 0=closed, or 1=open
#        for open, close in zip(opens, closes):
#            open_time = open * mean_open_time
#            close_time = close * mean_close_time
#            step_time = open_time + close_time
#            #print(step_time)
#            cum_time += step_time
#            #print(cum_time)
#            if cum_time > interval:
#                over_shot = cum_time - interval
#                #open_time, close_time = trim_times(open_time, close_time, over_shoot, start_state)
#                over_shot = True
#            channel_data += run_channel(open_time, close_time,
#                                        start_open=start_state)
#            
#            if over_shot:
#                break
            
        channel = []
        # dt is bin size
        # you want recording duration in ms / dt in ms = number of bins
        print('time', time)
        print('dt', dt)
        n_bins = int(time/dt)
        state = randint(0, 1)
        openlifedist = np.random.normal(open_lifetime, .10 * open_lifetime, 100)  # generate 100 possible open liftimes centered at open_lifetime with variance equal to 10% of lifetime
        closedlifedist = np.random.normal(closed_lifetime, .10 * closed_lifetime, 100)  # same for closed
        pick = randint(0, 99)
        if state == 1:
            countdown = int(openlifedist[pick]/dt)
            if countdown <= 0:
                countdown = dt
        else:
            countdown = int(closedlifedist[pick]/dt)
            if countdown <= 0:
                countdown = dt
        for pos in range(0, n_bins):
            if state == 1:
                change_to = 0
            else:
                change_to = 1
            if countdown == 0:  # then let the channel be open
                state = change_to
                pick = randint(0, 99)
                if state == 1:
                    countdown = int(openlifedist[pick]/dt)
                    if countdown <= 0:
                        countdown = dt
                else:
                    countdown = int(closedlifedist[pick]/dt)
                    if countdown <= 0:
                        countdown = dt
            channel.append(state)
            countdown -= 1
        
        
        
        
#        # chopping it at interval
#        print('interval/dt', interval/dt)
#        print('trimmed_data length', int(interval/dt))
#        print('channel data length', len(channel_data))
#        trimmed_data = channel_data[0:int(interval/dt)]
        return channel
    
    '''def add_noise(channel_data, amp):
        """ Adds noise to the on and off states to make it more biological-looking """
        noise = np.random.normal(size=len(channel_data))
        scaled_noise = noise * amp
        chan_dat_np = np.array(channel_data)+scaled_noise
        return chan_dat_np
    '''
    

    # Receive inputs for open, closed, and total times
    mean_open_time, mean_close_time, interval = input_times(open_lifetime, closed_lifetime, time)
    print('mean open time', mean_open_time)
    print('mean close time', mean_close_time)
    print('interval', interval)
    # Concoct random open and closed times    
    opens, closes = get_randoms(mean_open_time, mean_close_time, interval)
    #open_avg = opens.mean()
    #closed_avg = closes.mean()
    #print(open_avg, closed_avg)
    #dt = 1e-5  # commented out to test sending dt as input
    channel_data = record_channel(time, interval, dt, open_lifetime, closed_lifetime)
    print('returning vector of length', len(channel_data))
    print('')
    #channel_times = [i*dt for i in range(len(channel_data))]


    # Data formatting
    #data = {'time': channel_times, 'record': channel_data}
    
    return channel_data
    # Plotting
    #my_record = DataFrame(data)
    #my_record.plot() 
    #plt.plot(data['time'], data['record'])
    # plt.axes([0.0, 0.3, 0, 1.5])
    #plt.show()
