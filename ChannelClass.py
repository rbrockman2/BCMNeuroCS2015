# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 20:40:30 2015

@author: Olivia
"""


from RandomSwitchClass import RandomSwitch
import numpy as np
from math import exp

debug=True

class Channel():
    """This class models the properties of all of the channels of a specific
    type in a cell membrane.  There can be many individual channels for
    each channel type object, each of which will flip open and closed randomly
    according to specified kinetic properties which can be affected by
    membrane voltage."""
    def __init__(self, **propDict):
        '''Creates an instance of the channel class with properties:
            lifeo   lifetime open in ms at 0 mV
            lifec   lifetime closed in ms at 0 mV
            zg      gating charges
            d       delta
            N       number of this kind of channel
            name    name of the channel
            gamma   single-channel conductance (S)
            E0      reversal potential for the channel (mV)
        
        You have a few different options for setting channel proerties.
        You may:
            1) send a populated dictionary to the class with all of the keys:
                name, lifeo, lifec, zg, d, N, gamma, E0
                
                ** MAKE SURE YOU USE THE EXACT SAME KEY CASE AND SPELLING **
                
                    e.g. 
                    myDict = {'name': 'test', 'lifeo': 10, 'lifec': 20,
                              'zg': 1, 'd': 0.8, 'N': 100,
                              'gamma': 10e-9, 'E0': 0}
                    myChannel = Channel(**myDict)
                this class is not equipped to deal with different input keys
            2) send a populated dictionary to the class with  some of the keys:
                name, lifeo, lifec, zg, d, N, gamma, E0
                
                ** any key you omit will default to 0 (or generic in the case
                of name) **
                
                    e.g.
                    myDict = {'name': 'test', 'lifeo': 10, 'lifec': 20,
                              'N': 100, 'gamma': 10e-9}
                    myChannel = Channel(**myDict)
            3) send an empty dictionary to the class
                ** this will prompt the class to ask the user to input
                info about channel properties into the console window**
                    
                    e.g.
                    myChannel = Channel()
        
        Once you've created your Channel instance, you can use 
        instancename.computeCurrentTS to find the current that a group of
        channels with the instance's properties would pass over a specified
        amount of time.
                
        '''
        ui_name, ui_lifeo, ui_lifec, ui_zg, ui_d, ui_N, ui_E0, ui_gamma = self.getParams(**propDict)
        self.lifeo = ui_lifeo
        self.lifec = ui_lifec
        self.zg = ui_zg
        self.d = ui_d
        self.N = ui_N
        self.name = ui_name
        self.E0 = ui_E0
        self.gamma = ui_gamma
    
    def getParams(self, **thisDict):
        '''getParams sets values to the channel's properties. If the user sent
        an empty dictionary, then this function will ask the user for
        information about the channel. If the user sent a populated dictionary,
        this function will set the channel properties to the values specified
        in the dictionary.
            Note that this function isn't equipped to deal with variable
        dictionary keys. Also note that '''
        IsReversalPotentialVerified = False        
        IsOpenLifetimeVerified = False
        IsClosedLifetimeVerified = False
        IsGammaVerified = False
        IsDeltaVerified = False
        IsGatingChargeVerified = False
        IsChannelNumVerified = False
        
        if len(thisDict) == 0:
            name = input("What is this channel's name?: ")
            while IsReversalPotentialVerified is False:
                ErevStr = input("What is this channel's 0-current potential? (mV): ")
                try:
                    Erev = float(ErevStr)
                except ValueError:
                    print("Error: Reversal Potential entered is not a floating point number")
                else:
                    if Erev < -200 or Erev > 400:
                        print("Warning: ErevStr is outside -200mV to 400mV range")  
                        IsItOK = input("Is this OK (Y/N)?")
                        if IsItOK.lower() == 'y':
                            IsReversalPotentialVerified = True
                        else:
                            IsReversalPotentialVerified = False
                    else:
                        IsReversalPotentialVerified = True
            
            while IsOpenLifetimeVerified is False:
                openlifeStr = input("What is this channel's open lifetime (msec)?: ")
                try:
                    openlife = float(openlifeStr)
                except ValueError:
                    print("Error: Open Lifetime was not entered as a positive floating point number") 
                else:
                    if openlife <= 0:
                        print("Error: Open Lifetime was not entered as a positive floating point number")
                    else:
                        IsOpenLifetimeVerified = True
                        
            while IsClosedLifetimeVerified is False:     
                closedlifeStr = input("What is this channel's closed lifetime (msec)?: ")
                try:
                    closedlife = float(closedlifeStr)
                except ValueError:
                    print("Error: Closed Lifetime was not entered as a positive floating point number") 
                else:
                    if closedlife <= 0:
                        print("Error: Closed Lifetime was not entered as a positive floating point number")
                    else:
                        IsClosedLifetimeVerified = True
            
            while IsGammaVerified is False:     
                gammaStr = input("What is the single-channel conductance (S)?: ")
                try:
                    gamma = float(gammaStr)
                except ValueError:
                    print("Error: Single Channel Conductance was not entered as a positive floating point number") 
                else:
                    if gamma <= 0:
                        print("Error: Single Channel Conductance was not entered as a positive floating point number") 
                    else:
                        IsGammaVerified = True
            
            while IsGatingChargeVerified is False:     
                gatingChargesStr = input("How many gating charges does this channel have?: ")
                try:
                    gatingCharges = float(gatingChargesStr)
                except ValueError:
                    print("Error: Gating Charge was not entered as a floating point number") 
                else:
                    IsGatingChargeVerified = True
            
            while IsDeltaVerified is False:     
                deltaStr = input("What is delta for this channel's gating charge (0-1)?: ")
                try:
                    delta = float(deltaStr)
                except ValueError:
                    print("Error: Delta was not entered as a number between 0 and 1") 
                else:
                    if delta < 0 or delta > 1:
                        print("Error: Delta was not entered as a number between 0 and 1") 
                    else:
                        IsDeltaVerified = True       
            while IsChannelNumVerified is False:
                numberStr = input("How many of these channels are there?: ")
                try:
                    number = int(numberStr)
                except ValueError:
                    print("Error: Number of channels entered is not a positive integer")                
                else:
                    if number <= 0:
                        print("Error: Number of channels entered is not a positive integer")    
                    else:
                        IsChannelNumVerified = True
    
        else:
            # default everything to 0
            Erev = 0
            openlife = 0
            closedlife = 0
            gamma = 0
            gatingCharges = 0
            number = 0
            delta = 0
            name = 'generic'
            
            # pull the given values from the dictionary
            count = 0
            for key, val in thisDict.items():
                if key == 'name':
                    name = val
                    count += 1
                elif key == 'E0':
                    Erev = val
                    count += 1
                elif key == 'lifeo':
                    openlife = val
                    count += 1
                elif key == 'lifec':
                    closedlife = val
                    count += 1
                elif key == 'gamma':
                    gamma = val
                    count += 1
                elif key == 'zg':
                    gatingCharges = val
                    count += 1
                elif key == 'd':
                    delta = val
                    count += 1
                elif key == 'N':
                    number = val
                    count += 1
                else:
                    print('Found unrecognized channel property "{0}"'.format(key))
            if count < 8:
                print('WARNING: Some channel properties left at default values.')
        return name, openlife, closedlife, gatingCharges, delta, number, Erev, gamma

    def compute_current_TS(self, Vm, record_time, dt, T):
        '''This function is set up to be called from outside (i.e., from a Membrane
        object that contains this channel object). If computes the current
        passed by all of the channels of this type for each time step.

        Inputs:
            Vm:  the membrane voltage the channel is clamped at in mV
            record_time:  the duration of the recording in ms
            dt:  the duration of the time step in ms
            T:  temperature in K

        Outputs:
            current_TS:  a vector with the current being passed by the channels
                in each bin of dt, with the first bin corresponding to
                time 0 to dt, the second bin corresponding to time dt to 2*dt,
                etc.'''

        # Adjust open and closed lifetimes for voltage dependence.
        lifeo_Vm, lifec_Vm = self.compute_voltage_dependence(T, Vm)

        # Calculate the number of channels that are open at each time step.
        num_open_channel_TS = Channel.open_channel_TS(record_time, dt, self.N,
                                                      lifeo_Vm, lifec_Vm)

        mean_open_channels = sum(num_open_channel_TS) / \
            float(len(num_open_channel_TS))

        if debug is True:
            print("Lifetimes: {0} {1}".format(lifeo_Vm, lifec_Vm))
            print("Average # of open channels: {0}".format(mean_open_channels))

        # Compute current from all channels of this type for each time step.
        current_TS = Channel.currentFromTimeSeries_oneVm(num_open_channel_TS,
                                                         self.gamma, Vm,
                                                         self.E0)

        return current_TS

    def compute_voltage_dependence(self, T=295, Vm=0):
        """This function computes the voltage dependent open and closed
        lifetimes for this channel type.

        Inputs:
            T:  temperature in K
            Vm:  the membrane voltage the channel is clamped at in mV

        Outputs:
            lifeo_Vm:  voltage-adjusted lifetime of open state for this channel
            lifec_Vm:  voltage-adjusted lifetime of closed state for this
                channel."""

        F = 96485  # Faraday's constant in coloumbs per mole
        R = 8.314  # Ideal gas constant in J / (mole * K)

        lifeo_Vm = self.lifeo * exp((self.d*self.zg*F*(Vm/1000))/(R*T))
        lifec_Vm = self.lifec * exp(((1-self.d)*-1*self.zg*F*(Vm/1000))/(R*T))
        return lifeo_Vm, lifec_Vm

    @staticmethod
    def open_channel_TS(total_time, dt, n_channels,
                        lifetime_open, lifetime_closed):
        """Generates a time series of how many channels are open at each time
        step.  This is done by generating a time series for whether each
        individual channel is open at each time step and then summing these
        series.

        Inputs:
            total_time:  length of time series in ms
            dt:  duration of time step in ms
            n_channels:  number of channels
            lifetime_open:  mean open lifetime of a channel
            lifetime_closed:  mean closed lifetime of a channel

        Outputs:
            summed_series:  time series of how many channels are open at each
                time step.
        """
        # The random switch will generate a time series for a single channel.
        random_switch = RandomSwitch(lifetime_open, lifetime_closed)
        summed_series = []  # Accumulator
        for i in range(n_channels):
            single_series = random_switch.run_switch(total_time, dt)
            if i > 0:
                # Add series from single channel to total.
                # Time series are converted to lists to maintain type
                #   consistency.
                summed_series = np.add(summed_series, single_series).tolist()
            else:
                summed_series = single_series
        return summed_series

    @staticmethod
    def currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex):
        '''
        Given the number of channels active at a series of times, this function
        will return a vector of the current passed by these channels during this
        series of time.
        
        This function assumes that timeseries describes the number of ONE KIND of
        channels that are open at a given time.
        
        Inputs:
        timeseries  a vector of integers where the integer means the number of 
                    channels active in the bin
        gamma       single-channel conducance in S
        Vm          voltage being clamped to in mV
        Ex          0-current potential for the channel in mV
        
        Outputs:
        current_series  the current in each time bin
    
        Written by Olivia.    
        '''
        Vm_inV = float(Vm * 10**-3)
        Ex_inV = float(Ex * 10**-3)

        current_series = [N * gamma * (Vm_inV - Ex_inV) for N in timeseries]

        return current_series            
