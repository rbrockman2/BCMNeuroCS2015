# -*- coding: utf-8 -*-
from RandomSwitchClass import RandomSwitch
import unittest


class TestRandomSwitch(unittest.TestCase):
    def setUp(self):
        self.defaultSwitch = RandomSwitch()
        self.configuredSwitch = RandomSwitch(10, 3)
        self.openSwitch = RandomSwitch(1, 0)
        self.closedSwitch = RandomSwitch(0, 1)

    def testDumbInput(self):
        self.idiotSwitch = RandomSwitch(0, 0)
        self.idiotSwitch = RandomSwitch(-4, 0)
        self.idiotSwitch = RandomSwitch(0, 4)
        self.assertEqual(self.openSwitch.run_switch(0.01, 0), [1])

    def testStuckSwitch(self):
        self.assertEqual(self.openSwitch.run_switch(1, 1), [1])
        self.assertEqual(self.closedSwitch.run_switch(1, 1), [0])
        self.assertEqual(self.openSwitch.run_switch(1, 1.1), [])
        self.assertEqual(self.closedSwitch.run_switch(1, 1.1), [])
        self.assertEqual(self.openSwitch.run_switch(1, 0.9), [1])
        self.assertEqual(self.closedSwitch.run_switch(1, 0.9), [0])
        self.assertEqual(self.openSwitch.run_switch(1, 0.5), [1, 1])
        self.assertEqual(self.closedSwitch.run_switch(1, 0.5), [0, 0])

    def testBigStuckSwitch(self):
        bigOpenRun = self.openSwitch.run_switch(1E3, 0.1)
        bigOpenRunMean = sum(bigOpenRun)/float(len(bigOpenRun))
        self.assertAlmostEqual(bigOpenRunMean, 1, 5)
        self.assertEqual(len(bigOpenRun), 1E4)

        bigClosedRun = self.closedSwitch.run_switch(1E3, 0.1)
        bigClosedRunMean = sum(bigClosedRun)/float(len(bigClosedRun))
        self.assertAlmostEqual(bigClosedRunMean, 0, 5)
        self.assertEqual(len(bigClosedRun), 1E4)

    def testDefaultSwitch(self):
        bigDefaultRun = self.defaultSwitch.run_switch(1E4, 0.1)
        bigDefaultRunMean = sum(bigDefaultRun)/float(len(bigDefaultRun))
        self.assertAlmostEqual(bigDefaultRunMean, 2/5, 1)
        self.assertEqual(len(bigDefaultRun), 1E5)

    def testConfiguredSwitch(self):
        bigConfiguredRun = self.configuredSwitch.run_switch(1E4, 0.1)
        bigConfiguredRunMean = sum(bigConfiguredRun) / \
            float(len(bigConfiguredRun))
        self.assertAlmostEqual(bigConfiguredRunMean, 10/13, 1)
        self.assertEqual(len(bigConfiguredRun), 1E5)


"""Unit Testing."""
if __name__ == '__main__':
    unittest.main()
