# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:19:21 2015

@author: uday, kim
"""

from ChannelClass import Channel

class Membrane():
    def __init__(self):   
        self.channel_set = []
        self.Temp = 298 #set default value to 298K
        self.SimulationTime = 100 #set default simulation time to 20ms
        self.get_membrane_parameters()
        self.create_channel_set()
        
    def get_membrane_parameters(self):
        self.Temp = int(input("Enter Temperature (Kelvin) ::"))
        self.SimulationTime = int(input("Enter Total Simulation Time (msec)::"))
        self.dT = float(input("Enter dT step (msec)"))
 
    def create_channel_set(self):
        more_channels = True
        while more_channels == True:   
            self.channel_set.append(Channel())
            continueQuery = input("Add more channels?  (y/N) ")
            if continueQuery.lower() == 'y':
                more_channels = True
            else:
                more_channels = False
    

    def plot_current(self):  
        total_current_TS = []

        for channel in self.channel_set:
            channel_current_TS_local = channel.computeCurrentTS(self.SimulationTime, self.dT, self.Temp)
            if total_current_TS == []:
                total_current_TS = channel_current_TS_local
            else:
                total_current_TS += channel_current_TS_local
        print(total_current_TS)                            


if __name__ == "__main__": 
    myMembrane = Membrane()
    myMembrane.plot_current()
    
    
    #TODO: Add Test Functions
        
        