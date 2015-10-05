# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 00:58:24 2015

@author: robert
"""

from MembraneClass import Membrane
from ChannelClass import Channel
import unittest

class TestMembraneClass(unittest.TestCase):
    def testIfGoes(self):
        myDict = {'name': 'test', 'lifeo': 10, 'lifec': 20,
                              'zg': 1, 'd': 0.8, 'Vm': -65, 'N': 100,
                              'gamma': 10e-9, 'E0': 0}
        myDict2 = {'name': 'test', 'lifeo': 1, 'lifec': 3,
                              'zg': 1, 'd': 0.8, 'Vm': -65, 'N': 100,
                              'gamma': 10e-9, 'E0': 0}
        channel1 = Channel(**myDict)
        channel2 = Channel(**myDict2)
        chanDict = {channel1.name:channel1, channel2.name:channel2}
        m = Membrane()
        m.get_membrane_parameters()
        m.create_channel_set(**chanDict)
        m.makePlot()
        self.AssertsEquals(1, 1)