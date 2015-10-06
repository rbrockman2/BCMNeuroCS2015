# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 2015

@author: The Entire First Year Neuroscience Graduate Student Contingent
    (plus Elizabeth Lackey from second year, of course)

BCM Computation for Neuroscience Fall 2015

Final Group Assignment
"""
import unittest
from MembraneClass import Membrane
from ChannelClass import Channel
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


class TestComputeCurrent(unittest.TestCase):
    def setUp(self):
        self.m = Membrane()
        self.m.dt = 1
        self.m.simulation_time = 3
        self.m.Vm = 0

    def test_single_channel(self):
        channel_1_dict = {'name': 'ch1', 'lifeo': 1, 'lifec': 0,
                          'zg': 0, 'd': 0.5, 'N': 1,
                          'gamma': 1, 'E0': 1000}
        channel1 = Channel(**channel_1_dict)
        channel_set_dict = {channel1.name: channel1}
        self.m.create_channel_set(**channel_set_dict)
        self.assertEqual(self.m.compute_current(), [-1, -1, -1])

    def test_multiple_channels_same_type(self):
        channel_1_dict = {'name': 'ch1', 'lifeo': 1, 'lifec': 0,
                          'zg': 0, 'd': 0.5, 'N': 4,
                          'gamma': 1, 'E0': 1000}
        channel1 = Channel(**channel_1_dict)
        channel_set_dict = {channel1.name: channel1}
        self.m.create_channel_set(**channel_set_dict)
        self.assertEqual(self.m.compute_current(), [-4, -4, -4])

    def test_two_channel_types(self):
        channel_1_dict = {'name': 'ch1', 'lifeo': 1, 'lifec': 0,
                          'zg': 0, 'd': 0.5, 'N': 2,
                          'gamma': 1, 'E0': 1000}
        channel_2_dict = {'name': 'ch2', 'lifeo': 1, 'lifec': 0,
                          'zg': 0, 'd': 0.5, 'N': 3,
                          'gamma': 1, 'E0': 1000}
        channel1 = Channel(**channel_1_dict)
        channel2 = Channel(**channel_2_dict)
        channel_set_dict = {channel1.name: channel1, channel2.name: channel2}
        self.m.create_channel_set(**channel_set_dict)
        self.assertEqual(self.m.compute_current(), [-5, -5, -5])


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
        chanDict = {channel1.name: channel1, channel2.name: channel2}
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
        chanDict = {channel1.name: channel1, channel2.name: channel2}
        m = Membrane()
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
        chanDict = {channel1.name: channel1, channel2.name: channel2}
        m = Membrane()
        m.create_channel_set(**chanDict)
        m.make_plot()  # Check if graph yields sensible results.
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
