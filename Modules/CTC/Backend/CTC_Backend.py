#CTC OFfice Backend
#This holds both the route class and a route queue
#This holds helper functions also

import re
import sys
import numpy as np
sys.path.append(".")
from Track_Resources.Track import *

class RouteQueue:
    def __init__(self):
        self.routes: list[Route] = []

class Route:
    def __init__(self):
        #create a counter
        self.stops = []
        self.stopTime = []



#Helper Functions

#Validates time in 00:00 to 23:59 format
def validateTimeInput(inputTime):
    #use regular expression to check time
    if re.match('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', inputTime):
        return True
    else:
        return False
    
#swaps station names to their block numbers
def stationNamesToBlocks(stationList, line):
    #make a block list and track object
    track = Track()
    stationList = np.array(stationList)

    if(line == "Red"):
        lineStationList = np.array(track.redLineStationNames)
        #block index array
        blockIndex = np.isin(lineStationList, stationList)
        #station block number array
        blockList = []
        for i in range(len(track.redLineStationBlocks)):
            if(blockIndex[i] == True):
                blockList.append(track.redLineStationBlocks[i])
        return blockList

    elif(line == "Green"):
        lineStationList = np.array(track.greenLineStationNames)
        #block index array
        blockIndex = np.isin(lineStationList, stationList)
        #station block number array
        blockList = []
        for i in range(len(track.greenLineStationBlocks)):
            if(blockIndex[i] == True):
                blockList.append(track.greenLineStationBlocks[i])
        return blockList
    
