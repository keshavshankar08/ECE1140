from Track import *

def defaultTrack():
    # Create track object
    track = Track()
    for i in range(3):
        track.lines.append(Line())

    # Fill track line colors
    track.lines[0].lineColor = "Blue"
    track.lines[1].lineColor = "Red"
    track.lines[2].lineColor = "Green"

    if(track.lines[0].lineColor == "Blue"):
        # Waysides
        numWaysides = 3
        numBlocks = 15
        for i in range(numWaysides):
            track.lines[0].waysides.append(Wayside())

        # Wayside blocks
        waysideBlocks = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]
        for i in range(len(waysideBlocks)):
            for j in waysideBlocks[i]:
                track.lines[0].waysides[i].blocks.append(Block())
        
        # Default type
        defaultBlocks = [2,3,4,7,8,9,12,13,14]

        # Station type
        stationBlocks = [1,10,15]
        stationBlocksNames = ["Yard", "Station B", "Station C"]
        stationBlocksNoNext = [10,15]
        stationBlocksNoPrevious = [1]

        # Junction type
        junctionBlocks = [5,6,11]
        junctionSwitch = [5]
        junctionReceiver = [6,11]

        # Crossing type
        crossingBlocks = []
        
        # Loop to fill data
        blockNumberCount = 1
        for numWayside in range(numWaysides):
            # Assign wayside number
            track.lines[0].waysides[numWayside].waysideNumber = numWayside + 1

            # Add blocks
            for numBlock in range(len(waysideBlocks[numWayside])):
                track.lines[0].waysides[numWayside].blocks[numBlock].blockNumber = blockNumberCount
                
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
    

if __name__ == "__main__":
    generatedTrack = defaultTrack()
    blueLine = generatedTrack.lines[0]
    for wayside in blueLine.waysides:
        for block in wayside.blocks:
            print("\n-----------")
            print("\nPrevious Block: " + str(block.previousBlockNumber))
            print("\nBlock Number: " + str(block.blockNumber))
            print("\nNext Block: " + str(block.nextBlockNumber))
            print("\nNext Next Block: " + str(block.nextNextBlockNumber))
            print("\nBlock Type: " + block.blockType)