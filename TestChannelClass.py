            
from ChannelClass import Channel
import unittest


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
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 1, places = 5)
    def test_at_0delta(self): 
        loVm, lcVm = self.zero_delta_channel.compute_voltage_dependence(295, 
                                                                        -70)       
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 17.44221, places = 5)
    def test_at_0valence(self):   
        loVm, lcVm = self.zero_valence_channel.compute_voltage_dependence(295, 
                                                                          -70)                
        self.assertAlmostEqual(loVm, 1, places = 5)        
        self.assertAlmostEqual(lcVm, 1, places = 5)
    def test_at_neg70mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, -70)         
        self.assertAlmostEqual(loVm, 0.23944, places = 5)        
        self.assertAlmostEqual(lcVm, 4.17639, places = 5)
    def test_at_neg80mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, -80)             
        self.assertAlmostEqual(loVm, 0.19522, places = 5)        
        self.assertAlmostEqual(lcVm, 5.12255, places = 5)
    def test_at_neg90mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, -90)             
        self.assertAlmostEqual(loVm, 0.15916, places = 5)        
        self.assertAlmostEqual(lcVm, 6.28308, places = 5)
    def test_at_70mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 70)             
        self.assertAlmostEqual(loVm, 4.17639, places = 5)        
        self.assertAlmostEqual(lcVm, 0.23944, places = 5)
    def test_at_80mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 80)    
        self.assertAlmostEqual(loVm, 5.12255, places = 5)        
        self.assertAlmostEqual(lcVm, 0.19522, places = 5)
    def test_at_90mV(self):
        loVm, lcVm = self.standard_channel.compute_voltage_dependence(295, 90)    
        self.assertAlmostEqual(loVm, 6.28308, places = 5)        
        self.assertAlmostEqual(lcVm, 0.15916, places = 5)
        
        
class TestCurrentFromTimeSeries_oneVm(unittest.TestCase):
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
        
        
class TestOpenChannelTS(unittest.TestCase):
    def test_zero_channels(self):
        self.assertEqual(Channel.open_channel_TS(1,0.1,0,1,1),[])
        self.assertEqual(Channel.open_channel_TS(0,0.1,0,1,1),[])
    
    def test_one_channel(self):
        self.assertEqual(Channel.open_channel_TS(1,1,1,1,0),[1])
        self.assertEqual(Channel.open_channel_TS(1,1,1,0,1),[0])
        self.assertEqual(Channel.open_channel_TS(1,0.5,1,1,0),[1,1])
        self.assertEqual(Channel.open_channel_TS(0,0.5,1,1,0),[])
        self.assertEqual(Channel.open_channel_TS(1,0.5,1,0,1),[0,0])
        
    def test_two_channel(self):
        self.assertEqual(Channel.open_channel_TS(1,1,2,1,0),[2])
        self.assertEqual(Channel.open_channel_TS(1,1,2,0,1),[0])
        self.assertEqual(Channel.open_channel_TS(1,0.5,2,1,0),[2,2])
        self.assertEqual(Channel.open_channel_TS(0,0.5,2,1,0),[])
        self.assertEqual(Channel.open_channel_TS(1,0.5,2,0,1),[0,0])
        
    def test_100_channel(self):
        self.assertEqual(Channel.open_channel_TS(1,1,100,1,0),[100])
        self.assertEqual(Channel.open_channel_TS(1,1,100,0,1),[0])
        self.assertEqual(Channel.open_channel_TS(1,0.5,100,1,0),[100,100])
        self.assertEqual(Channel.open_channel_TS(0,0.5,100,1,0),[])
        self.assertEqual(Channel.open_channel_TS(1,0.5,100,0,1),[0,0])
        
    
        
        

"""Unit Testing."""
if __name__ == '__main__':
    unittest.main()
 