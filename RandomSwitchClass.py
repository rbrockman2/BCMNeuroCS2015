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

    def __init__(self, open_lifetime=2, closed_lifetime=3):
        """Constructor.

        Inputs:
            open_lifetime:  mean time the switch stays open in ms
            closed_lifetime:  mean time the switch stays closed in ms"""

        # Convert ms to s.
        self.open_lifetime = float(open_lifetime)
        self.closed_lifetime = float(closed_lifetime)

    def run_switch_cycle(self, dt, start_open=False):
        """Generates a sequence of 1s and 0s corresponding to whether the
        switch is open or closed at any given time step.  Returned list
        accounts for one complete cycle of open and closed states.

        Inputs:
            dt:  time step in ms
            start_open:  True if the switch starts open, False if closed

        Outputs:
            switch_data_one_cycle:  sequence of 1s and 0s corresponding to the
                state of the switch at each time step.  1 is open, 0 is closed.
        """
        switch_data_one_cycle = []

        open_time = np.random.exponential(scale=self.open_lifetime)
        closed_time = np.random.exponential(scale=self.closed_lifetime)

        n_open_steps = int(open_time/dt)
        n_close_steps = int(closed_time/dt)
        opening = [1 for i in range(n_open_steps)]
        closing = [0 for i in range(n_close_steps)]
        if start_open:
            switch_data_one_cycle = opening + closing
        else:
            switch_data_one_cycle = closing + opening
        return switch_data_one_cycle

    def run_switch(self, run_time=500, dt=1):  # added dt as input to this function instead of having default value        
        switch_data = []
        start_state = randint(0, 1)  # initial state is 0=closed, or 1=open

        total_data_length = int(run_time/dt)

        while len(switch_data) <= total_data_length:
            switch_data += self.run_switch_cycle(dt, start_open=start_state)

        trimmed_switch_data = switch_data[0:int(run_time/dt)]
        return trimmed_switch_data
