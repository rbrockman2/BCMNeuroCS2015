            
from ChannelClass import Channel
import unittest

class TestVoltageDependence(unittest.TestCase):    
    def test_at_0mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, 0)        
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 1, places = 5)
    def test_at_0delta(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0, -70)        
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 17.44221, places = 5)
    def test_at_0valence(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 0, 295, 0.5, -70)        
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 1, places = 5)
    def test_at_neg70mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, -70)        
        self.assertAlmostEqual(loVm, 0.23944, places = 5)        
        self.assertAlmostEqual(lcVm, 4.17639, places = 5)
    def test_at_neg80mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, -80)        
        self.assertAlmostEqual(loVm, 0.19522, places = 5)        
        self.assertAlmostEqual(lcVm, 5.12255, places = 5)
    def test_at_neg90mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, -90)        
        self.assertAlmostEqual(loVm, 0.15916, places = 5)        
        self.assertAlmostEqual(lcVm, 6.28308, places = 5)
    def test_at_70mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, 70)        
        self.assertAlmostEqual(loVm, 4.17639, places = 5)        
        self.assertAlmostEqual(lcVm, 0.23944, places = 5)
    def test_at_80mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, 80)
        self.assertAlmostEqual(loVm, 5.12255, places = 5)        
        self.assertAlmostEqual(lcVm, 0.19522, places = 5)
    def test_at_90mV(self):
        loVm, lcVm = Channel.compute_voltage_dependence(1, 1, 1, 295, 0.5, 90)
        self.assertAlmostEqual(loVm, 6.28308, places = 5)        
        self.assertAlmostEqual(lcVm, 0.15916, places = 5)
        
        
class testCurrentFromTimeSeries_oneVm(unittest.TestCase):
    def testIfRuns(self):
        timeseries = [0 for i in range(0, 1000)]
        gamma = 0
        Vm = 0
        Ex = 0
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertEqual(sum(currentTimeSeries), 0)

    def testDrivingForce(self):
        timeseries = [1 for i in range(0, 1000)]
        gamma = 1
        Vm = 20
        Ex = 20
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertEqual(sum(currentTimeSeries), 0)
        
        timeseries = [1 for i in range(0, 1000)]
        gamma = 1
        Vm = 20
        Ex = 10
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertAlmostEqual(.010 * len(timeseries), sum(currentTimeSeries))
    
    def testGamma(self):
        timeseries = [1 for i in range(0, 1000)]
        gamma = 0.5
        Vm = 20
        Ex = 19
        currentTimeSeries = Channel.currentFromTimeSeries_oneVm(timeseries, gamma, Vm, Ex)
        self.assertAlmostEqual(gamma*0.001*len(timeseries), sum(currentTimeSeries))
        

"""Unit Testing."""
if __name__ == '__main__':
    unittest.main()
 