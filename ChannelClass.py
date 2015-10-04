# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 20:40:30 2015

@author: Olivia
"""

from compute_voltage_dependence import compute_voltage_dependence
from channelSummer import channelSummer
from currentFromTimeSeries_oneVm import currentFromTimeSeries_oneVm

class Channel():
    def __init__(self, **propDict):
        '''Creates an instance of the channel class with properties:
            lifeo   lifetime open in ms
            lifec   lifetime closed in ms
            zg      gating charges
            d       delta
            Vm      voltage clamping channel to (mV)
            N       number of this kind of channel
            name    name of the channel
            gamma   single-channel conductance (S)
            E0      reversal potential for the channel (mV)
        O
        You have a few different options for setting channel proerties.
        You may:
            1) send a populated dictionary to the class with all of the keys:
                name, lifeo, lifec, zg, d, Vm, N, gamma, E0
                
                ** MAKE SURE YOU USE THE EXACT SAME KEY CASE AND SPELLING **
                
                    e.g. 
                    myDict = {'name': 'test', 'lifeo': 10, 'lifec': 20,
                              'zg': 1, 'd': 0.8, 'Vm': -65, 'N': 100,
                              'gamma': 10e-9, 'E0': 0}
                    myChannel = Channel(**myDict)
                this class is not equipped to deal with different input
            2) send a populated dictionary to the class with  some of the keys:
                name, lifeo, lifec, zg, d, Vm, N, gamma, E0
                
                ** any key you omit will default to 0 (or generic in the case
                of name) **
                
                    e.g.
                    myDict = {'name': 'test', 'lifeo': 10, 'lifec': 20,
                              'Vm': -65, 'N': 100, 'gamma': 10e-9}
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
        ui_name, ui_lifeo, ui_lifec, ui_zg, ui_d, ui_Vm, ui_N, ui_E0, ui_gamma = self.getParams(**propDict)
        self.lifeo = ui_lifeo
        self.lifec = ui_lifec
        self.zg = ui_zg
        self.d = ui_d
        self.Vm = ui_Vm
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
        if len(thisDict) == 0:
            name = input("What is this channel's name?: ")
            Erev = float(input("What is this channel's 0-current potential? (mV): "))
            openlife = float(input("What is this channel's open lifetime (msec)?: "))
            closedlife = float(input("What is this channel's closed lifetime (msec)?: "))
            gamma = float(input("What is the single-channel conductance (S)?: "))
            gatingCharges = float(input("How many gating charges does this channel have?: "))
            delta = float(input("What is delta for this channel's gating charge?: "))
            membraneVoltage = float(input("At what voltage would you like to clamp this channel (mV)?: "))
            number = int(input("How many of these channels are there?: "))
        else:
            # default everything to 0
            Erev = 0
            openlife = 0
            closedlife = 0
            gamma = 0
            gatingCharges = 0
            number = 0
            delta = 0
            membraneVoltage = 0
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
                elif key == 'Vm':
                    membraneVoltage = val
                    count += 1
                elif key == 'N':
                    number = val
                    count += 1
                else:
                    print('Found unrecognized channel property "{0}"'.format(key))
            if count < 9:
                print('WARNING: Some channel properties left at default values.')
        return name, openlife, closedlife, gatingCharges, delta, membraneVoltage, number, Erev, gamma
        
    def computeCurrentTS(self, time, dt, temp):
        '''This function is set up to be called from outside (i.e., from a Membrane
        object that contains this channel object). It takes time (total duration
        of the recording), dt (the size of the time step), and temp (temperature in K).
            It utilizes compute_voltage_dependence to get the channel's open
        and closed lifetimes at the object's Vm, channelSummer to get the number
        of channels open in each bin (which should be of width dt), and
        currentFromTimeSeries_oneVm to find the current being passed by
        these channels in each bin (still of width dt).
            This function will return a vector with the current being passed
        by the channels in each bin of dt, with the first bin corresponding to
        time 0 to dt, the second bin corresponding to time dt to 2*dt, etc.
        
        NOTE: NEED TO MODIFY channelSummer TO TAKE dt'''
        # call Uday/Kim to get lifetime open and closed
        lifeo_Vm, lifec_Vm = compute_voltage_dependence(self.lifeo, self.lifec, self.zg, temp, self.d, self.Vm)
        
        # call Andrew to get the time series
        numChannel_TS = channelSummer(time, self.N, self.lifeo, self.lifec)        
        
        # call Olivia to get the current
        current_TS = currentFromTimeSeries_oneVm(numChannel_TS, self.gamma, self.Vm, self.E0)
        
        return current_TS
    