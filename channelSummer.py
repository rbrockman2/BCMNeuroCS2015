
def channelSummer(totalTime, nChannels, lifetimeOpenVm, lifetimeClosedVm):
	# this will be received from somewhere else, eventually. whoever calls it.

	bigTime = []
	for i in nChannels:
    	timeSeries = MysteryProgram(lifetimeOpenMs, lifetimeClosedMs, totalTime)
    	bigSeries = bigSeries + timeSeries

    return bigSeries