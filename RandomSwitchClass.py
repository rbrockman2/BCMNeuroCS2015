# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:18:24 2015

@author: Jiakun Fu
"""

import numpy as np
from random import randint

class RandomSwitch():  
    def __init__(self, open_lifetime_ms=2, closed_lifetime_ms=3):
        self.open_lifetime = float(open_lifetime_ms) * 1e-3  # convert ms to s
        self.closed_lifetime = float(closed_lifetime_ms) * 1e-3  # convert ms to s
    
    def get_randoms(self, run_time):
        """ Generates open and close times randomly """
        too_short = True
        samples = 10
        while too_short:
            # Repeats until we get enough samples
            opens = np.random.exponential(size=samples) # random intervals, mean 1
            closes = np.random.exponential(size=samples) # random intervals, mean 1
            time_covered = self.open_lifetime * sum(opens) + self.closed_lifetime * sum(closes)
            if time_covered > run_time:
                too_short = False
            else:
                samples *= 2
        return opens, closes    
    
    def run_switch_cycle(self, open_time, close_time, dt, g_open=1, start_open=False):
        switch_data_one_cycle = []
        # to minimize roundup error here, we need to make sure dt is small enough, i.e. less than a tenth of the open or closed lifetime.
        n_open_steps = int(open_time/dt)
        n_close_steps = int(close_time/dt)
        opening = [g_open for i in range(n_open_steps)]
        closing = [0 for i in range(n_close_steps)]
        if start_open:
            switch_data_one_cycle = opening + closing
        else:
            switch_data_one_cycle = closing + opening
        return switch_data_one_cycle    
    
    def record_channel(self,run_time, dt, opens, closes):        
        switch_data = []
        start_state = randint(0, 1)  # initial state is 0=closed, or 1=open
        for single_open, single_close in zip(opens, closes):
            open_time = single_open * self.open_lifetime  # Scale to average open time.
            close_time = single_close * self.closed_lifetime  # Scale to average close time.
            switch_data += self.run_switch_cycle(open_time, close_time, dt, start_open=start_state)
            n_steps = len(switch_data) # have to check channel_data instead of summing up open and closed times because in run-channel, int(open/dt) has roundup errors that makes us loose a few data points.
            if n_steps > int(run_time/dt):
                break
        # We need to make sure the for loop can generate data that is longer than run_time/dt.
        trimmed_data = switch_data[0:int(run_time/dt)]
        return trimmed_data

    def run_switch(self, run_time_ms=500, dt_ms=0.1):  # added dt as input to this function instead of having default value. By Jiakun: I changed the default value to 0.1 msec so it would be a small enough number for short open or closed lifetime.      
        run_time = run_time_ms * 1e-3  # convert ms to s
        dt = dt_ms * 1e-3  # convert ms to s

        # Construct random open and closed times    
        opens, closes = self.get_randoms(run_time)

        channel_data = self.record_channel(run_time, dt, opens, closes)

        return channel_data