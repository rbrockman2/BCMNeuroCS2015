import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

"""Edited by Uday, ***"""

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