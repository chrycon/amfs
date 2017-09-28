import matlab.engine
import math
import sys
from setup import *
AEG_PATH = ".\AEGTools_1.5"

# Get the Valence-Arousal pair from the input audio file
def getVApair(audioFile):
    eng = matlab.engine.start_matlab()
    # Add the path of the classifier to MATLAB's paths for this session
    eng.addpath(eng.genpath(AEG_PATH))
    # Perform emotion detection on the audio file given
    matlab_out = eng.predict(audioFile)
    # Get the Valence-Arousal pair out of the matlab output
    VApair = (matlab_out[0][0],matlab_out[0][1])
    return VApair

# Assign a color palette to the given VApair. The colors are specified in setup.py
def groupColor(VApair):
    valence = VApair[0]
    arousal = VApair[1]
    # Check which group the VA pair belongs to and return it
    for i in range(0,len(COLOR_GROUPS)):
        if(COLOR_GROUPS[i]["bounds"](valence,arousal)):
            return COLOR_GROUPS[i]
    return 0
