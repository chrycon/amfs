import math

# Behaviour of the color of the fountain's lights

def getColor(performance,time,jet):
    return performance["intervals"][time]["jetState"][jet]["lightColor"]

def setColor(performance,time,jet,lightColor):
    performance["intervals"][time]["jetStates"][jet]["lightColor"]=lightColor

# Set the same color on the chosen unit for the whole duration of a selected period
def constantColor(performance,startTime,endTime,unit,color):
    for t in range(startTime,endTime):
        for jet in unit:
            setColor(performance,t,jet,color)

# Behaviour of the intensity of the fountain's lights

def getIntensity(performance,time,jet):
    return performance["intervals"][time]["jetStates"][jet]["lightIntensity"]

def setIntensity(performance,time,jet,lightIntensity):
    performance["intervals"][time]["jetStates"][jet]["lightIntensity"]=lightIntensity

# Set the same intensity on the chosen unit for the whole duration of a selected period
def constantIntensity(performance,startTime,endTime,unit,lightIntensity):
    for t in range(startTime,endTime):
        for jet in unit:
            setIntensity(performance,t,jet,lightIntensity)

def slowIntensityChange(performance,startTime,endTime,unit,endIntensity,startIntensity=None):
    if(startTime>2):
        startTime-=2
    for jet in unit:
        if(startIntensity==None):
            if(getIntensity(performance,startTime,jet)>0 and
            getIntensity(performance,startTime+1,jet)>0):
                currentIntensity=getIntensity(performance,startTime,jet)
            else:
                currentIntensity=0
        else:
            currentIntensity=startIntensity
        diff=(endIntensity-currentIntensity)/float(endTime-startTime)
        newIntensity=currentIntensity
        for i in range(startTime,endTime):
            newIntensity+=diff
            setIntensity(performance,i,jet,newIntensity)

# Behaviour of the velocity of the fountain's jets
def getVelocity(performance,time,jet):
    return performance["intervals"][time]["jetStates"][jet]["velocity"]

def setVelocity(performance,time,jet,velocity):
    performance["intervals"][time]["jetStates"][jet]["velocity"]=velocity

# Set the same velocity on the chosen unit for the whole duration of a selected period
def constantVelocity(performance,startTime,endTime,unit,velocity):
    for i in range(startTime,endTime):
        simultaneous(performance,i,unit,velocity)

# Perform a sine wave on the chosen unit during the selected period
def sineWave(performance,startTime,endTime,unit,minVelocity,maxVelocity):
    velocityD=(maxVelocity-minVelocity)*0.5
    noJets=len(unit)
    for t in range(startTime,endTime):
        for jet in unit:
            # The equation of the wave is v = v_d * sin((2pi/n)*(t+jet)) + v_d +v_min
            velocity=velocityD*math.sin(2*math.pi/(noJets/2)*(t+jet))+velocityD+minVelocity
            setVelocity(performance,t,jet,velocity)

# Perform a wave on the chosen unit, that causes only one jet to be active at a
# specific time
def constantWave(performance,startTime,endTime,unit,velocity,direction,step):
    startJet=unit[0]
    endJet=unit[-1]
    noJets=len(unit)
    # Anticlockwise
    if(direction==0):
        for i in range(startTime,endTime,step):
            setVelocity(performance,i,int(i%noJets+startJet),velocity)
    # Clockwise
    elif(direction==1):
        for i in range(startTime,endTime,step):
            setVelocity(performance,i,int(endJet-i%noJets),velocity)

# Perform a constant wave that synchronises the jets to the beats. This is too slow
# and doesn't produce an appealing effect. Not currently in use.
def beatWave(performance,timestamps,unit,velocity):
    startJet=unit[0]
    endJet=unit[-1]
    noJets=len(unit)
    for i in range(0,len(timestamps)):
        for j in range(0,2):
            setVelocity(performance,timestamps[i],int((i+j*18)%noJets+startJet),velocity)

# Trigger all jets of a unit to go off simultaneously and instantaneously
def simultaneous(performance,time,unit,velocity):
    for jet in unit:
        setVelocity(performance,time,jet,velocity)

# Cause two units to alternately go off with respect to a list of timestamps
def simultaneousOnBeat(performance,timestamps,unit1,unit2,velocity,step):
    # Controls which unit out of the two will shoot
    timestampsWithStep=[timestamps[i] for i in range(0,len(timestamps)) if i%step==0]
    # unit1 will start first
    turn=1
    for t in timestampsWithStep:
        if(turn==1):
            for i in unit1:
                simultaneous(performance,t,unit1,velocity)
            turn=2
        else:
            for i in unit2:
                simultaneous(performance,t,unit2,velocity)
            turn=1

# Causes a slow rising of a unit from the specified start velocity to an end velocity
# during the chosen time interval
def slowRising(performance,startTime,endTime,unit,endVelocity,startVelocity=None):
    # Change the start time to start just a bit quicker, in order to ensure the
    # transition from one speed to another is smoother
    if(startTime>2):
        startTime-=2
    for jet in unit:
        # If no start velocity is specified
        if(startVelocity==None):
            # If the two previous velocities from the start time were not equal to zero
            # then assign the current velocity to be the velocity of the jet at start time
            if(getVelocity(performance,startTime,jet)>0 and getVelocity(performance,startTime+1,jet)>0):
                currentVelocity=getVelocity(performance,startTime,jet)
            else:
                currentVelocity=0
        else:
            currentVelocity=startVelocity
        diff=(endVelocity-currentVelocity)/float(endTime-startTime)
        newVelocity=currentVelocity
        # Change the velocity slowly in equal increments in the time period specified
        for i in range(startTime,endTime):
            newVelocity+=diff
            setVelocity(performance,i,jet,newVelocity)


# Causes several slow rising movements of a unit as defined above which are synchronised
# to the timestamps provided
def slowRisingOnBeat(performance,timestamps,unit,minVelocity,maxVelocity,step):
    if(len(timestamps)<=1):
        return
    else:
        # Produce the decreasing phases
        for i in range(0,len(timestamps),2*step):
            if(len(timestamps)<i+step+1):
                duration=step*(timestamps[1]-timestamps[0])
            else:
                duration=timestamps[i+step]-timestamps[i]
            slowRising(performance,timestamps[i],timestamps[i]+duration,unit,maxVelocity,minVelocity)
        # Produce the increasing phases
        for i in range(step,len(timestamps),2*step):
            if(len(timestamps)<i+step+1):
                duration=step*(timestamps[1]-timestamps[0])
            else:
                duration=timestamps[i+step]-timestamps[i]
            slowRising(performance,timestamps[i],timestamps[i]+duration,unit,minVelocity,maxVelocity)

# Perform a slow rising on beat of two units that alternate with each other
def slowRisingOnBeatAlternating(performance,timestamps,unit1,unit2,minVelocity,maxVelocity,step):
    slowRisingOnBeat(performance,timestamps,unit1,minVelocity,maxVelocity,step)
    slowRisingOnBeat(performance,timestamps,unit2,maxVelocity,minVelocity,step)
