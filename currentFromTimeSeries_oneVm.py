# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:16:54 2015

@author: Olivia
"""

'''Take in time series with N channels active in a time bin, single-channel
conductance, Vm being clamped to, Ex'''

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
    current_series  the current in each time bin'''
    
    Vm_inV = float(Vm * 10**-3)
    Ex_inV = float(Ex * 10**-3)
    print(len(timeseries))
    #if len(timeseries) > 1:
    current_series = [N * gamma * (Vm_inV - Ex_inV) for N in timeseries]
    #else:
    #current_series = timeseries * gamma * (Vm_inV - Ex_inV)
    return current_series
