# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:18:24 2015

@author: Jiakun Fu
"""
import numpy as np
from random import randint


class RandomSwitch():
    """This class is a model of a switch that turns itself on and off randomly
    with time according to Poisson statisics."""

    def __init__(self, open_lifetime_ms=2, closed_lifetime_ms=3):
        """Constructor.

        Inputs:
            open_lifetime_ms:  mean time the switch stays open in ms
            closed_lifetime_ms:  mean time the switch stays closed in ms"""

        # Convert ms to s.
        self.open_lifetime = float(open_lifetime_ms) * 1e-3
        self.closed_lifetime = float(closed_lifetime_ms) * 1e-3

    def get_randoms(self, run_time):
        """Generates Poisson distributions for opening and closing with mean 1.
        Sufficient statistics are generated to cover the entire time the
        switch is operating.

        Inputs:
            run_time:  total time the switch is operating in seconds.

        Outputs:
            opens:  list of numbers exponentially distributed with mean 1.
            closes:  list of numbers exponentally distributed with mean 1."""
        too_short = True
        samples = 10
        while too_short:
            # Repeats until we get enough samples.
            # Generates random intervals, mean of 1.
            opens = np.random.exponential(size=samples)
            closes = np.random.exponential(size=samples)

            # Length of time covered by scaled sum of all intervals must
            # cover run time.
            time_covered = self.open_lifetime * sum(opens) + \
                self.closed_lifetime * sum(closes)

            if time_covered > run_time + \
                    10*samples*(self.open_lifetime + self.closed_lifetime):
                too_short = False
            else:
                samples *= 2
        return opens, closes

    def run_switch_cycle(self, open_time, close_time, dt, start_open=False):
        """Generates a sequence of 1s and 0s corresponding to whether the
        switch is open or closed at any given time step.  Returned list
        accounts for one complete cycle of open and closed states.

        Inputs:
            open_time:  time that switch is to be open in s (randomized)
            close_time:  time that switch is to be closed in s (randomized)
            dt:  time step in s
            start_open:  True if the switch starts open, False if closed

        Outputs:
            switch_data_one_cycle:  sequence of 1s and 0s corresponding to the
                state of the switch at each time step.  1 is open, 0 is closed.
        """
        switch_data_one_cycle = []
        n_open_steps = int(open_time/dt)
        n_close_steps = int(close_time/dt)
        opening = [1 for i in range(n_open_steps)]
        closing = [0 for i in range(n_close_steps)]
        if start_open:
            switch_data_one_cycle = opening + closing
        else:
            switch_data_one_cycle = closing + opening
        return switch_data_one_cycle

    def run_switch(self, run_time_ms=500, dt_ms=1):  # added dt as input to this function instead of having default value        
        run_time = run_time_ms * 1e-3  # convert ms to s
        dt = dt_ms * 1e-3  # convert ms to s

        # Get random open and close intervals sufficient to cover the run time.
        # Note these lists have mean 1 -- they have not been scaled by the
        # average open and closed times yet.
        opens, closes = self.get_randoms(run_time)

        switch_data = []
        start_state = randint(0, 1)  # initial state is 0=closed, or 1=open

        # Choose one random open and close interval at a time.
        for single_open, single_close in zip(opens, closes):
            # Scale open and closed interval by the mean open and closed
            # lifetimes.
            open_time = single_open * self.open_lifetime
            close_time = single_close * self.closed_lifetime

            switch_data += self.run_switch_cycle(open_time, close_time, dt, start_open=start_state)
            n_steps = len(switch_data) # have to check channel_data instead of summing up open and closed times because in run-channel, int(open/dt) has roundup errors that makes us loose a few data points.
            if n_steps > int(run_time/dt):
                break
        # chopping it at interval
        trimmed_switch_data = switch_data[0:int(run_time/dt)]
        return trimmed_switch_data
