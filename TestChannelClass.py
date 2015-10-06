# -*- coding: utf-8 -*-
from ChannelClass import Channel
import unittest


class TestComputeCurrentTS(unittest.TestCase):
    def setUp(self):
        myDict = {'name': 'Na', 'lifeo': 10, 'lifec': 30,
                  'zg': 0, 'd': 0.5, 'N': 100,
                  'gamma': 10e-9, 'E0': 60}
        self.channel = Channel(**myDict)

    def test_no_driving(self):
        current_TS = self.channel.compute_current_TS(60, 100, 0.01, 300)
        mean_current_TS = sum(current_TS) / float(len(current_TS))
        self.assertEqual(len(current_TS), 10000)
        self.assertEqual(mean_current_TS, 0)

    def test_minus_100mV_driving(self):
        current_TS = self.channel.compute_current_TS(-40, 10000, 0.01, 300)
        mean_current_TS = sum(current_TS) / float(len(current_TS))
        self.assertEqual(len(current_TS), 1000000)
        self.assertAlmostEqual(mean_current_TS, -2.5e-8, 8)

    def test_single_channel(self):
        self.channel.N = 1
        current_TS = self.channel.compute_current_TS(-40, 10000, 0.01, 300)
        mean_current_TS = sum(current_TS) / float(len(current_TS))
        self.assertEqual(len(current_TS), 1000000)
        self.assertAlmostEqual(mean_current_TS, -2.5e-10, 10)

    def test_two_channels(self):
        self.channel.N = 2
        current_TS = self.channel.compute_current_TS(-40, 10000, 0.01, 300)
        mean_current_TS = sum(current_TS) / float(len(current_TS))
        self.assertEqual(len(current_TS), 1000000)
        self.assertAlmostEqual(mean_current_TS, -5.0e-10, 10)

    def test_voltage_dependence(self):
        self.channel.zg = 4
        self.channel.d = 0.8
        Vm = -40
        #  k+ = k+_0*exp(4*96485*(-40/1000)*0.2/(8.314*300))
        #  lifec = lifec * exp(-(4*96485*(-40/1000)*0.2/(8.314*300)))
        #        = lifec * 3.448 = 103.449
        #  k- = k- *exp(4*96485*(-40/1000)*-0.8/(8.314*300))
        #  lifeo = lifeo *exp(-(4*96485*(-40/1000)*-0.8/(8.314*300)))
        #        = lifeo * 7.0727 * 10^-3 = 0.070727
        #  I = (Vm-Ex)*gamma*N*(lifeo/(lifec+lifeo))
        #  I = (-0.1)*10E-9*100*(0.070727 / (103.449 + 0.070727)) = 6.8322E-11
        print(self.channel.compute_voltage_dependence(300, -40))
        current_TS = self.channel.compute_current_TS(Vm, 10000, 0.01, 300)
        mean_current_TS = sum(current_TS) / float(len(current_TS))
        self.assertAlmostEqual(mean_current_TS, -6.83e-7, 4)


class TestVoltageDependence(unittest.TestCase):
    def setUp(self):
        myDict = {'name': 'test', 'lifeo': 1, 'lifec': 1,
                  'zg': 1, 'd': 0.5, 'N': 1,
                  'gamma': 10e-9, 'E0': 0}
        self.standard_channel = Channel(**myDict)

        myDict = {'name': 'test', 'lifeo': 1, 'lifec': 1,
                  'zg': 1, 'd': 0, 'N': 1,
                  'gamma': 10e-9, 'E0': 0}
        self.zero_delta_channel = Channel(**myDict)

        myDict = {'name': 'test', 'lifeo': 1, 'lifec': 1,
                  'zg': 0, 'd': 0.5, 'N': 1,
                  'gamma': 10e-9, 'E0': 0}
        self.zero_valence_channel = Channel(**myDict)

    def test_at_0mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 0)
        self.assertAlmostEqual(loVm, 1, places=5)
        self.assertAlmostEqual(lcVm, 1, places=5)

    def test_at_0delta(self):
        loVm, lcVm = self.zero_delta_channel.compute_voltage_dependence(295,
                                                                        -70)
        self.assertAlmostEqual(loVm, 1, places=5)
        self.assertAlmostEqual(lcVm, 15.70153, places=5)

    def test_at_0valence(self):
        loVm, lcVm = self.zero_valence_channel.compute_voltage_dependence(295,
                                                                          -70)
        self.assertAlmostEqual(loVm, 1, places=5)
        self.assertAlmostEqual(lcVm, 1, places=5)

    def test_at_neg70mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, -70)
        self.assertAlmostEqual(loVm, 0.25236, places=5)
        self.assertAlmostEqual(lcVm, 3.96252, places=5)

    def test_at_neg80mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, -80)
        self.assertAlmostEqual(loVm, 0.20730, places=5)
        self.assertAlmostEqual(lcVm, 4.82387, places=5)

    def test_at_neg90mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, -90)
        self.assertAlmostEqual(loVm, 0.17029, places=5)
        self.assertAlmostEqual(lcVm, 5.87246, places=5)

    def test_at_70mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 70)
        self.assertAlmostEqual(loVm, 3.96252, places=5)
        self.assertAlmostEqual(lcVm, 0.25236, places=5)

    def test_at_80mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 80)
        self.assertAlmostEqual(loVm, 4.82387, places=5)
        self.assertAlmostEqual(lcVm, 0.20730, places=5)

    def test_at_90mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 90)
        self.assertAlmostEqual(loVm, 5.87246, places=5)
        self.assertAlmostEqual(lcVm, 0.17029, places=5)


class TestOpenChannelTS(unittest.TestCase):
    def test_zero_channels(self):
        self.assertEqual(Channel.open_channel_TS(1, 0.1, 0, 1, 1), [])
        self.assertEqual(Channel.open_channel_TS(0, 0.1, 0, 1, 1), [])

    def test_one_channel(self):
        self.assertEqual(Channel.open_channel_TS(1, 1, 1, 1, 0), [1])
        self.assertEqual(Channel.open_channel_TS(1, 1, 1, 0, 1), [0])
        self.assertEqual(Channel.open_channel_TS(1, 0.5, 1, 1, 0), [1, 1])
        self.assertEqual(Channel.open_channel_TS(0, 0.5, 1, 1, 0), [])
        self.assertEqual(Channel.open_channel_TS(1, 0.5, 1, 0, 1), [0, 0])

    def test_two_channel(self):
        self.assertEqual(Channel.open_channel_TS(1, 1, 2, 1, 0), [2])
        self.assertEqual(Channel.open_channel_TS(1, 1, 2, 0, 1), [0])
        self.assertEqual(Channel.open_channel_TS(1, 0.5, 2, 1, 0), [2, 2])
        self.assertEqual(Channel.open_channel_TS(0, 0.5, 2, 1, 0), [])
        self.assertEqual(Channel.open_channel_TS(1, 0.5, 2, 0, 1), [0, 0])

    def test_100_channel(self):
        self.assertEqual(Channel.open_channel_TS(1, 1, 100, 1, 0), [100])
        self.assertEqual(Channel.open_channel_TS(1, 1, 100, 0, 1), [0])
        self.assertEqual(Channel.open_channel_TS(1, 0.5, 100, 1, 0),
                         [100, 100])
        self.assertEqual(Channel.open_channel_TS(0, 0.5, 100, 1, 0), [])
        self.assertEqual(Channel.open_channel_TS(1, 0.5, 100, 0, 1), [0, 0])


class TestCurrentFromTimeSeries_oneVm(unittest.TestCase):
    def testIfRuns(self):
        timeseries = [0 for i in range(0, 1000)]
        gamma = 0
        Vm = 0
        Ex = 0
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries,
                                                                gamma, Vm, Ex)
        self.assertEqual(sum(currentTimeSeries), 0)

    def testDrivingForce(self):
        timeseries = [1 for i in range(0, 1000)]
        gamma = 1
        Vm = 20
        Ex = 20
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries,
                                                                gamma, Vm, Ex)
        self.assertEqual(sum(currentTimeSeries), 0)

        timeseries = [1 for i in range(0, 1000)]
        gamma = 1
        Vm = 20
        Ex = 10
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries,
                                                                gamma, Vm, Ex)
        self.assertAlmostEqual(.010 * len(timeseries), sum(currentTimeSeries))

    def testGamma(self):
        timeseries = [1 for i in range(0, 1000)]
        gamma = 0.5
        Vm = 20
        Ex = 19
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries,
                                                                gamma, Vm, Ex)
        self.assertAlmostEqual(gamma*0.001*len(timeseries),
                               sum(currentTimeSeries))

"""Unit Testing."""
if __name__ == '__main__':
    unittest.main()
