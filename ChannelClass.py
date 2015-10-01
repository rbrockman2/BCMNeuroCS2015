# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 20:40:30 2015

@author: Olivia
"""

from compute_voltage_dependence import compute_voltage_dependence
from channelSummer import channelSummer
from currentFromTimeSeries_oneVm import currentFromTimeSeries_oneVm

class Channel():
    def __init__(self):
        '''Creates an instance of the channel class with properties:
            lifeo   lifetime open in ms
            lifec   lifetime closed in ms
            zg      gating charges
            d       delta
            Vm      voltage clamping channel to (mV)
            N       number of this kind of channel
            name    name of the channel'''
        # default everything to 0
        self.lifeo = 0
        self.lifec = 0
        self.zg = 0
        self.d = 1
        self.Vm = 0
        self.N = 1
        self.E0 = 0
        self.gamma = 0
        self.name = 'generic'
        ui_name, ui_lifeo, ui_lifec, ui_zg, ui_d, ui_Vm, ui_N, ui_E0, ui_gamma = self.getParams()
        self.lifeo = ui_lifeo
        self.lifec = ui_lifec
        self.zg = ui_zg
        self.d = ui_d
        self.Vm = ui_Vm
        self.N = ui_N
        self.name = ui_name
        self.E0 = ui_E0
        self.gamma = ui_gamma
    
    def getParams(self):
        '''Asks the user to describe the channel.'''
        name = input("What is this channel's name?: ")
        Erev = input("What is this channel's 0-current potential?: ")
        openlife = input("What is this channel's open lifetime (msec)?: ")
        closedlife = input("What is this channel's closed lifetime (msec)?: ")
        gamma = input("What is the single-channel conductance?: ")
        gatingCharges = input("How many gating charges does this channel have?: ")
        delta = input("What is delta for this channel's gating charge?: ")
        membraneVoltage = input("At what voltage would you like to clamp this channel (mV)?: ")
        number = input("How many of these channels are there?: ")
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
        lifeo_Vm, lifec_Vm = compute_voltage_dependence(False, self.lifeo, self.lifec, self.zg, temp, self.d, self.Vm)
        
        # call Andrew to get the time series
        numChannel_TS = channelSummer(time, self.N, self.lifeo, self.lifec)        
        
        # call Olivia to get the current
        current_TS = currentFromTimeSeries_oneVm(numChannel_TS, self.gamma, self.Vm, self.Ex)
        
        return current_TS
    