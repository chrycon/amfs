import sys,time,json,librosa,msaf
from performanceGeneration import *

startTime=time.clock()
audio_file = sys.argv[1]
print("Getting performance data...")
performanceData=getPerformanceData(audio_file)
segments = segmentData(performanceData)
performance = initialise(performanceData["duration"]+10)
print("Generating performance...")
generatePerformance(performance,performanceData,segments)
with open('../MusicalFountainSimulator/Assets/Resources/performance.json', 'w') as outfile:
    json.dump(performance, outfile)
print("Performance generated in: "+str(round((time.clock() - startTime),1))+" seconds.")
