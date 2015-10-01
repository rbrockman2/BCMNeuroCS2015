# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:33:53 2015

@author: Kimberly, Uday
"""
from math import exp
import unittest

#compute voltage dependent lifetime
#inputs: lambda open 0, lambda closed 0, Zg, T, delta, Vm
#outputs: lambda open Vm, lambda closed Vm

def compute_voltage_dependence(debug = False, lo0=1, lc0=1, zg=1, T=295, delta=0.5, Vm=0):
    if debug is False:    
        lo0 = float(input("Enter the open lifetime at 0 mV, in msec: "))
        lc0 = float(input("Enter the closed lifetime at 0 mV, in msec: "))
        zg = float(input("Enter the number of gating charges (Zg): "))
        T = float(input("Enter the temperature, in Kelvin: "))
        delta = float(input("Enter the gating delta: "))
        Vm = float(input("Enter the Vm for the voltage clamp, in mV: "))
    F = 1E5
    R = 8.3
    loVm = lo0 * exp((delta*zg*F*(Vm/1000))/(R*T))
    lcVm = lc0 * exp(((1-delta)*-1*zg*F*(Vm/1000))/(R*T))
    return loVm, lcVm

class TestVoltageDependence(unittest.TestCase):    
    def test_at_0mV(self):
        loVm, lcVm = compute_voltage_dependence(debug=1, 1, 1, 1, 295, 0.5, 0)        
                
        print("Open lifetime is", loVm, "Closed lifetime is", lcVm)
        
#if debug:
#    test_compute_voltage_dependence()