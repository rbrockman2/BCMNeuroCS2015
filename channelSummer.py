import Noiseless_Channel


def channelSummer(totalTime, nChannels, lifetimeOpenVm, lifetimeClosedVm):
        # this will be received from somewhere else, eventually. whoever calls it.
        bigSeries = []
        for i in range(nChannels):
            timeSeries = Noiseless_Channel(lifetimeOpenVm, lifetimeClosedVm, totalTime)
            bigSeries = bigSeries + timeSeries
        return bigSeries
    
    
if __name__ == "__main__": 
    channelSummer(1000, 1000, 100, 100)
    