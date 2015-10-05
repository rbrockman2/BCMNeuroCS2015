# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 00:57:57 2015

@author: robert
"""

from RandomSwitchClass import RandomSwitch
import unittest


class TestRandomSwitch(unittest.TestCase):
    def setUp(self):
        self.defaultSwitch = RandomSwitch()
        self.configuredSwitch = RandomSwitch(10, 3)
        self.openSwitch = RandomSwitch(1, 0)
        self.closedSwitch = RandomSwitch(0, 1)

    def testStuckSwitch(self):
        self.assertEqual(self.openSwitch.run_switch(1, 1), [1])
        self.assertEqual(self.closedSwitch.run_switch(1, 1), [0])
        self.assertEqual(self.openSwitch.run_switch(1, 1.1), [])
        self.assertEqual(self.closedSwitch.run_switch(1, 1.1), [])
        self.assertEqual(self.openSwitch.run_switch(1, 0.9), [1])
        self.assertEqual(self.closedSwitch.run_switch(1, 0.9), [0])
        self.assertEqual(self.openSwitch.run_switch(1, 0.5), [1, 1])
        self.assertEqual(self.closedSwitch.run_switch(1, 0.5), [0, 0])

    def testDefaultSwitch(self):
        bigDefaultRun = self.defaultSwitch.run_switch(1E6, 0.1)
        bigDefaultRunMean = sum(bigDefaultRun)/float(len(bigDefaultRun))
        self.assertAlmostEqual(bigDefaultRunMean, 2/5, 2)
        self.assertEqual(len(bigDefaultRun), 1E7)

    def testConfiguredSwitch(self):
        bigConfiguredRun = self.configuredSwitch.run_switch(1E6, 0.1)
        bigConfiguredRunMean = sum(bigConfiguredRun) / \
            float(len(bigConfiguredRun))
        self.assertAlmostEqual(bigConfiguredRunMean, 10/13, 2)
        self.assertEqual(len(bigConfiguredRun), 1E7)


"""Unit Testing."""
if __name__ == '__main__':
    unittest.main()
