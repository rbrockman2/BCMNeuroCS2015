import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from random import randint
debug = True

from record_channel import record_channel
from add_noise import add_noise
from get_randoms import get_randoms
from input_times import input_times


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
    channel_data = record_channel(interval, dt, opens, closes, mean_open_time, mean_close_time)
    channel_times = [i*dt for i in range(len(channel_data))]

    # Noise addition
    noise_amp = 0.05
    chan_dat_np = add_noise(channel_data, noise_amp)

    # Data formatting
    data = {'time': channel_times, 'record': chan_dat_np}
    
    # Plotting
    my_record = DataFrame(data)
    #my_record.plot() 
    plt.plot(data['time'], data['record'])
    # plt.axes([0.0, 0.3, 0, 1.5])
    plt.show()
