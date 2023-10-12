inputFileName = "src/backend/SW_Wayside/PLC_Program.txt"
outputFileName = "src/backend/SW_Wayside/PLC_Program_Interpreted.txt"
fileIn = open(inputFileName,"r")
fileOut = open(outputFileName, "w")
line = fileIn.readline()
while line:
    line = line.strip()
    if(line == "LN_INF_START"):
        trackLineNumber = ""
        for i in range(2):
            line = fileIn.readline()
            line.strip()
            trackLineNumber = line[6] + trackLineNumber
        fileOut.write(trackLineNumber + "\n")
    elif(line == "WS_INF_START"):
        waysideNumber = ""
        for i in range(5):
            line = fileIn.readline()
            line.strip()
            waysideNumber = line[6] + waysideNumber
        fileOut.write(waysideNumber + "\n")
    elif(line == "BLK_START"):
        sectionLetter = blockNumber = nextBlockNumber = next2BlockNumber = previousBlockNumber = defaultBlock = junctionType = crossingType = stationType = switchOn = receiverEnd = trafficLight = stationName = crossingActive = ""
        for i in range(5):
            line = fileIn.readline()
            line.strip()
            sectionLetter = line[6] + sectionLetter
        for i in range(8):
            line = fileIn.readline()
            line.strip()
            blockNumber = line[6] + blockNumber
        for i in range(8):
            line = fileIn.readline()
            line.strip()
            nextBlockNumber = line[6] + nextBlockNumber
        for i in range(8):
            line = fileIn.readline()
            line.strip()
            next2BlockNumber = line[6] + next2BlockNumber
        for i in range(8):
            line = fileIn.readline()
            line.strip()
            previousBlockNumber = line[6] + previousBlockNumber

        line = fileIn.readline()
        line.strip()
        defaultBlock = line[6]
        
        line = fileIn.readline()
        line.strip()
        junctionType = line[6]

        line = fileIn.readline()
        line.strip()
        crossingType = line[6]

        line = fileIn.readline()
        line.strip()
        stationType = line[6]

        line = fileIn.readline()
        line.strip()
        switchOn = line[6]

        line = fileIn.readline()
        line.strip()
        receiverEnd = line[6]

        line = fileIn.readline()
        line.strip()
        trafficLight = line[6]

        for i in range(5):
            line = fileIn.readline()
            line.strip()
            stationName = line[6] + stationName

        line = fileIn.readline()
        line.strip()
        crossingActive = line[6]

        fileOut.write(sectionLetter + "," + blockNumber + "," + nextBlockNumber + "," + next2BlockNumber + "," + previousBlockNumber + "," + defaultBlock + "," + junctionType + "," + crossingType + "," + stationType + "," + switchOn + "," + receiverEnd + "," + trafficLight + "," + stationName + "," + crossingActive + "\n")

    line = fileIn.readline()