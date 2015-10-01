# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:33:53 2015

@author: Kimberly, Uday
"""
import math
debug = True

#compute voltage dependent lifetime
#inputs: lambda open 0, lambda closed 0, Zg, T, delta, Vm
#outputs: lambda open Vm, lambda closed Vm

def compute_voltage_dependence():
    lo0 = input("Enter the open lifetime at 0 mV, in msec: ")
    lc0 = input("Enter the closed lifetime at 0 mV, in msec: ")
    zg = input("Enter the number of gating charges (Zg): ")
    T = input("Enter the temperature, in Kelvin: ")
    delta = input("Enter the gating delta: ")
    Vm = input("Enter the Vm for the voltage clamp, in mV: ")
    F = 10^5
    R = 8.3
    loVm = lo0 * exp((delta*zg*F*(Vm/1000))/(R*T))
    lcVm = lc0 * exp(((1 - delta)*-1*zg*F*(Vm/1000))/(R*T))
    return loVm, lcVm