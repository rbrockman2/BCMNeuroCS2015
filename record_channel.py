import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

def record_channel(interval, dt):
    """ Enforces correct ratio of closed to open times from random data """
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