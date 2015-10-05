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
        if open_lifetime < 0:
            print("Negative lifetimes not allowed.")
            open_lifetime = 0

        if closed_lifetime < 0:
            print("Negative lifetimes not allowed.")
            closed_lifetime = 0

        if open_lifetime == 0 and closed_lifetime == 0:
            print("Channel must have a defined state.")
            closed_lifetime = 1

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

        # Ensure random generator called with legitimate values.
        if self.open_lifetime > 0:
            open_time = np.random.exponential(scale=self.open_lifetime)
        else:
            open_time = 0

        if self.closed_lifetime > 0:
            closed_time = np.random.exponential(scale=self.closed_lifetime)
        else:
            closed_time = 0

        n_open_steps = int(open_time/dt)
        n_close_steps = int(closed_time/dt)
        opening = [1 for i in range(n_open_steps)]
        closing = [0 for i in range(n_close_steps)]
        if start_open:
            switch_data_one_cycle = opening + closing
        else:
            switch_data_one_cycle = closing + opening
        return switch_data_one_cycle

    def run_switch(self, run_time=500, dt=0.1):
        """Generates a sequence of 1s and 0s corresponding to whether the
        switch is open or closed at any given time step.  Returned list
        represents switch state for an entire data run.

        Inputs:
            run_time:  length of data run in ms
            dt:  time step in ms

        Outputs:
            trimmed_switch_data:  sequence of 1s and 0s corresponding to the
                state of the switch at each time step.  1 is open, 0 is closed.
        """
        switch_data = []
        start_state = randint(0, 1)  # initial state is 0=closed, or 1=open

        total_data_length = int(run_time/dt)  # number of samples needed

        while len(switch_data) < total_data_length:
            switch_data += self.run_switch_cycle(dt, start_open=start_state)

        # Remove extra samples to ensure consistent length.
        trimmed_switch_data = switch_data[0:total_data_length]
        return trimmed_switch_data
