# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:19:21 2015

@author: uday, kim
"""

from ChannelClass import Channel

class Membrane():
    def __init__(self):
        self.channel_sets_initialized_count = 0     
        self.channel = []
        self.Temp = 298 #set default value to 298K
        self.SimulationTime = 100 #set default simulation time to 20ms
    def get_user_input(self):
        self.Temp = int(input("Enter Temperature (Kelvin) ::"))
        self.SimulationTime = int(input("Enter Total Simulation Time (msec)::"))
        self.dT = float(input("Enter dT step (msec)"))
    def define_and_init_new_channel_set(self):
        self.channel.append(Channel())
        #self.channel[self.channel_sets_initialized_count].getParams()
        self.channel[self.channel_sets_initialized_count].computeCurrentTS( \
            self.SimulationTime, self.dT, self.Temp)
        self.channel_sets_initialized_count = self.channels_sets_initialized_count + 1

if __name__ == "__main__": 
    myMembrane = Membrane()
    myMembrane.get_user_input()
    myMembrane.define_and_init_new_channel_set()
    
    #TODO: Add Test Functions
        
        