# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:41:51 2015

@author: Olivia
"""

import unittest
from currentFromTimeSeries_oneVm import currentFromTimeSeries_oneVm

class testCurrentFromTimeSeries_oneVm(unittest.TestCase):

    def testIfRuns(self):
        timeseries = [0 for i in range(0, 1000)]
        gamma = 0
        Vm = 0
        Ex = 0
        currentTimeSeries = currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertEqual(sum(currentTimeSeries), 0)

    def testDrivingForce(self):
        timeseries = [1 for i in range(0, 1000)]
        gamma = 1
        Vm = 20
        Ex = 20
        currentTimeSeries = currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertEqual(sum(currentTimeSeries), 0)
        
        timeseries = [1 for i in range(0, 1000)]
        gamma = 1
        Vm = 20
        Ex = 10
        currentTimeSeries = currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertAlmostEqual(.010 * len(timeseries), sum(currentTimeSeries))
    
    def testGamma(self):
        timeseries = [1 for i in range(0, 1000)]
        gamma = 0.5
        Vm = 20
        Ex = 19
        currentTimeSeries = currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertAlmostEqual(gamma*0.001*len(timeseries), sum(currentTimeSeries))
        

if __name__ == '__main__':
    unittest.main()
    

