# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 00:58:24 2015
@author: robert
"""

"""
lifeo is open lifetime at 0 mV, in msec
lifec is closed lifetime at 0 mV, in msec
zg is gating charge, an integer
d is delta
Vm is voltage across the membranem in mV
N is number of channels, an integer
gamma is the single channel conductance, in Siemens 
E0 is the channel's reversal potential, in mV
"""

from MembraneClass import Membrane
from ChannelClass import Channel
import unittest

class TestMembraneClass(unittest.TestCase):
    def testIfGoes(self):
        '''Does the program run without crashing?'''
        myDict = {'name': 'test', 'lifeo': 10, 'lifec': 20,
                              'zg': 1, 'd': 0.8, 'N': 100,
                              'gamma': 10e-9, 'E0': 0}
        myDict2 = {'name': 'test', 'lifeo': 1, 'lifec': 3,
                              'zg': 1, 'd': 0.8, 'N': 100,
                              'gamma': 10e-9, 'E0': 0}
        channel1 = Channel(**myDict)
        channel2 = Channel(**myDict2)
        chanDict = {channel1.name:channel1, channel2.name:channel2}
        m = Membrane()
        m.create_channel_set(**chanDict)
        m.compute_current()
        self.assertEqual(1, 1)
    def testIfZero(self):
        '''When gammas are 0 is total current 0?'''
        myDict = {'name': 'Na', 'lifeo': 10, 'lifec': 20,
                              'zg': 1, 'd': 0.8, 'N': 100,
                              'gamma': 0, 'E0': 60}
        myDict2 = {'name': 'K', 'lifeo': 1, 'lifec': 3,
                              'zg': 1, 'd': 0.8, 'N': 100,
                              'gamma': 0, 'E0': -85}
        channel1 = Channel(**myDict)
        channel2 = Channel(**myDict2)
        chanDict = {channel1.name:channel1, channel2.name:channel2}
        m = Membrane()
        #m.get_membrane_parameters()
        m.create_channel_set(**chanDict)
        timeseries = m.compute_current()
        ans = sum(timeseries)
        self.assertEqual(ans, 0)
    def testDifferentChannels(self):
        '''Does code accept mult. Vms?'''
        myDict = {'name': 'Na', 'lifeo': 3, 'lifec': 3,
                              'zg': 0, 'd': 0.5, 'N': 1,
                              'gamma': 15e-12, 'E0': 60}
        myDict2 = {'name': 'K', 'lifeo': 3, 'lifec': 3,
                              'zg': 0, 'd': 0.5, 'N': 1,
                              'gamma': 15e-12, 'E0': -85}
        channel1 = Channel(**myDict)
        channel2 = Channel(**myDict2)
        chanDict = {channel1.name:channel1, channel2.name:channel2}
        m = Membrane()
        m.create_channel_set(**chanDict)
        m.make_plot()
        self.assertEqual(1, 1)
        
        
if __name__ == "__main__":
    unittest.main()