# Track Object - A entire track network
class Track:
    def __init__(self):
        self.lines: list[Line] = []

# Line Object - A single line from the entire track network
class Line:
    def __init__(self):
        self.lineColor = ""
        self.waysides: list[Wayside] = []

# Wayside Object - A single wayside controller on a single line
class Wayside:
    def __init__(self):
        self.waysideNumber = 0
        self.blocks: list[Block] = []

# Block Object - A single block linked to a single wayside controller
class Block:
    def __init__(self):
        self.blockNumber = 0
        self.nextBlockNumber = 0
        self.nextNextBlockNumber = 0
        self.previousBlockNumber = 0
        self.blockType = ""
        self.blockOccupied = False
        self.trackFaultDetected = False
        self.maintenanceActive = False
        self.switchDirection = ""
        self.isReceiverEnd = False
        self.trafficLightColor = ""
        self.stationName = ""
        self.crossingActive = False

# Generates a track with predefined values for physical devices and elements
def generateDefaultTrack():
    # Create track object
    track = Track()

    # Fill with 3 lines
    for i in range(3):
        track.lines.append(Line())

    # Update line colors
    track.lines[0].lineColor = "Blue"
    track.lines[1].lineColor = "Red"
    track.lines[2].lineColor = "Green"

    # Initializing blue line
    if(track.lines[0].lineColor == "Blue"):
        # Define number of waysides and blocks
        numWaysides = 3
        numBlocks = 15

        # Fill line with waysides
        for i in range(numWaysides):
            track.lines[0].waysides.append(Wayside())

        # Wayside blocks (0 index = WS1, 1 index = WS2, 2 index = WS3)
        waysideBlocks = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]

        # Fill wayside with blocks
        for i in range(len(waysideBlocks)):
            for j in waysideBlocks[i]:
                track.lines[0].waysides[i].blocks.append(Block())
        
        # Default Blocks
        defaultBlocks = [2,3,4,7,8,9,12,13,14]

        # Station Blocks
        stationBlocks = [1,10,15]
        stationBlocksNames = ["Yard", "Station B", "Station C"]
        stationBlocksNoNext = [10,15]
        stationBlocksNoPrevious = [1]

        # Junction Blocks
        junctionBlocks = [5,6,11]
        junctionSwitch = [5]
        junctionReceiver = [6,11]

        # Crossing Blocks
        crossingBlocks = []
        
        # Algorithm to fill each block with corresponding data
        blockNumberCount = 1
        for numWayside in range(numWaysides):
            # Assign wayside number
            track.lines[0].waysides[numWayside].waysideNumber = numWayside + 1

            # Loop through each block for a wayside
            for numBlock in range(len(waysideBlocks[numWayside])):
                # Assign block number
                track.lines[0].waysides[numWayside].blocks[numBlock].blockNumber = blockNumberCount

                # Assign block type and corresponding information
                if(blockNumberCount in defaultBlocks):
                    track.lines[0].waysides[numWayside].blocks[numBlock].blockType = "Default"
                    track.lines[0].waysides[numWayside].blocks[numBlock].nextBlockNumber = blockNumberCount+1
                    track.lines[0].waysides[numWayside].blocks[numBlock].previousBlockNumber = blockNumberCount-1
                elif(blockNumberCount in stationBlocks):
                    track.lines[0].waysides[numWayside].blocks[numBlock].blockType = "Station"
                    if(blockNumberCount in stationBlocksNoNext):
                        track.lines[0].waysides[numWayside].blocks[numBlock].nextBlockNumber = 0
                        track.lines[0].waysides[numWayside].blocks[numBlock].previousBlockNumber = blockNumberCount-1
                    elif(blockNumberCount in stationBlocksNoPrevious):
                        track.lines[0].waysides[numWayside].blocks[numBlock].previousBlockNumber = 0
                        track.lines[0].waysides[numWayside].blocks[numBlock].nextBlockNumber = blockNumberCount+1
                    for numStations in range(len(stationBlocks)):
                        track.lines[0].waysides[numWayside].blocks[numBlock].stationName = stationBlocksNames[stationBlocks.index(blockNumberCount)]
                elif(blockNumberCount in junctionBlocks):
                    track.lines[0].waysides[numWayside].blocks[numBlock].blockType = "Junction"
                    if(blockNumberCount in junctionSwitch):
                        track.lines[0].waysides[numWayside].blocks[numBlock].previousBlockNumber = blockNumberCount-1
                        track.lines[0].waysides[numWayside].blocks[numBlock].nextBlockNumber = junctionReceiver[0]
                        track.lines[0].waysides[numWayside].blocks[numBlock].nextNextBlockNumber = junctionReceiver[1]
                    if(blockNumberCount in junctionReceiver):
                        track.lines[0].waysides[numWayside].blocks[numBlock].isReceiverEnd = True
                        track.lines[0].waysides[numWayside].blocks[numBlock].previousBlockNumber = junctionSwitch[0]
                        track.lines[0].waysides[numWayside].blocks[numBlock].nextBlockNumber = blockNumberCount+1
                elif(blockNumberCount in crossingBlocks):
                    track.lines[0].waysides[numWayside].blocks[numBlock].blockType = "Crossing"

                blockNumberCount += 1

        return track