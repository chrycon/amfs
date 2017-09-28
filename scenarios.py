from behaviour import *
from setup import *
# Get the velocities corresponding to the given segment based on the equation
# v=ce^2+v_min, where c is the coefficient of the fountain unit, as calculated
# using the f lambda function below, e is the relative amplitude of the
# segment and v_min is the minimum velocity of the fountain unit
def getQuadraticVelocities(segmentAmplitude,maxAmplitude):
    # First find the quadratic coefficients to be used for this segment
    f=lambda x: (MAX_VELOCITIES[x]-MIN_VELOCITIES[x])/pow(maxAmplitude,2)
    cs={"U1":f("U1"),"U2":f("U2"),"U3":f("U3"),"U4":f("U4")}
    # Construct a lambda function to calculate the quadratic velocities
    g=lambda x: (cs[x]*pow(segmentAmplitude,2)+MIN_VELOCITIES[x])
    # Calculate each velocity for each fountain unit separately
    v1=g("U1")
    v2=g("U2")
    v3=g("U3")
    v4=g("U4")
    return {"U1":v1,"U2":v2,"U3":v3,"U4":v4}

# Get the light intensities corresponding to the given segment based on the equation
# i=ce+i_min, where c is the coefficient of the fountain unit, as calculated
# using the f lambda function below, e is the relative amplitude of the
# segment and i_min is the minimum intensity of the fountain unit's lights
def getLinearIntensities(segmentAmplitude,maxAmplitude):
    # First find the quadratic coefficients to be used for this segment
    f=lambda x: (MAX_INTENSITIES[x]-MIN_INTENSITIES[x])/maxAmplitude
    cs={"U0":f("U0"),"U1":f("U1"),"U2":f("U2"),"U3":f("U3"),"U4":f("U4")}
    # Construct a lambda function to calculate the quadratic velocities
    g=lambda x: (cs[x]*segmentAmplitude+MIN_INTENSITIES[x])
    # Calculate each velocity for each fountain unit separately
    i0=g("U0")
    i1=g("U1")
    i2=g("U2")
    i3=g("U3")
    i4=g("U4")
    return {"U0":i0,"U1":i1,"U2":i2,"U3":i3,"U4":i4}


# The scenario assigned to the intro
def scIntro(performance,segmentData):
    start=segmentData["start"]
    end=segmentData["end"]
    maxAmplitude=segmentData["maxAmplitude"]
    segmentAmplitude=segmentData["segmentAmplitude"]
    relativeAmplitude=segmentData["relativeAmplitude"]
    onsets=segmentData["onsets"]
    onsetRatios=segmentData["onsetRatios"]
    beats=segmentData["beats"]
    # Sort the onset ratio pairs from highest to lowest, in order to get the
    # most significant ones
    onsetRatioPairsSorted=sorted([(onsetRatios[i],onsets[i]) for i in range(0,len(onsets))],reverse=True)
    # Get a significant onset in the range of 40 to 60 ds from the start of the segment
    onsetRatioPairsCropped=[(i,j) for (i,j) in onsetRatioPairsSorted if j>start+40 and j<start+60]
    if(len(onsetRatioPairsCropped)>0):
        onsetSignal=onsetRatioPairsCropped[0][1]
    else:
        onsetSignal=start+50
    # Get the quadratic velocities
    velocities=getQuadraticVelocities(segmentAmplitude,maxAmplitude)
    intensities=getLinearIntensities(segmentAmplitude,maxAmplitude)

    # The velocities to be used in this scenario
    v11=velocities["U1"]
    v12=velocities["U1"]*0.7
    v31=velocities["U3"]
    v32=velocities["U3"]*0.9
    v41=velocities["U4"]
    i01=intensities["U0"]
    # Start with a slow rise of U1,U3 and U4
    slowRising(performance,start,onsetSignal,U1,v11)
    slowRising(performance,start,onsetSignal,U3,v32)
    slowRising(performance,start,onsetSignal,U4,v41)
    # Continue with a wave and a beat-based move
    sineWave(performance,onsetSignal,end,U1,v12,v11)
    slowRisingOnBeatAlternating(performance,[b for b in beats if b>onsetSignal],U3,U4,v31,v32,3)
    slowIntensityChange(performance,start,onsetSignal,U0,i01)
    constantIntensity(performance,onsetSignal,end,U0,i01)

    return 0

# The scenario assigned to the outro
def scOutro(performance,segmentData):
    start=segmentData["start"]
    end=segmentData["end"]
    maxAmplitude=segmentData["maxAmplitude"]
    segmentAmplitude=segmentData["segmentAmplitude"]
    relativeAmplitude=segmentData["relativeAmplitude"]
    step=1 if segmentAmplitude>relativeAmplitude else 2
    beats=segmentData["beats"]
    onsets=segmentData["onsets"]
    onsetRatios=segmentData["onsetRatios"]
    # Sort the onset ratio pairs from highest to lowest, in order to get the
    # most significant ones
    onsetRatioPairsSorted=sorted([(onsetRatios[i],onsets[i]) for i in range(0,len(onsets))],reverse=True)
    # Get a significant onset in the range of 40 to 60 ds from the start of the segment
    onsetRatioPairsCropped_1=[(i,j) for (i,j) in onsetRatioPairsSorted if j>start+40 and j<start+60]
    if(len(onsetRatioPairsCropped_1)>0):
        onsetSignal_1=onsetRatioPairsCropped_1[0][1]
    else:
        onsetSignal_1=start+50
    # Get a significant onset in the range of 40 to 60 ds from the end of the segment
    onsetRatioPairsCropped_2=[(i,j) for (i,j) in onsetRatioPairsSorted if j>end-40 and j<end-20]
    if(len(onsetRatioPairsCropped_2)>0):
        onsetSignal_2=onsetRatioPairsCropped_2[0][1]
    else:
        onsetSignal_2=end-50
    # Get the quadratic velocities
    velocities=getQuadraticVelocities(segmentAmplitude,maxAmplitude)
    intensities=getLinearIntensities(segmentAmplitude,maxAmplitude)
    # The velocities to be used in this scenario
    v11=velocities["U1"]
    v12=velocities["U1"]*0.7
    v21=velocities["U2"]
    v22=velocities["U2"]*0.8
    v31=velocities["U3"]
    v41=velocities["U4"]
    i01=intensities["U0"]

    # Start with a constant wave of U1, a beat-based move of U2 and a slow rising
    # of U3 and U4
    constantWave(performance,start,end,U1,v11,0,1)
    slowRising(performance,start,onsetSignal_1,U3,v31)
    slowRisingOnBeat(performance,[b for b in beats if b<onsetSignal_2],U2,v22,v21,3)
    slowRising(performance,start,onsetSignal_1,U4,v41)
    # Set U3 and U4 to constant velocities until the second onset signal
    constantVelocity(performance,onsetSignal_1,onsetSignal_2,U3,v31)
    constantVelocity(performance,onsetSignal_1,onsetSignal_2,U4,v41)
    # End the scenario with a slow 'rising' to 0m/s of U2, U3 and U4
    slowRising(performance,onsetSignal_2,end,U2,0)
    slowRising(performance,onsetSignal_2,end,U3,0)
    slowRising(performance,onsetSignal_2,end,U4,0)
    slowIntensityChange(performance,start,onsetSignal_1,U0,i01)
    constantIntensity(performance,onsetSignal_1,onsetSignal_2,U0,i01)
    slowIntensityChange(performance,onsetSignal_2,end,U0,0)
    return 1

# The scenario assigned to a chorus
def scChorus(performance,segmentData):
    start=segmentData["start"]
    end=segmentData["end"]
    maxAmplitude=segmentData["maxAmplitude"]
    segmentAmplitude=segmentData["segmentAmplitude"]
    relativeAmplitude=segmentData["relativeAmplitude"]
    beats=segmentData["beats"]
    onsets=segmentData["onsets"]
    onsetRatios=segmentData["onsetRatios"]
    # Sort the onset ratio pairs from highest to lowest, in order to get the
    # most significant ones
    onsetRatioPairsSorted=sorted([(onsetRatios[i],onsets[i]) for i in range(0,len(onsets))],reverse=True)
    # Get a significant onset in the range of 40 to 60 ds from the start of the segment
    onsetRatioPairsCropped=[(i,j) for (i,j) in onsetRatioPairsSorted if j>start+40 and j<start+60]
    if(len(onsetRatioPairsCropped)>0):
        onsetSignal=onsetRatioPairsCropped[0][1]
    else:
        onsetSignal=start+50
    # Get the quadratic velocities
    velocities=getQuadraticVelocities(segmentAmplitude,maxAmplitude)
    intensities=getLinearIntensities(segmentAmplitude,maxAmplitude)

    # The velocities to be used in this scenario
    v11=velocities["U1"]
    v21=velocities["U2"]
    v22=velocities["U2"]*0.85
    v31=velocities["U3"]
    v41=velocities["U4"]
    i01=intensities["U0"]

    # Start with a slow rising of U3 and U4. A sine wave plays on U2 and
    # a beat-based move on U1 throughout
    simultaneousOnBeat(performance,beats,U1_TRIPLETS1,U1_TRIPLETS2,v11,1)
    sineWave(performance,start,end,U2,v21,v22)
    slowRising(performance,start,onsetSignal,U3,v31)
    slowRising(performance,start,onsetSignal,U4,v41)
    # Keep U3 and U4 constant after the rising has completed
    constantVelocity(performance,onsetSignal,end,U3,v31)
    constantVelocity(performance,onsetSignal,end,U4,v41)
    # Trigger U1 on the two most significant onsets in the segment
    simultaneous(performance,onsetRatioPairsSorted[0][1],U1,15)
    simultaneous(performance,onsetRatioPairsSorted[1][1],U1,15)
    slowIntensityChange(performance,start,onsetSignal,U0,i01)
    constantIntensity(performance,onsetSignal,end,U0,i01)
    return 2

# A scenario assigned to a verse
def scVerse_1(performance,segmentData):
    start=segmentData["start"]
    end=segmentData["end"]
    maxAmplitude=segmentData["maxAmplitude"]
    segmentAmplitude=segmentData["segmentAmplitude"]
    relativeAmplitude=segmentData["relativeAmplitude"]
    beats=segmentData["beats"]
    onsets=segmentData["onsets"]
    onsetRatios=segmentData["onsetRatios"]
    # Sort the onset ratio pairs from highest to lowest, in order to get the
    # most significant ones
    onsetRatioPairsSorted=sorted([(onsetRatios[i],onsets[i]) for i in range(0,len(onsets))],reverse=True)
    # Get a significant onset in the range of 40 to 60 ds from the start of the segment
    onsetRatioPairsCropped=[(i,j) for (i,j) in onsetRatioPairsSorted if j>start+40 and j<start+60]
    if(len(onsetRatioPairsCropped)>0):
        onsetSignal=onsetRatioPairsCropped[0][1]
    else:
        onsetSignal=start+50
    # Get the quadratic velocities
    velocities=getQuadraticVelocities(segmentAmplitude,maxAmplitude)
    intensities=getLinearIntensities(segmentAmplitude,maxAmplitude)

    # The velocities to be used in this scenario
    v11=velocities["U1"]
    v21=velocities["U2"]
    v31=velocities["U3"]
    v32=velocities["U3"]*0.9
    v41=velocities["U4"]
    i01=intensities["U0"]

    # Start with a slow rising of U3 and U4. Perform constant waves of U1
    # and U2 in opposite directions
    constantWave(performance,start,end,U1,v11,1,1)
    constantWave(performance,start,end,U2,v11,0,1)
    slowRising(performance,start,onsetSignal,U3,v31)
    slowRising(performance,start,onsetSignal,U4,v41)
    # Continue with a beat based move of U3. Keep U4 constant
    slowRisingOnBeatAlternating(performance,[b for b in beats if b>onsetSignal],U3_HALF2,U3_HALF1,v31,v32,3)
    constantVelocity(performance,onsetSignal,end,U4,v41)
    # Trigger U2 on the two most significant onsets of the segment
    simultaneous(performance,onsetRatioPairsSorted[0][1],U2,15)
    simultaneous(performance,onsetRatioPairsSorted[1][1],U2,15)
    slowIntensityChange(performance,start,onsetSignal,U0,i01)
    constantIntensity(performance,onsetSignal,end,U0,i01)
    return 3

# A scenario assigned to a verse
def scVerse_2(performance,segmentData):
    start=segmentData["start"]
    end=segmentData["end"]
    maxAmplitude=segmentData["maxAmplitude"]
    segmentAmplitude=segmentData["segmentAmplitude"]
    relativeAmplitude=segmentData["relativeAmplitude"]
    # Store a step variable that indicates whether the segment is relatively
    # of high or low amplitude
    step=1 if segmentAmplitude>relativeAmplitude else 2
    beats=segmentData["beats"]
    onsets=segmentData["onsets"]
    onsetRatios=segmentData["onsetRatios"]
    # Sort the onset ratio pairs from highest to lowest, in order to get the
    # most significant ones
    onsetRatioPairsSorted=sorted([(onsetRatios[i],onsets[i]) for i in range(0,len(onsets))],reverse=True)
    # Get a significant onset in the range of 40 to 60 ds from the start of the segment
    onsetRatioPairsCropped=[(i,j) for (i,j) in onsetRatioPairsSorted if j>start+40 and j<start+60]
    if(len(onsetRatioPairsCropped)>0):
        onsetSignal=onsetRatioPairsCropped[0][1]
    else:
        onsetSignal=start+50
    # Get the quadratic velocities
    velocities=getQuadraticVelocities(segmentAmplitude,maxAmplitude)
    intensities=getLinearIntensities(segmentAmplitude,maxAmplitude)

    # The velocities to be used in this scenario
    v11=velocities["U1"]
    v12=velocities["U1"]*0.8
    v21=velocities["U2"]*0.8
    v22=velocities["U2"]*0.7
    v31=velocities["U3"]
    v32=velocities["U3"]
    v41=velocities["U4"]
    i01=intensities["U0"]

    # Start with a slow rising of U2, U3 and U4. Perform a beat based move of U1
    simultaneousOnBeat(performance,beats,U1_TRIPLETS1,U1_TRIPLETS2,v11,step)
    slowRising(performance,start,onsetSignal,U2,v21)
    slowRising(performance,start,onsetSignal,U3,v31)
    slowRising(performance,start,onsetSignal,U4,v41)
    # Continue with a beat based move of U2 and keep U3 and U4 constant
    slowRisingOnBeatAlternating(performance,[b for b in beats if b>onsetSignal],U2_TRIPLETS1,U2_TRIPLETS2,v21,v22,3)
    constantVelocity(performance,onsetSignal,end,U3,v31)
    constantVelocity(performance,onsetSignal,end,U4,v41)
    # Trigger U2 on the most significant onset of the segment
    simultaneous(performance,onsetRatioPairsSorted[0][1],U2,15)
    slowIntensityChange(performance,start,onsetSignal,U0,i01)
    constantIntensity(performance,onsetSignal,end,U0,i01)
    return 4

# A scenario assigned to a verse
def scVerse_3(performance,segmentData):
    start=segmentData["start"]
    end=segmentData["end"]
    maxAmplitude=segmentData["maxAmplitude"]
    segmentAmplitude=segmentData["segmentAmplitude"]
    relativeAmplitude=segmentData["relativeAmplitude"]
    # Store a step variable that indicates whether the segment is relatively
    # of high or low amplitude
    step=1 if segmentAmplitude>relativeAmplitude else 2
    beats=segmentData["beats"]
    onsets=segmentData["onsets"]
    onsetRatios=segmentData["onsetRatios"]
    # Sort the onset ratio pairs from highest to lowest, in order to get the
    # most significant ones
    onsetRatioPairsSorted=sorted([(onsetRatios[i],onsets[i]) for i in range(0,len(onsets))],reverse=True)
    # Get a significant onset in the range of 40 to 60 ds from the start of the segment
    onsetRatioPairsCropped=[(i,j) for (i,j) in onsetRatioPairsSorted if j>start+40 and j<start+60]
    if(len(onsetRatioPairsCropped)>0):
        onsetSignal=onsetRatioPairsCropped[0][1]
    else:
        onsetSignal=start+50
    # Get the quadratic velocities
    velocities=getQuadraticVelocities(segmentAmplitude,maxAmplitude)
    intensities=getLinearIntensities(segmentAmplitude,maxAmplitude)

    # The velocities to be used in this scenario
    v11=velocities["U1"]
    v21=velocities["U2"]
    v22=velocities["U2"]*0.8
    v31=velocities["U3"]
    v32=velocities["U3"]*0.8
    v41=velocities["U4"]
    i01=intensities["U0"]

    # Start with a slow rising of U3 and U4. Perform a constant wave on U2 and
    # a beat-based move on U1
    simultaneousOnBeat(performance,beats,U1_ODD,U1_EVEN,v11,step)
    constantWave(performance,start,end,U2,v22,1,1)
    slowRising(performance,start,onsetSignal,U3,v31)
    slowRising(performance,start,onsetSignal,U4,v41)
    # Keep U3 and U4 constant
    constantVelocity(performance,onsetSignal,end,U3,v31)
    constantVelocity(performance,onsetSignal,end,U4,v41)
    # Trigger U2 on the two most significant onsets of the segment
    simultaneous(performance,onsetRatioPairsSorted[0][1],U2,15)
    simultaneous(performance,onsetRatioPairsSorted[1][1],U2,15)
    slowIntensityChange(performance,start,onsetSignal,U0,i01)
    constantIntensity(performance,onsetSignal,end,U0,i01)
    return 5

# Keep a list of the scenarios, in order for them to be callable using their
# respective place in the list
scenarios=[scIntro,scOutro,scChorus,scVerse_1,scVerse_2,scVerse_3]
