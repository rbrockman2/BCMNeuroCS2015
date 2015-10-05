# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:18:24 2015

@author: Jiakun Fu
"""

import numpy as np
from random import randint
debug = False


class RandomSwitch():
    
    def __init__(self, open_lifetime, closed_lifetime):   
        self.open_lifetime = open_lifetime
        self.closed_lifetime = closed_lifetime


    def input_times(self,time_len = 0.0):
        """ Take user inputs for open/closed times in msec."""
        open = self.open_lifetime
        close = self.closed_lifetime
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
    
    @staticmethod
    def get_randoms(mean_open_time, mean_close_time, interval):
        """ Generates open and close times randomly """
        too_short = True
        samples = 10
        while too_short:
            # Repeats until we get enough samples
            opens = np.random.exponential(size=samples)
            closes = np.random.exponential(size=samples)
            time_covered = mean_open_time * sum(opens) + mean_close_time * sum(closes)
            if time_covered > interval:
                too_short = False
            else:
                samples *= 2
        return opens, closes
    
    
    
    
    def record_channel(interval, dt, opens, closes, mean_open_time, mean_close_time):        
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
        start_state = randint(0, 1)  # initial state is 0=closed, or 1=open
        for open, close in zip(opens, closes):
            open_time = open * mean_open_time
            close_time = close * mean_close_time
            channel_data += run_channel(open_time, close_time,
                                        start_open=start_state)
            n_steps = len(channel_data) # have to check channel_data instead of summing up open and closed times because in run-channel, int(open/dt) has roundup errors that makes us loose a few data points.
            if n_steps > int(interval/dt):
                break
        # chopping it at interval
        trimmed_data = channel_data[0:int(interval/dt)]
        return trimmed_data

    def run_switch(self, run_time, dt):  # added dt as input to this function instead of having default value
    
            
        # Receive inputs for open, closed, and total times
        mean_open_time, mean_close_time, interval = self.input_times(run_time)
        # Concoct random open and closed times    
        opens, closes = RandomSwitch.get_randoms(mean_open_time, mean_close_time, interval)

        dt = dt/1000  # convert ms input into seconds units
        channel_data = RandomSwitch.record_channel(interval, dt, opens,closes,mean_open_time, mean_close_time)

        return channel_data
  
