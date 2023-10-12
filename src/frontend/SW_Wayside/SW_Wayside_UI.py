from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import cv2
from Track import *

class SWWaysideModuleUI(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("src/frontend/SW_Wayside/SW_Wayside_UI.ui", self)
                
                # Create default track object
                self.track = generateDefaultTrack()
                
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
                                                        else:
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                                                else:
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].trafficLightColor = "Green"
                                                        if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockNumber == 6):
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
                                                        else:
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                        # If both receivers occupied
                                        elif(self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].blockOccupied == True and self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].blockOccupied == True):
                                                # If switch block not occupied
                                                if(self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].blockOccupied == False):
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[prevBlockWayside].blocks[prevBlockIndex].trafficLightColor = "Green"
                                                        if(self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].blockNumber == 6):
                                                                self.track.lines[0].waysides[prevBlockNextNextWayside].blocks[prevBlockNextNextIndex].trafficLightColor = "Red"
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
                                                        else:
                                                                self.track.lines[0].waysides[prevBlockNextWayside].blocks[prevBlockNextIndex].trafficLightColor = "Red"
                                                                self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-11"
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

                                                else:
                                                        self.track.lines[0].waysides[nextBlockWayside].blocks[nextBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[nextnextBlockWayside].blocks[nextNextBlockIndex].trafficLightColor = "Red"
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].trafficLightColor = "Green"
                                                        self.track.lines[0].waysides[currWayside].blocks[currBlockIndex].switchDirection = "5-6"
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
                
        def setupUi(self, SWWaysideModule):
                # Main Window
                SWWaysideModule.setObjectName("SWWaysideModule")
                SWWaysideModule.resize(1280, 720)
                SWWaysideModule.setMaximumSize(QtCore.QSize(1280, 720))
                font = QtGui.QFont()
                font.setFamily("Arial")
                SWWaysideModule.setFont(font)

                # Central Widget
                self.centralwidget = QtWidgets.QWidget(SWWaysideModule)
                self.centralwidget.setObjectName("centralwidget")

                #region Top Menu Bar
                # Menu Bar Frame
                self.MenuSection = QtWidgets.QFrame(self.centralwidget)
                self.MenuSection.setGeometry(QtCore.QRect(12, 12, 1256, 81))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.MenuSection.setFont(font)
                self.MenuSection.setLayoutDirection(QtCore.Qt.LeftToRight)
                self.MenuSection.setAutoFillBackground(False)
                self.MenuSection.setStyleSheet("background-color: rgb(21, 175, 255)")
                self.MenuSection.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.MenuSection.setFrameShadow(QtWidgets.QFrame.Raised)
                self.MenuSection.setObjectName("MenuSection")

                # Module Menu
                self.ModuleSelectionMenu = QtWidgets.QComboBox(self.MenuSection)
                self.ModuleSelectionMenu.setGeometry(QtCore.QRect(40, 20, 200, 50))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.ModuleSelectionMenu.setFont(font)
                self.ModuleSelectionMenu.setAutoFillBackground(False)
                self.ModuleSelectionMenu.setStyleSheet("background-color: rgb(211, 215, 215)")
                self.ModuleSelectionMenu.setMaxVisibleItems(10)
                self.ModuleSelectionMenu.setMaxCount(12)
                self.ModuleSelectionMenu.setObjectName("ModuleSelectionMenu")
                self.ModuleSelectionMenu.raise_()
                
                # System Speed
                self.SystemSpeedValue = QtWidgets.QDoubleSpinBox(self.MenuSection)
                self.SystemSpeedValue.setGeometry(QtCore.QRect(440, 20, 151, 51))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.SystemSpeedValue.setFont(font)
                self.SystemSpeedValue.setStyleSheet("background-color: rgb(211, 215, 215)")
                self.SystemSpeedValue.setDecimals(1)
                self.SystemSpeedValue.setMinimum(1.0)
                self.SystemSpeedValue.setMaximum(50.0)
                self.SystemSpeedValue.setSingleStep(0.1)
                self.SystemSpeedValue.setObjectName("SystemSpeedValue")
                self.SystemSpeedValue.raise_()
                self.SystemSpeedLabel = QtWidgets.QLabel(self.MenuSection)
                self.SystemSpeedLabel.setGeometry(QtCore.QRect(330, 40, 111, 20))
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(15)
                self.SystemSpeedLabel.setFont(font)
                self.SystemSpeedLabel.setObjectName("SystemSpeedLabel")
                self.SystemSpeedLabel.raise_()
                
                # System Clock
                self.SystemClockValue = QtWidgets.QTimeEdit(self.MenuSection)
                self.SystemClockValue.setGeometry(QtCore.QRect(780, 20, 150, 51))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.SystemClockValue.setFont(font)
                self.SystemClockValue.setStyleSheet("background-color: rgb(211, 215, 215)")
                self.SystemClockValue.setReadOnly(True)
                self.SystemClockValue.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(1, 0, 0)))
                self.SystemClockValue.setMaximumTime(QtCore.QTime(13, 56, 59))
                self.SystemClockValue.setMinimumTime(QtCore.QTime(0, 0, 0))
                self.SystemClockValue.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
                self.SystemClockValue.setCurrentSectionIndex(0)
                self.SystemClockValue.setObjectName("SystemClockValue")
                self.SystemClockValue.raise_()
                self.SystemClockLabel = QtWidgets.QLabel(self.MenuSection)
                self.SystemClockLabel.setGeometry(QtCore.QRect(680, 40, 101, 20))
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setPointSize(15)
                self.SystemClockLabel.setFont(font)
                self.SystemClockLabel.setObjectName("SystemClockLabel")
                self.SystemClockLabel.raise_()

                # System Info Button
                self.SystemInfoButton = QtWidgets.QPushButton(self.MenuSection)
                self.SystemInfoButton.setGeometry(QtCore.QRect(1020, 20, 200, 50))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.SystemInfoButton.setFont(font)
                self.SystemInfoButton.setStyleSheet("background-color: rgb(211, 215, 215)")
                self.SystemInfoButton.setObjectName("SystemInfoButton")
                self.SystemInfoButton.raise_()

                #endregion Top Menu Bar

                #region User Area
                # Module Frame
                self.ModuleSection = QtWidgets.QFrame(self.centralwidget)
                self.ModuleSection.setGeometry(QtCore.QRect(12, 90, 1256, 621))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.ModuleSection.setFont(font)
                self.ModuleSection.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.ModuleSection.setFrameShadow(QtWidgets.QFrame.Raised)
                self.ModuleSection.setObjectName("ModuleSection")

                # Track Line Menu
                self.TrackLineColorValue = QtWidgets.QComboBox(self.ModuleSection)
                self.TrackLineColorValue.setGeometry(QtCore.QRect(20, 20, 141, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TrackLineColorValue.setFont(font)
                self.TrackLineColorValue.setMaxVisibleItems(10)
                self.TrackLineColorValue.setMaxCount(3)
                self.TrackLineColorValue.setObjectName("TrackLineColorValue")

                # Track Map View Button
                self.TrackMapViewButton = QtWidgets.QPushButton(self.ModuleSection)
                self.TrackMapViewButton.setGeometry(QtCore.QRect(250, 20, 131, 32))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TrackMapViewButton.setFont(font)
                self.TrackMapViewButton.setObjectName("TrackMapViewButton")

                # Operation Mode Menu
                self.OperationModeValue = QtWidgets.QComboBox(self.ModuleSection)
                self.OperationModeValue.setGeometry(QtCore.QRect(1090, 20, 141, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.OperationModeValue.setFont(font)
                self.OperationModeValue.setObjectName("OperationModeValue")
                self.OperationModeValue.addItem("")
                self.OperationModeValue.addItem("")


                #region Wayside Controller
                # Wayside Controller Box
                self.WaysideControllerBox = QtWidgets.QGroupBox(self.ModuleSection)
                self.WaysideControllerBox.setGeometry(QtCore.QRect(20, 60, 1211, 551))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.WaysideControllerBox.setFont(font)
                self.WaysideControllerBox.setObjectName("WaysideControllerBox")

                # Wayside Controller Number
                self.WaysideControllerWaysideValue = QtWidgets.QComboBox(self.WaysideControllerBox)
                self.WaysideControllerWaysideValue.setGeometry(QtCore.QRect(20, 40, 150, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.WaysideControllerWaysideValue.setFont(font)
                self.WaysideControllerWaysideValue.setMaxCount(50)
                self.WaysideControllerWaysideValue.setObjectName("WaysideControllerWaysideValue")

                # Section Letter
                self.WaysideControllerSectionLetterValue = QtWidgets.QComboBox(self.WaysideControllerBox)
                self.WaysideControllerSectionLetterValue.setGeometry(QtCore.QRect(270, 40, 150, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.WaysideControllerSectionLetterValue.setFont(font)
                self.WaysideControllerSectionLetterValue.setMaxVisibleItems(10)
                self.WaysideControllerSectionLetterValue.setMaxCount(26)
                self.WaysideControllerSectionLetterValue.setObjectName("WaysideControllerSectionLetterValue")

                # PLC Program Upload Button
                self.WaysideControllerUploadPLCProgramButton = QtWidgets.QPushButton(self.WaysideControllerBox)
                self.WaysideControllerUploadPLCProgramButton.setGeometry(QtCore.QRect(510, 40, 171, 32))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.WaysideControllerUploadPLCProgramButton.setFont(font)
                self.WaysideControllerUploadPLCProgramButton.setObjectName("WaysideControllerUploadPLCProgramButton")
                #endregion Wayside Controller

                #region Block Status
                # Block Status Box
                self.BlockStatusBox = QtWidgets.QGroupBox(self.WaysideControllerBox)
                self.BlockStatusBox.setGeometry(QtCore.QRect(20, 80, 1171, 451))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.BlockStatusBox.setFont(font)
                self.BlockStatusBox.setObjectName("BlockStatusBox")

                # Block Number
                self.BlockStatusBlockNumberValue = QtWidgets.QComboBox(self.BlockStatusBox)
                self.BlockStatusBlockNumberValue.setGeometry(QtCore.QRect(20, 40, 150, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.BlockStatusBlockNumberValue.setFont(font)
                self.BlockStatusBlockNumberValue.setMaxCount(200)
                self.BlockStatusBlockNumberValue.setObjectName("BlockStatusBlockNumberValue")

                #endregion Block Status

                #region General
                # General Region
                self.GeneralBox = QtWidgets.QGroupBox(self.BlockStatusBox)
                self.GeneralBox.setGeometry(QtCore.QRect(20, 80, 351, 141))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.GeneralBox.setFont(font)
                self.GeneralBox.setObjectName("GeneralBox")

                # Block Type
                self.BlockTypeLabel = QtWidgets.QTextBrowser(self.GeneralBox)
                self.BlockTypeLabel.setGeometry(QtCore.QRect(20, 40, 121, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.BlockTypeLabel.setFont(font)
                self.BlockTypeLabel.setObjectName("BlockTypeLabel")
                self.BlockTypeValue = QtWidgets.QLineEdit(self.GeneralBox)
                self.BlockTypeValue.setGeometry(QtCore.QRect(210, 40, 113, 21))
                self.BlockTypeValue.setText("")
                self.BlockTypeValue.setAlignment(QtCore.Qt.AlignCenter)
                self.BlockTypeValue.setReadOnly(True)
                self.BlockTypeValue.setObjectName("BlockTypeValue")

                # Block Occupancy
                self.BlockOccupancyLabel = QtWidgets.QTextBrowser(self.GeneralBox)
                self.BlockOccupancyLabel.setGeometry(QtCore.QRect(20, 90, 121, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.BlockOccupancyLabel.setFont(font)
                self.BlockOccupancyLabel.setObjectName("BlockOccupancyLabel")
                self.BlockOccupancyValue = QtWidgets.QLineEdit(self.GeneralBox)
                self.BlockOccupancyValue.setGeometry(QtCore.QRect(242, 90, 81, 21))
                self.BlockOccupancyValue.setText("")
                self.BlockOccupancyValue.setMaxLength(3)
                self.BlockOccupancyValue.setAlignment(QtCore.Qt.AlignCenter)
                self.BlockOccupancyValue.setReadOnly(True)
                self.BlockOccupancyValue.setObjectName("BlockOccupancyValue")
                #endregion General

                #region Maintenance
                # Maintenance Region
                self.MaintenanceBox = QtWidgets.QGroupBox(self.BlockStatusBox)
                self.MaintenanceBox.setGeometry(QtCore.QRect(20, 240, 351, 141))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.MaintenanceBox.setFont(font)
                self.MaintenanceBox.setObjectName("MaintenanceBox")

                # Track Fault
                self.MaintenanceTrackFaultLabel = QtWidgets.QTextBrowser(self.MaintenanceBox)
                self.MaintenanceTrackFaultLabel.setGeometry(QtCore.QRect(20, 40, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.MaintenanceTrackFaultLabel.setFont(font)
                self.MaintenanceTrackFaultLabel.setObjectName("MaintenanceTrackFaultLabel")
                self.MaintenanceTrackFaultValue = QtWidgets.QLineEdit(self.MaintenanceBox)
                self.MaintenanceTrackFaultValue.setGeometry(QtCore.QRect(242, 40, 81, 21))
                self.MaintenanceTrackFaultValue.setText("")
                self.MaintenanceTrackFaultValue.setMaxLength(3)
                self.MaintenanceTrackFaultValue.setAlignment(QtCore.Qt.AlignCenter)
                self.MaintenanceTrackFaultValue.setReadOnly(True)
                self.MaintenanceTrackFaultValue.setObjectName("MaintenanceTrackFaultValue")

                # Maintenance Active
                self.MaintenanceActiveLabel = QtWidgets.QTextBrowser(self.MaintenanceBox)
                self.MaintenanceActiveLabel.setGeometry(QtCore.QRect(20, 90, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.MaintenanceActiveLabel.setFont(font)
                self.MaintenanceActiveLabel.setObjectName("MaintenanceActiveLabel")
                self.MaintenanceActiveValue = QtWidgets.QLineEdit(self.MaintenanceBox)
                self.MaintenanceActiveValue.setGeometry(QtCore.QRect(242, 90, 81, 21))
                self.MaintenanceActiveValue.setText("")
                self.MaintenanceActiveValue.setMaxLength(3)
                self.MaintenanceActiveValue.setAlignment(QtCore.Qt.AlignCenter)
                self.MaintenanceActiveValue.setReadOnly(True)
                self.MaintenanceActiveValue.setObjectName("MaintenanceActiveValue")
                #endregion Maintenance
                
                #region Junction
                # Junction Region
                self.JunctionBox = QtWidgets.QGroupBox(self.BlockStatusBox)
                self.JunctionBox.setGeometry(QtCore.QRect(420, 40, 351, 191))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.JunctionBox.setFont(font)
                self.JunctionBox.setObjectName("JunctionBox")

                # Switch Direction
                self.JunctionSwitchDirectionValue = QtWidgets.QComboBox(self.JunctionBox)
                self.JunctionSwitchDirectionValue.setGeometry(QtCore.QRect(230, 40, 104, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.JunctionSwitchDirectionValue.setFont(font)
                self.JunctionSwitchDirectionValue.setMaxCount(5)
                self.JunctionSwitchDirectionValue.setObjectName("JunctionSwitchDirectionValue")
                self.JunctionSwitchDirectionLabel = QtWidgets.QTextBrowser(self.JunctionBox)
                self.JunctionSwitchDirectionLabel.setGeometry(QtCore.QRect(20, 40, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.JunctionSwitchDirectionLabel.setFont(font)
                self.JunctionSwitchDirectionLabel.setObjectName("JunctionSwitchDirectionLabel")

                # Receiver End
                self.JunctionIsReceiverEndLabel = QtWidgets.QTextBrowser(self.JunctionBox)
                self.JunctionIsReceiverEndLabel.setGeometry(QtCore.QRect(20, 90, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.JunctionIsReceiverEndLabel.setFont(font)
                self.JunctionIsReceiverEndLabel.setObjectName("JunctionIsReceiverEndLabel")
                self.JunctionIsReceiverEndValue = QtWidgets.QLineEdit(self.JunctionBox)
                self.JunctionIsReceiverEndValue.setGeometry(QtCore.QRect(220, 90, 113, 21))
                self.JunctionIsReceiverEndValue.setText("")
                self.JunctionIsReceiverEndValue.setMaxLength(3)
                self.JunctionIsReceiverEndValue.setAlignment(QtCore.Qt.AlignCenter)
                self.JunctionIsReceiverEndValue.setReadOnly(True)
                self.JunctionIsReceiverEndValue.setClearButtonEnabled(False)
                self.JunctionIsReceiverEndValue.setObjectName("JunctionIsReceiverEndValue")

                # Traffic Light
                self.JunctionTrafficLightLabel = QtWidgets.QTextBrowser(self.JunctionBox)
                self.JunctionTrafficLightLabel.setGeometry(QtCore.QRect(20, 140, 161, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.JunctionTrafficLightLabel.setFont(font)
                self.JunctionTrafficLightLabel.setObjectName("JunctionTrafficLightLabel")
                self.JunctionTrafficLightValue = QtWidgets.QComboBox(self.JunctionBox)
                self.JunctionTrafficLightValue.setGeometry(QtCore.QRect(230, 140, 104, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.JunctionTrafficLightValue.setFont(font)
                self.JunctionTrafficLightValue.setMaxCount(3)
                self.JunctionTrafficLightValue.setObjectName("JunctionTrafficLightValue")
                #endregion Junction

                #region Station
                # Station Region
                self.StationBox = QtWidgets.QGroupBox(self.BlockStatusBox)
                self.StationBox.setGeometry(QtCore.QRect(420, 240, 351, 91))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.StationBox.setFont(font)
                self.StationBox.setObjectName("StationBox")

                # Station Name
                self.StationNameLabel = QtWidgets.QTextBrowser(self.StationBox)
                self.StationNameLabel.setGeometry(QtCore.QRect(20, 40, 121, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.StationNameLabel.setFont(font)
                self.StationNameLabel.setObjectName("StationNameLabel")
                self.StationNameValue = QtWidgets.QLineEdit(self.StationBox)
                self.StationNameValue.setGeometry(QtCore.QRect(160, 40, 171, 21))
                self.StationNameValue.setText("")
                self.StationNameValue.setAlignment(QtCore.Qt.AlignCenter)
                self.StationNameValue.setReadOnly(True)
                self.StationNameValue.setObjectName("StationNameValue")
                #endregion Station

                #region Crossing
                # Crossing Region
                self.CrossingBox = QtWidgets.QGroupBox(self.BlockStatusBox)
                self.CrossingBox.setGeometry(QtCore.QRect(420, 340, 351, 91))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.CrossingBox.setFont(font)
                self.CrossingBox.setObjectName("CrossingBox")

                # Crossing Active
                self.BlockCrossingActiveValue = QtWidgets.QComboBox(self.CrossingBox)
                self.BlockCrossingActiveValue.setGeometry(QtCore.QRect(230, 40, 104, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.BlockCrossingActiveValue.setFont(font)
                self.BlockCrossingActiveValue.setMaxCount(2)
                self.BlockCrossingActiveValue.setObjectName("BlockCrossingActiveValue")
                self.BlockCrossingActiveLabel = QtWidgets.QTextBrowser(self.CrossingBox)
                self.BlockCrossingActiveLabel.setGeometry(QtCore.QRect(20, 40, 121, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.BlockCrossingActiveLabel.setFont(font)
                self.BlockCrossingActiveLabel.setObjectName("BlockCrossingActiveLabel")
                #endregion Crossing

                #region Test Bench

                # Test Bench Box
                self.TestBenchBox = QtWidgets.QGroupBox(self.BlockStatusBox)
                self.TestBenchBox.setGeometry(QtCore.QRect(790, 40, 361, 291))
                self.TestBenchBox.setObjectName("TestBenchBox")

                # Inputs Box
                self.InputsBox = QtWidgets.QGroupBox(self.TestBenchBox)
                self.InputsBox.setGeometry(QtCore.QRect(20, 80, 321, 191))
                self.InputsBox.setObjectName("InputsBox")

                # Maintenance Active
                self.TestMaintenanceActiveLabel = QtWidgets.QTextBrowser(self.InputsBox)
                self.TestMaintenanceActiveLabel.setGeometry(QtCore.QRect(20, 90, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TestMaintenanceActiveLabel.setFont(font)
                self.TestMaintenanceActiveLabel.setObjectName("TestMaintenanceActiveLabel")
                self.TestMaintenenaceActiveValue = QtWidgets.QComboBox(self.InputsBox)
                self.TestMaintenenaceActiveValue.setGeometry(QtCore.QRect(200, 90, 104, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TestMaintenenaceActiveValue.setFont(font)
                self.TestMaintenenaceActiveValue.setMaxCount(2)
                self.TestMaintenenaceActiveValue.setObjectName("TestMaintenenaceActiveValue")

                # Track Fault Detected
                self.TestTrackFaultDetectedLabel = QtWidgets.QTextBrowser(self.InputsBox)
                self.TestTrackFaultDetectedLabel.setGeometry(QtCore.QRect(20, 40, 151, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TestTrackFaultDetectedLabel.setFont(font)
                self.TestTrackFaultDetectedLabel.setObjectName("TestTrackFaultDetectedLabel")
                self.TestTrackFaultDetectedValue = QtWidgets.QComboBox(self.InputsBox)
                self.TestTrackFaultDetectedValue.setGeometry(QtCore.QRect(200, 40, 104, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TestTrackFaultDetectedValue.setFont(font)
                self.TestTrackFaultDetectedValue.setMaxCount(2)
                self.TestTrackFaultDetectedValue.setObjectName("TestTrackFaultDetectedValue")

                # Block Occupied
                self.TestBlockOccupiedLabel = QtWidgets.QTextBrowser(self.InputsBox)
                self.TestBlockOccupiedLabel.setGeometry(QtCore.QRect(20, 140, 121, 31))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TestBlockOccupiedLabel.setFont(font)
                self.TestBlockOccupiedLabel.setObjectName("TestBlockOccupiedLabel")
                self.TestBlockOccupiedValue = QtWidgets.QComboBox(self.InputsBox)
                self.TestBlockOccupiedValue.setGeometry(QtCore.QRect(200, 140, 104, 26))
                font = QtGui.QFont()
                font.setFamily("Arial")
                self.TestBlockOccupiedValue.setFont(font)
                self.TestBlockOccupiedValue.setMaxCount(2)
                self.TestBlockOccupiedValue.setObjectName("TestBlockOccupiedValue")

                # Activate button
                self.TestBenchActivateButton = QtWidgets.QPushButton(self.TestBenchBox)
                self.TestBenchActivateButton.setGeometry(QtCore.QRect(40, 40, 113, 32))
                self.TestBenchActivateButton.setObjectName("TestBenchActivateButton")

                # Deactivate Button
                self.TestBenchDeactivateButton = QtWidgets.QPushButton(self.TestBenchBox)
                self.TestBenchDeactivateButton.setGeometry(QtCore.QRect(190, 40, 113, 32))
                self.TestBenchDeactivateButton.setObjectName("TestBenchDeactivateButton")

                #endregion Test Bench

                
                SWWaysideModule.setCentralWidget(self.centralwidget)

                self.retranslateUi(SWWaysideModule)
                QtCore.QMetaObject.connectSlotsByName(SWWaysideModule)

                #endregion User Area

        def retranslateUi(self, SWWaysideModule):
                _translate = QtCore.QCoreApplication.translate
                SWWaysideModule.setWindowTitle(_translate("SWWaysideModule", "SW Wayside"))
                self.TrackMapViewButton.setText(_translate("SWWaysideModule", "View Track Map"))
                self.OperationModeValue.setItemText(0, _translate("SWWaysideModule", "Manual"))
                self.OperationModeValue.setItemText(1, _translate("SWWaysideModule", "Automatic"))
                self.WaysideControllerBox.setTitle(_translate("SWWaysideModule", "Wayside Controller"))
                self.WaysideControllerUploadPLCProgramButton.setText(_translate("SWWaysideModule", "Upload PLC Program"))
                self.BlockStatusBox.setTitle(_translate("SWWaysideModule", "Block Status"))
                self.GeneralBox.setTitle(_translate("SWWaysideModule", "General"))
                self.BlockTypeLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Block Type</span></p></body></html>"))
                self.BlockOccupancyLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Block Occupied</span></p></body></html>"))
                self.MaintenanceBox.setTitle(_translate("SWWaysideModule", "Maintenance"))
                self.MaintenanceTrackFaultLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Track Fault Detected</span></p></body></html>"))
                self.MaintenanceActiveLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Maintenance Active</span></p></body></html>"))
                self.StationBox.setTitle(_translate("SWWaysideModule", "Station"))
                self.StationNameLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Station Name</span></p></body></html>"))
                self.CrossingBox.setTitle(_translate("SWWaysideModule", "Crossing"))
                self.BlockCrossingActiveLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Crossing Active</span></p></body></html>"))
                self.JunctionBox.setTitle(_translate("SWWaysideModule", "Junction"))
                self.JunctionSwitchDirectionLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Switch Direction</span></p></body></html>"))
                self.JunctionIsReceiverEndLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Is Receiver End</p></body></html>"))
                self.JunctionTrafficLightLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Traffic Light Color</span></p></body></html>"))
                self.TestBenchBox.setTitle(_translate("SWWaysideModule", "Test Bench"))
                self.InputsBox.setTitle(_translate("SWWaysideModule", "Inputs"))
                self.TestMaintenanceActiveLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Maintenance Active</span></p></body></html>"))
                self.TestTrackFaultDetectedLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Track Fault Detected</span></p></body></html>"))
                self.TestBlockOccupiedLabel.setHtml(_translate("SWWaysideModule", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Arial\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.AppleSystemUIFont\';\">Block Occupied</span></p></body></html>"))
                self.TestBenchActivateButton.setText(_translate("SWWaysideModule", "Activate"))
                self.TestBenchDeactivateButton.setText(_translate("SWWaysideModule", "Deactivate"))
                self.SystemInfoButton.setText(_translate("SWWaysideModule", "System Info"))
                self.SystemSpeedValue.setSuffix(_translate("SWWaysideModule", " x"))
                self.SystemClockValue.setDisplayFormat(_translate("SWWaysideModule", "h:mm"))
                self.SystemSpeedLabel.setText(_translate("SWWaysideModule", "System Speed:"))
                self.SystemClockLabel.setText(_translate("SWWaysideModule", "System Clock:")) 

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = SWWaysideModuleUI()
        app.exec()
