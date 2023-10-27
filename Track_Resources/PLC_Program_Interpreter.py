import sys
sys.path.append(".")
from signals import *
from Track_Resources.Track import *
from Main_Backend import *

class Interpreter():
    def __init__(self):
        # Create copy of current track instance
        self.trackCopy = mainInstance.trackInstance

    # Interprets one PLC file
    def interpretSingleFile(self, filename):
        fileIn = open(filename,"r")
        line = fileIn.readline()
        while line:
            line = line.strip()
            if(line == "LN_START"):
                line = fileIn.readline()
                line.strip()
                trackLineColor = int(line[6])
            elif(line == "BLK_START"):
                blockNumber = 0
                blockNumberArray = []
                for i in range(8):
                    line = fileIn.readline()
                    line.strip()
                    blockNumberArray.append(int(line[6]))
                for i in range(8):
                    blockNumber += int(blockNumberArray[i]) * (2**i)

                line = fileIn.readline()
                line.strip()
                switchDirection = int(line[6])

                line = fileIn.readline()
                line.strip()
                trafficLight = int(line[6])

                line = fileIn.readline()
                line.strip()
                crossingActive = int(line[6])

                # Update switch direction
                self.trackCopy.lines[trackLineColor].blocks[blockNumber].switchDirection = switchDirection
                
                # Update traffic light color
                self.trackCopy.lines[trackLineColor].blocks[blockNumber].trafficLightColor = trafficLight
                    
                # Update crossing active status
                self.trackCopy.lines[trackLineColor].blocks[blockNumber].crossingActive = crossingActive
            line = fileIn.readline()

        # Emit signal to update track
        signals.sw_wayside_track_update.emit(self.trackCopy)
        return self.trackCopy

    # Interprets multiple PLC files
    def interpretMultipleFiles(self, filenames):
        for filename in filenames:
            self.interpretSingleFile(self, filename)