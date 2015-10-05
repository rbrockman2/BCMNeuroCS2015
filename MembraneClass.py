# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:19:21 2015

@author: uday, kim
"""

import matplotlib.pyplot as plot
from ChannelClass import Channel
import numpy as np
debug = True


class Membrane():
    """
    Created on Wed Sep 30 21:19:21 2015

    @author: uday, kim
    """
    def __init__(self):
        """This function creates an instance of the membrane class with 
        our default membrane properties. User will also have option to set the 
        parameters. Temperature is in Kelvin. Time is in msec."""
        self.channel_set = []
        self.Vm = -65
        self.Temp = 310 #set default value to 310K
        self.simulation_time = 100 #set default simulation time to 100ms
        self.dt = 0.01 #set default dt to 0.01 ms
        self.noise_amp = 1E-13
        
    def get_membrane_parameters(self):
        """This function will set the properties of the membranne either to 
        default values or can take user input."""
        IsMembraneVoltageVerified = False
        IsTempVerified = False
        IsSimTimeVerified = False
        IsDtVerified = False
        UseDefaultYN = input("Would you like to use defaults for Vm, Temp, Sim Time and dt? (Y/N) :")
        if UseDefaultYN.lower() != 'y':
            while IsMembraneVoltageVerified is False:     
                membraneVoltageStr = input("At what voltage would you like to clamp this channel (mV)?: ")
                try:
                    membraneVoltage = float(membraneVoltageStr)
                except ValueError:
                    print("Error: Membrane Voltage was not entered as a number") 
                else:
                    if membraneVoltage < -200 or membraneVoltage > 400:
                        print("Warning: Membrane Voltage is outside -200mV to 400mV range")
                        IsItOK = input("Is this OK (Y/N)?")
                        if IsItOK.lower() == 'y':
                            IsMembraneVoltageVerified = True
                        else:
                            IsMembraneVoltageVerified = False
                    else:
                        IsMembraneVoltageVerified = True         
            while IsTempVerified is False:
                Temperature = input("Enter Temperature (0K - 400K): ")
                try:
                    self.Temp = int(Temperature)
                except ValueError:
                    print("Error: Temperatures are outside expected range (0K - 400K)")                
                else:
                    if self.Temp < 0 or self.Temp > 400:
                        print("Error: Temperatures are outside expected range (0K - 400K)")    
                    else:
                        IsTempVerified = True
            while IsSimTimeVerified is False:
                SimTime = input("Enter Total Simulation Time (msec): ")
                try:
                    self.simulation_time = int(SimTime)
                except ValueError:
                    print("Error: Simulation Time was not entered as a positive integer") 
                else:
                    if self.simulation_time <= 0:
                        print("Error: Simulation Time was not entered as a positive integer")
                    else:
                        IsSimTimeVerified = True
            while IsDtVerified is False:
                dtStep = input("Enter dt step (<1msec): ")
                try:
                    self.dt = float(dtStep)
                except ValueError:
                    print("Error: dt step was not entered as a positive integer") 
                else:
                    if self.dt <= 0:
                        print("Error: dt step was not entered as a positive integer") 
                    elif self.dt > self.simulation_time:
                        print("Error: dt step entered is longer than Simulation time")
                    else: 
                        IsDtVerified = True
 
    def create_channel_set(self, **inDict):
        '''Takes a dictionary of dictionaries as input. If empty, query 
        user for more information. If has channel object as a dictionary entry,
        appends to channel_set.'''
        if len(inDict) == 0:
            more_channels = True
            while more_channels == True:   
                self.channel_set.append(Channel())
                continueQuery = input("Add more channels?  (y/N) ")
                if continueQuery.lower() == 'y':
                    more_channels = True
                else:
                    more_channels = False
        else:
            for channName, channObj in inDict.items():
                self.channel_set.append(channObj)

    def compute_current(self):  
        total_current_TS = []

        for channel in self.channel_set:
            channel_current_TS_local = channel.computeCurrentTS(self.Vm, self.simulation_time, self.dt, self.Temp)
            if total_current_TS == []:
                total_current_TS = channel_current_TS_local
            else:
                #total_current_TS += channel_current_TS_local
                temp = total_current_TS
                del total_current_TS
                total_current_TS = []
                for i in range(0, len(temp)):
                    total_current_TS.append(temp[i] + channel_current_TS_local[i])
        return total_current_TS
    
    @staticmethod
    def add_noise(channel_data, amp):
        """Worked on by Gabe S. and Elizabeth L."""
        """ATTN: there is unit testing stuff in here you will need to get rid of for actual inputs"""
        
        """This function adds noise to the on and off states to make it more biologically realistic.
        
        Inputs: 
            channel_data output of record_channel
            
        Outputs: 
            array of channel_data with noise added
        """
        
        noise = np.random.normal(size=len(channel_data)) #takes the output from record_channel and makes a tuple of random numbers using Numpy
        scaled_noise = noise * amp #takes your randoms from the last line and scales them down to 5% of what they were
        chan_dat_np = np.array(channel_data)+scaled_noise #creates an array from our channel_data list input and adds our scaled noise to it
        return chan_dat_np #returns the output of the line above as the function's output

    @staticmethod
    def plot_current_TS(current_TS, dt=1E5):
        """
        Plots a current time series.

        Inputs:
            current_TS:  a list of current values in amps
            dt: the time step size for the current time series in ms
            
        Authors: by Gabe and Carli.    
        
        """
               
        print("Time Step in ms {0}".format(dt));
        print("Length of the time series {0}".format(len(current_TS)))                
               
             
        x_axis = []    
        i = 0
        idx = 0
        while idx < len(current_TS): # create x_axis list in correct time steps
            x_axis += [i] 
            i += dt
            idx += 1
            
        nano_current = []
        for item in current_TS: 
            item = item*(10**9) # convert to nanoamps for graph prettiness
            nano_current += [item]
        y_axis = nano_current

            
        print("y_axis length {0}".format(len(y_axis)))
        print("x_axis length {0}".format(len(x_axis)))              
            
        plot.plot(x_axis, y_axis, label='time', color='maroon', linestyle = '-')
        plot.xlabel('Time (msec)')
        plot.ylabel('Net current (nA)')
        plot.title('Current Time Series')
        plot.grid()
        plot.show()
       
    def make_plot(self):        
        current_TS = self.compute_current()
        noisy_TS = Membrane.add_noise(current_TS,self.noise_amp)        
        
        Membrane.plot_current_TS(noisy_TS,self.dt)    