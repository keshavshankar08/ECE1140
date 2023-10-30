from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import cv2
sys.path.append(".")
import Track_Resources.Track as track

class SWWaysideModuleUI(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("Modules/SW_Wayside/Frontend/SW_Wayside_UI.ui", self)
                
                # Create default track object
                self.track = track.generateDefaultTrack()
                
                # Line Option Calls
                linesList = [self.track.lines[0].lineColor]
                self.TrackLineColorValue.addItems(linesList)
                self.TrackLineColorValue.textActivated.connect(self.updateWaysideMenu)
                self.TrackMapViewButton.clicked.connect(self.mapViewClicked)
                self.OperationModeValue.textActivated.connect(self.switchOperationMode)

                # Wayside Option Calls
                self.WaysideControllerUploadPLCProgramButton.clicked.connect(self.uploadPLCClicked)
                self.WaysideControllerWaysideValue.textActivated.connect(self.updateBlockMenu)

                # Block Option Calls
                self.BlockStatusBlockNumberValue.textActivated.connect(self.updateBlockInfo)

                # Test Bench Option Calls
                self.TestBenchActive = False
                self.TestBenchActivateButton.clicked.connect(self.activateTestBench)
                self.TestBenchDeactivateButton.clicked.connect(self.deactivateTestbench)
                self.TestBenchSendSignalsButton.clicked.connect(self.testbenchSendSignal)

                self.show()

        # Opens map of device layout for current line
        def mapViewClicked(self):
                lineNumber = 1
                if(lineNumber == 1):
                        image = cv2.imread("src/frontend/SW_Wayside/BlueLine.jpg")
                elif(lineNumber == 2):
                        image = cv2.imread("src/frontend/SW_Wayside/BlueLine.jpg")
                elif(lineNumber == 3):
                        image = cv2.imread("src/frontend/SW_Wayside/BlueLine.jpg")
                cv2.imshow("Blue Line Map", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        # Updates UI editability based on operation mode
        def switchOperationMode(self):
                if(self.OperationModeValue.currentText() == "Manual"):
                        self.JunctionSwitchDirectionValue.setEnabled(True)
                        self.JunctionTrafficLightValue.setEnabled(True)
                        self.BlockCrossingActiveValue.setEnabled(True)
                        self.TestBenchBox.setEnabled(True)
                        SWWaysideModuleUI.deactivateTestbench(self)
                elif(self.OperationModeValue.currentText() == "Automatic"):
                        self.JunctionSwitchDirectionValue.setEnabled(False)
                        self.JunctionTrafficLightValue.setEnabled(False)
                        self.BlockCrossingActiveValue.setEnabled(False)
                        self.TestBenchBox.setEnabled(False)

        def updateWaysideMenu(self):
                self.WaysideControllerWaysideValue.clear()
                if(self.TrackLineColorValue.currentText() == "Blue Line"):
                        waysidesList = []
                        for wayside in self.track.lines[0].waysides:
                                waysidesList.append("Wayside " + str(wayside.waysideNumber))
                        self.WaysideControllerWaysideValue.addItems(waysidesList)
                else:
                        self.WaysideControllerWaysideValue.clear()
        
        def updateBlockMenu(self):
                self.BlockStatusBlockNumberValue.clear()
                currWayside = int((self.WaysideControllerWaysideValue.currentText())[-1])
                blockList = []
                for block in self.track.lines[0].waysides[currWayside-1].blocks:
                        blockList.append("Block " + str(block.blockNumber))
                self.BlockStatusBlockNumberValue.addItems(blockList)

        def updateBlockInfo(self):
                currWayside = int((self.WaysideControllerWaysideValue.currentText())[7:]) - 1
                blockIndex = []
                if(currWayside == 0):
                        blockIndex = [1,2,3,4,5]
                elif(currWayside == 1):
                        blockIndex = [6,7,8,9,10]
                elif(currWayside == 2):
                        blockIndex = [11,12,13,14,15]
                currBlock = int((self.BlockStatusBlockNumberValue.currentText())[5:])
                currBlockIndex = blockIndex.index(currBlock)
                self.BlockTypeValue.setText(str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockType))
                self.BlockOccupancyValue.setText(str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockOccupied))
                self.MaintenanceTrackFaultValue.setText(str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trackFaultDetected))
                self.MaintenanceActiveValue.setText(str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].maintenanceActive))
                if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockType == "Junction"):
                        self.JunctionBox.setEnabled(True)
                        self.StationBox.setEnabled(False)
                        self.CrossingBox.setEnabled(False)
                        self.JunctionSwitchDirectionValue.clear()
                        self.JunctionTrafficLightValue.clear()

                        # Junction Switch Logic
                        if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockOccupied == True):
                                # If block is receiver end
                                if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].isReceiverEnd == True):
                                        prevBlockIndex = 4
                                        prevBlockWayside = 0
                                        prevBlockNextIndex = 0
                                        prevBlockNextWayside = 1
                                        prevBlockNextNextIndex = 0
                                        prevBlockNextNextWayside = 2
                                        # If one receiver occupied
                                        if(self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].blockOccupied == True ^ self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].blockOccupied == True):
                                                # If switch block not occupied
                                                if(self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].blockOccupied == False):
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].trafficLightColor = "Green"
                                                        if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockNumber == 6):
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                                                self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].switchDirection = "5-6"
                                                                self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].switchDirection = "5-6"
                                                        else:
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                                                                self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].switchDirection = "5-11"
                                                                self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].switchDirection = "5-11"
                                                else:
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].trafficLightColor = "Green"
                                                        if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockNumber == 6):
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                                                                self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].switchDirection = "5-11"
                                                                self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].switchDirection = "5-11"
                                                        else:
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                                                self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].switchDirection = "5-6"
                                                                self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].switchDirection = "5-6"
                                        # If both receivers occupied
                                        elif(self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].blockOccupied == True and self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].blockOccupied == True):
                                                # If switch block not occupied
                                                if(self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].blockOccupied == False):
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].trafficLightColor = "Green"
                                                        if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockNumber == 6):
                                                                self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].trafficLightColor = "Red"
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                                                self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].switchDirection = "5-6"
                                                                self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].switchDirection = "5-6"
                                                        else:
                                                                self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].trafficLightColor = "Red"
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                                                                self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].switchDirection = "5-11"
                                                                self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].switchDirection = "5-11"
                                                else:
                                                        self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].trafficLightColor = "Red"
                                else:
                                        nextBlockIndex = 0
                                        nextBlockWayside = 1
                                        nextNextBlockIndex = 0
                                        nextnextBlockWayside = 2
                                        # If one receiver occupied
                                        if(self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].blockOccupied == True ^ self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].blockOccupied == True):
                                                if(self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].blockOccupied == True):
                                                        self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                                                        self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].switchDirection = "5-11"
                                                        self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].switchDirection = "5-11"
                                                else:
                                                        self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                                        self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].switchDirection = "5-6"
                                                        self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].switchDirection = "5-6"
                                        # If two receivers occupied
                                        elif(self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].blockOccupied == True and self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].blockOccupied == True):
                                                self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].trafficLightColor = "Red"
                                                self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].trafficLightColor = "Red"
                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Red"
                                        # If not receivers occupied
                                        elif(self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].blockOccupied == False and self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].blockOccupied == False):
                                                self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].trafficLightColor = "Green"
                                                self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].trafficLightColor = "Red"
                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                                self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].switchDirection = "5-6"
                                                self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].switchDirection = "5-6"
 
                        self.JunctionSwitchDirectionValue.addItems(["5-11", "5-6"])
                        self.JunctionSwitchDirectionValue.setCurrentText(str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection))
                        self.JunctionIsReceiverEndValue.setText(str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].isReceiverEnd))
                        self.JunctionTrafficLightValue.addItems(["Green", "Red"])
                if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockType == "Station"):
                        self.StationBox.setEnabled(True)
                        self.JunctionBox.setEnabled(False)
                        self.CrossingBox.setEnabled(False)
                        self.StationNameValue.setText(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].stationName)
                elif(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockType == "Crossing"):
                        self.CrossingBox.setEnabled(True)
                        self.JunctionBox.setEnabled(False)
                        self.StationBox.setEnabled(False)
                        self.BlockCrossingActiveValue.clear()
                        self.BlockCrossingActiveValue.addItems([str(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].crossingActive), str(not(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].crossingActive))])
                elif(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockType == "Default"):
                        self.CrossingBox.setEnabled(False)
                        self.JunctionBox.setEnabled(False)
                        self.StationBox.setEnabled(False)

        # Opens file browser to open/upload .txt PLC file
        def uploadPLCClicked(self):
                fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")

        # Activates test bench
        def activateTestBench(self):
                self.TestTrackFaultDetectedValue.setEnabled(True)
                self.TestMaintenenaceActiveValue.setEnabled(True)
                self.TestBlockOccupiedValue.setEnabled(True)
                self.TestBenchSendSignalsButton.setEnabled(True)
                self.TestBenchActive = True

        # Deactivates test bench
        def deactivateTestbench(self):
                self.TestTrackFaultDetectedValue.setEnabled(False)
                self.TestMaintenenaceActiveValue.setEnabled(False)
                self.TestBlockOccupiedValue.setEnabled(False)
                self.TestBenchSendSignalsButton.setEnabled(False)
                self.TestBenchActive = False

        # Sends test bench signals
        def testbenchSendSignal(self):
                currWayside = int((self.WaysideControllerWaysideValue.currentText())[7:]) - 1
                blockIndex = []
                if(currWayside == 0):
                        blockIndex = [1,2,3,4,5]
                elif(currWayside == 1):
                        blockIndex = [6,7,8,9,10]
                elif(currWayside == 2):
                        blockIndex = [11,12,13,14,15]
                currBlock = int((self.BlockStatusBlockNumberValue.currentText())[5:])
                currBlockIndex = blockIndex.index(currBlock)
                if(self.TestBlockOccupiedValue.currentText() == "True"):
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockOccupied = True
                else:
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockOccupied = False
                if(self.TestTrackFaultDetectedValue.currentText() == "True"):
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trackFaultDetected = True
                else:
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trackFaultDetected = False
                if(self.TestMaintenenaceActiveValue.currentText() == "True"):
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].maintenanceActive = True
                else:
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].maintenanceActive = False
                if(self.JunctionSwitchDirectionValue.currentText() == "5-6"):
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                else:
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                if(self.JunctionTrafficLightValue.currentText() == "Green"):
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "Green"
                else:
                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "Red"

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = SWWaysideModuleUI()
        app.exec()
