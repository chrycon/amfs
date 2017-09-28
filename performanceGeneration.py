import sys,json,random,librosa,msaf
from setup import *
from scenarios import *
from behaviour import *
from emotionRetrieval import *

# Set the starting dictionary for the performance on which we will be working
def initialise(totalIntervals):
    performance={"intervals":[]}
    for i in range(totalIntervals):
        interval={}
        interval["intervalNo"]=i
        interval["jetStates"]=[]
        for j in range(77):
            jetState={}
            jetState["jetNo"]=j
            jetState["velocity"]=0
            jetState["lightColor"]={"r":1.0,"g":1.0,"b":1.0,"a":1.0}
            jetState["lightIntensity"]=0
            interval["jetStates"].append(jetState)
        performance["intervals"].append(interval)
    return performance


# Bring the segment boundaries to a good condition for the performance by
# removing performance-wise redundant boundaries
def cleanSegments(boundaries,songDuration):
    # The first boundary is always 0
    cleanBoundaries=[0]
    temp=[]
    for t in boundaries:
        # Only accept boundaries that don't occur in the first or last 6 seconds
        if(t>60 and t<songDuration-60):
            cleanBoundaries.append(t)
    # The last boundary is always equal to the song's duration
    cleanBoundaries.append(songDuration)
    return cleanBoundaries

# Performs analysis of the input audio file and produces the data
# necessary for the generation of the performance
def getPerformanceData(audioFile):
    # Load the audio file with a sampling rate of 44100 Hz
    x,fs=librosa.load(audioFile,sr=44100)
    print("File \'"+audioFile+"\' loaded.")
    # Calculate the duration of the audio file
    duration=int(10*librosa.get_duration(x,fs))
    # Calculate the emotion of the audio file and get the associated colors
    print("Calculating emotion data...")
    colors = groupColor(getVApair(audioFile))
    # Get the percussive elements of the of the audio file
    print("Extracting percussive elements...")
    xPercussive = librosa.effects.percussive(x, margin=3.0)
    #xPercussive=x
    # Get the beats of the audio file
    print("Detecting beats...")
    tempo,beats=librosa.beat.beat_track(xPercussive,sr=44100)
    beatSampleTimes = librosa.frames_to_time(beats,sr=fs)
    beatDsTimes=[int(10*round(b,1)) for b in beatSampleTimes]
    # Get the onsets of the audio file
    print("Detecting onsets...")
    onsets=librosa.onset.onset_detect(xPercussive,sr=44100)
    onsetSampleTimes = librosa.frames_to_time(onsets,sr=fs)
    onsetDsTimes=[int(10*round(o,1)) for o in onsetSampleTimes]
    # Get the segment boundaries
    print("Segmenting audio file...")
    boundaries, labels = msaf.process(audioFile,boundaries_id="sf")
    # Clean the boundaries to remove redundant segments
    boundariesDs=cleanSegments([int(10*round(f,1)) for f in boundaries],duration)
    # Store the results of the segmentation in segments.txt for faster retrieval
    # during later segmentations
    outFile = 'segments.txt'
    print('Saving output to %s' % outFile)
    msaf.io.write_mirex(boundaries, labels, outFile)
    # Return a dictionary of the relevant performance data
    performanceData={"colors":colors,"waveValues":x,"duration":duration,"beats":beatDsTimes,"onsets":onsetDsTimes,"boundaries":boundariesDs}
    return performanceData

# Breaks the data of the whole performance into segments corresponding to the
# segments extracted using 'msaf', so that each one can be individually passed
# to a scenario for production
def segmentData(performanceData):
    segments=[]
    # Get the relative amplitudes of the segments
    relativeAmplitudes = relativeAmplitudesOfSegments(performanceData["waveValues"],performanceData["boundaries"])
    # Sort the relative amplitudes and store them in a list
    sortedAmplitudes=sorted(relativeAmplitudes,reverse=True)
    # Calculate the relative(average) amplitude of the whole audio file
    relativeAmplitude=sum(relativeAmplitudes)/len(relativeAmplitudes)
    # For each consecutive pair of boundaries
    for i in range(0,len(performanceData["boundaries"])-1):
        # Get the start time, end time, beats and onsets occurring in the segment
        start = performanceData["boundaries"][i]
        end = performanceData["boundaries"][i+1]
        beats = [b for b in performanceData["beats"] if b>=start and b<end]
        onsets =  [o for o in performanceData["onsets"] if o>=start and o<end]
        segmentAmplitude=relativeAmplitudes[i]
        # Calculate the onset ratios of the segment
        onsetRatios=getOnsetRatios(performanceData,onsets,0.3,0.1)
        maxAmplitude=max(relativeAmplitudes)
        # Set a 'section' string variable and assign to it the type of segment
        # it is likely to be. The system currently only has sections for
        # intro, outro, chorus and verses.
        section=""
        if(i==0):
            section="intro"
        elif(i==len(performanceData["boundaries"])-2):
            section="outro"
        # We assign 'chorus' to the two segments with the highest segment amplitudes.
        elif(segmentAmplitude==sortedAmplitudes[0] or segmentAmplitude==sortedAmplitudes[1]):
            section="chorus"
        # Anything remaining that is not intro, outro or chorus, is a verse.
        else:
            section="verse"
        # Store the segment data into a dictionary and append it to the list of
        # segments. Return that list.
        segmentData={"start":start,"end":end,"duration":end-start,"beats":beats,"onsets":onsets,"onsetRatios":onsetRatios,
        "relativeAmplitude":relativeAmplitude,"maxAmplitude":maxAmplitude,"segmentAmplitude":segmentAmplitude,"section":section}
        segments.append(segmentData)
    return segments

# Generate the performance given a pre-initialised performance dictionary, the
# performance data and the segments.
def generatePerformance(performance,performanceData,segments):
    duration=performanceData["duration"]
    colors=performanceData["colors"]
    currentScenario=0
    # We set the color of the four units at the start of the performance and they
    # remain unchanged.
    constantColor(performance,0,duration,U1,colors["color1"])
    constantColor(performance,0,duration,U2,colors["color2"])
    constantColor(performance,0,duration,U3,colors["color1"])
    constantColor(performance,0,duration,U4,colors["color1"])
    # For each segment in turn, we perform the corresponding scenarios, depending
    # on whether they are an intro, an outro, a chorus or a verse.
    for segmentData in segments:
        if(segmentData["section"]=="intro"):
            currentScenario=scIntro(performance,segmentData)
        elif(segmentData["section"]=="outro"):
            currentScenario=scOutro(performance,segmentData)
        elif(segmentData["section"]=="chorus"):
            currentScenario=scChorus(performance,segmentData)
        else:
            # If the segment is a verse, choose a random verse scenario based on
            # the transition matrix defined in setup.py
            currentScenario=randomVerse(performance,segmentData,currentScenario)

# Get a random verse, based on the cumulative transition matrix calculated
# in setup.py
def randomVerse(performance,segmentData,currentScenario):
    # Get a random number from 0 to 1.
    rnd=random.random()
    for j in range(0,len(scenarios)):
        # Find out in which scenario the random number corresponds
        if(rnd<=CUM_TRANSITIONS[currentScenario][j]):
            nextScenario=scenarios[j](performance,segmentData)
            break
    return nextScenario

# Get the relative amplitudes of the segments in a list
def relativeAmplitudesOfSegments(waveValues,timestamps):
    frames=[int(t*44100.0/10.0) for t in timestamps]
    relativeAmplitudes=[]
    for i in range(0,len(frames)-1):
        amplitude=0
        frameStart = frames[i]
        frameEnd =  frames[i+1] if frames[i+1]<len(waveValues) else len(waveValues)-1
        for j in range(frameStart,frameEnd):
            amplitude+=abs(waveValues[j])
        segmentAmplitude=amplitude/(frameEnd-frameStart)
        relativeAmplitudes.append(segmentAmplitude)
    return relativeAmplitudes

# Get the onset ratios. The ratio is a comparison of the total amplitude after an
# onset to the total amplitude before the onset, depending on the limits specified.
# The upperLimit is the amount of a second to read wave values from, after the onset,
# and the lowerLimit is the amount of a second to read wave values from, before the onset.
# eg. upperLimit=0.3, lowerLimit=0.1, will compare 3 ds after the onset to 1 ds before
# the onset.
def getOnsetRatios(performanceData,onsets,upperLimit,lowerLimit):
    #onsets=performanceData["onsets"]
    onsetRatios=[]
    # Convert the times of the onsets from ds to samples times
    samples=[int(t*44100.0/10.0) for t in onsets]
    # For each onset, find its onset ratio
    for i in range(0,len(samples)):
        amplitudeFront=0
        amplitudeBack=0
        # The time at which the onset occurs
        sampleStart = samples[i]
        # Get the last sample within the upperLimit and before the end of the audio file
        if ( samples[i]+int(44100*upperLimit))<len(performanceData["waveValues"])-1:
            sampleFront = samples[i]+int(44100*upperLimit)
        else:
            sampleFront = len(performanceData["waveValues"])-1
        # Get the first sample within the lowerLimit and after the start of the audio file
        if ( samples[i]-int(44100*lowerLimit))>0:
            sampleBack = samples[i]-int(44100*lowerLimit)
        else:
            sampleBack = 0
        # Add up the absolute values of the amplitudes before and after the onset
        # and then divide to find the ratio.
        for j in range(sampleStart,sampleFront):
            amplitudeFront+=abs(performanceData["waveValues"][j])
        for k in range(sampleBack,sampleStart):
            amplitudeBack+=abs(performanceData["waveValues"][k])
        ratio=amplitudeFront/amplitudeBack
        onsetRatios.append(ratio)
    return onsetRatios
