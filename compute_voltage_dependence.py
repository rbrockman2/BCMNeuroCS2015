# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:33:53 2015

@author: Kimberly, Uday

Function: compute voltage dependent lifetime and test
Inputs:   lambda open 0, lambda closed 0, Zg, T, delta, Vm
Outputs:  lambda open Vm, lambda closed Vm
"""
from math import exp
import unittest



def compute_voltage_dependence(debug = False, lo0=1, lc0=1, zg=1, T=295, delta=0.5, Vm=0):
    F = 1E5
    R = 8.3
    loVm = lo0 * exp((delta*zg*F*(Vm/1000))/(R*T))
    lcVm = lc0 * exp(((1-delta)*-1*zg*F*(Vm/1000))/(R*T))
    return loVm, lcVm

class TestVoltageDependence(unittest.TestCase):    
    def test_at_0mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, 0)        
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 1, places = 5)
    def test_at_0delta(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0, -70)        
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 17.44221, places = 5)
    def test_at_0valence(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 0, 295, 0.5, -70)        
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 1, places = 5)
    def test_at_neg70mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, -70)        
        self.assertAlmostEqual(loVm, 0.23944, places = 5)        
        self.assertAlmostEqual(lcVm, 4.17639, places = 5)
    def test_at_neg80mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, -80)        
        self.assertAlmostEqual(loVm, 0.19522, places = 5)        
        self.assertAlmostEqual(lcVm, 5.12255, places = 5)
    def test_at_neg90mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, -90)        
        self.assertAlmostEqual(loVm, 0.15916, places = 5)        
        self.assertAlmostEqual(lcVm, 6.28308, places = 5)
    def test_at_70mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, 70)        
        self.assertAlmostEqual(loVm, 4.17639, places = 5)        
        self.assertAlmostEqual(lcVm, 0.23944, places = 5)
    def test_at_80mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, 80)
        self.assertAlmostEqual(loVm, 5.12255, places = 5)        
        self.assertAlmostEqual(lcVm, 0.19522, places = 5)
    def test_at_90mV(self):
        loVm, lcVm = compute_voltage_dependence(True, 1, 1, 1, 295, 0.5, 90)
        self.assertAlmostEqual(loVm, 6.28308, places = 5)        
        self.assertAlmostEqual(lcVm, 0.15916, places = 5)

if __name__ == '__main__':
    unittest.main()
        
#if debug:
#    test_compute_voltage_dependence()