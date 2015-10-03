# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:19:21 2015

@author: uday, kim
"""

from ChannelClass import Channel
import numpy as np
import math
from pandas import DataFrame
from random import randint
debug = True
import matplotlib.pyplot as plot

class Membrane():
    """
    Created on Wed Sep 30 21:19:21 2015

    @author: uday, kim
    """
    def __init__(self):   
        self.channel_set = []
        self.Temp = 298 #set default value to 298K
        self.simulation_time = 100 #set default simulation time to 20ms
        self.get_membrane_parameters()
        self.create_channel_set()
        self.noise_amp = 0.05
        
    def get_membrane_parameters(self):
        # Todo:  add option to use default parameters.
        self.Temp = int(input("Enter Temperature (Kelvin) ::"))
        self.SimulationTime = int(input("Enter Total Simulation Time (msec)::"))
        self.dt = float(input("Enter dt step (msec)"))
 
    def create_channel_set(self):
        more_channels = True
        while more_channels == True:   
            self.channel_set.append(Channel())
            continueQuery = input("Add more channels?  (y/N) ")
            if continueQuery.lower() == 'y':
                more_channels = True
            else:
                more_channels = False

    def compute_current(self):  
        total_current_TS = []

        for channel in self.channel_set:
            channel_current_TS_local = channel.computeCurrentTS(self.simulation_time, self.dt, self.Temp)
            if total_current_TS == []:
                total_current_TS = channel_current_TS_local
            else:
                total_current_TS += channel_current_TS_local
        return total_current_TS
    
    @staticmethod
    def add_noise(channel_data, amp):
        """ATTN: there is unit testing stuff in here you will need to get rid of for actual inputs"""
        """ Adds noise to the on and off states to make it more biological-looking """
        noise = np.random.normal(size=len(channel_data)) #takes the output from record_channel and makes a tuple of random numbers using Numpy
        scaled_noise = noise * amp #takes your randoms from the last line and scales them down to 5% of what they were
        chan_dat_np = np.array(channel_data)+scaled_noise #creates an array from our channel_data list input and adds our scaled noise to it
        return chan_dat_np #returns the output of the line above as the function's output

    @staticmethod
    def plot_current_TS(current_TS, time, dt=1E5):
        # Gabe and Carli take on the world of magic and marvel, a world of plot perfection
                 
             
        x_axis = []    
        i = 0    
        while i < time: # create x_axis list in correct time steps
            x_axis += [i] 
            i += dt
            
        nano_current = []
        for item in current_TS: 
            item = item*(10**9) # convert to nanoamps for graph prettiness
            nano_current += [item]
        y_axis = nano_current

        print(dt)
        print(len(y_axis))            
        print(len(x_axis))            

            
#        plot.plot(x_axis, y_axis, label='time', marker='o', color='maroon', linestyle = '-')
 #       plot.xlabel('Time (msec)')
  #      plot.ylabel('Net current (nA)')
   #     plot.title('Title Title Title')
    #    plot.grid()
     #   plot.show()
      
      #plot.savefig('program_output.pdf')
        
    def make_plot(self):        
        current_TS = self.compute_current()
        noisy_TS = Membrane.add_noise(current_TS,self.noise_amp)        
        
        Membrane.plot_current_TS(noisy_TS,self.simulation_time*1000,self.dt)    


dt=1
time = 8
amp = 0.05
channel_data = [1,2,3,4,5,6,7,8]
noise_currents = Membrane.add_noise(channel_data, amp)
x = Membrane.plot_current_TS(noise_currents, time, dt)


                    


if __name__ == "__main__": 
    myMembrane = Membrane()
    myMembrane.make_plot()
    
    
    #TODO: Add Test Functions
        
        