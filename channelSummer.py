from Noisless_Channel import noiseless_channel
import numpy as np
import operator

def channelSummer(totalTime, nChannels, lifetimeOpenVm, lifetimeClosedVm):
        # this will be received from somewhere else, eventually. whoever calls it.
        bigSeries = []
        for i in range(nChannels):
            timeSeries = noiseless_channel(lifetimeOpenVm, lifetimeClosedVm, totalTime)
            print(len(timeSeries))
            bigSeries = [x + y for x, y in zip(bigSeries, timeSeries)]
            type(timeSeries)
            if i>0:
                bigSeries = np.add(bigSeries, timeSeries)
            else:
                bigSeries = timeSeries
        return bigSeries
    
    
if __name__ == "__main__": 
    bigSeries = channelSummer(1000, 10, 100, 100)
    