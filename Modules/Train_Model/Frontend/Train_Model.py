from PyQt6 import QtCore, QtWidgets, uic, QtGui
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.TrainList import trainList
from Modules.Train_Model.Backend.Train import Train
from signals import signals

class TrainModel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_UI.ui", self)
        signals.trainModel_backend_update.connect(self.UIUpdate)
        signals.ctc_added_train.connect(self.addTrainToBox)
        self.trainSelectComboBox.currentIndexChanged.connect(self.trainSelect)
        self.eBrakeButton.clicked.connect(self.setEBrake)
        self.signalFail.stateChanged.connect(self.sendSignalFail)
        self.brakeFail.stateChanged.connect(self.sendBrakeFail)
        self.engineFail.stateChanged.connect(self.sendEngineFail)
        
        self.ad1 = QtGui.QPixmap("Modules/Train_Model/Frontend/cokead.jpg")
        self.ad2 = QtGui.QPixmap("Modules/Train_Model/Frontend/hooverad.jpeg")
        self.ad3 = QtGui.QPixmap("Modules/Train_Model/Frontend/bbad.jpeg")
        self.ad4 = QtGui.QPixmap("Modules/Train_Model/Frontend/oldspicead.png")
        self.ad5 = QtGui.QPixmap("Modules/Train_Model/Frontend/docad.jpeg")
        self.adList = [self.ad1, self.ad2, self.ad3, self.ad4, self.ad5]
        self.adIdx = 0
        self.adDisplay.setScaledContents(True)
        self.adDisplay.setPixmap(self.ad1)
        
        self.adCounter = 40
        
        self.currentTrain = None
        self.eBrakeButton.setEnabled(False)
        self.trainSelectComboBox.addItem("< select train >")
        
    def addTrainToBox(self, id):
        train = trainList.allTrains[id]
        self.trainSelectComboBox.addItem(f"ID: {id}")
        self.trainSelectComboBox.setItemData(self.trainSelectComboBox.count() - 1, train)

    def UIUpdate(self):
        self.adCounter -= 1
        if (self.adCounter == 0):
            self.adIdx = (self.adIdx + 1) % len(self.adList)
            self.adDisplay.setPixmap(self.adList[self.adIdx])
            self.adCounter = 60
        
        if (self.currentTrain is not None):
            self.crewDisplay.setText(format(self.currentTrain.numCrew, '.0f'))
            self.passDisplay.setText(format(self.currentTrain.numPassengers, '.0f'))
            
            if (self.currentTrain.interiorLight):
                self.intLightDisplay.setText("on")
            else:
                self.intLightDisplay.setText("off")
                
            if (self.currentTrain.exteriorLight):
                self.extLightDisplay.setText("on")
            else:
                self.extLightDisplay.setText("off")
                
            if (self.currentTrain.leftDoor):
                self.leftDoorDisplay.setText("closed")
            else:
                self.leftDoorDisplay.setText("open")
                
            if (self.currentTrain.rightDoor):
                self.rightDoorDisplay.setText("closed")
            else:
                self.rightDoorDisplay.setText("open")
                
            if (self.currentTrain.serviceBrake):
                self.sBrakeDisplay.setText("on")
            else:
                self.sBrakeDisplay.setText("off")
                
            if (self.currentTrain.emergencyBrake):
                self.eBrakeButton.setEnabled(False)
            else:
                self.eBrakeButton.setEnabled(True)
                
            self.trainTempDisplay.setText(format(self.currentTrain.temperatureActual, '.0f')) # F
            self.lengthDisplay.setText(format(self.currentTrain.length * 3.281, '.2f')) # m * 3.281 = ft
            self.widthDisplay.setText(format(self.currentTrain.width * 3.281, '.2f')) # m * 3.281 = ft
            self.heightDisplay.setText(format(self.currentTrain.height * 3.281, '.2f')) # m * 3.281 = ft
            self.massDisplay.setText(format(self.currentTrain.mass * 2.205, '.2f')) # kg * 2.205 = lb
            self.velocityDisplay.setText(format(self.currentTrain.currentSpeed * 2.237, '.2f')) # m/s * 2.237 = mph
            self.accelDisplay.setText(format(self.currentTrain.currentAccel * 3.281, '.2f')) # m/s^2 * 3.281 = ft/s^2
            self.powerDisplay.setText(format(self.currentTrain.commandedPower / 745.7, '.0f')) # hp
            self.beaconDisplay.setText(self.currentTrain.currentBeacon)
            
        self.crewDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.passDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.signalFail.setEnabled(self.trainSelectComboBox.currentIndex())
        self.brakeFail.setEnabled(self.trainSelectComboBox.currentIndex())
        self.engineFail.setEnabled(self.trainSelectComboBox.currentIndex())
        self.intLightDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.extLightDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.leftDoorDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.rightDoorDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.trainTempDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.sBrakeDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.lengthDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.widthDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.heightDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.massDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.velocityDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.accelDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.powerDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.beaconDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
    def updateBeacon(self, value):
        self.beaconDisplay.append(value)
        
    def trainSelect(self, idx):
        self.currentTrain = self.trainSelectComboBox.itemData(idx)
        if isinstance(self.currentTrain, Train):
            signal_check_state = QtCore.Qt.CheckState.Checked if self.currentTrain.signalFail else QtCore.Qt.CheckState.Unchecked
            engine_check_state = QtCore.Qt.CheckState.Checked if self.currentTrain.engineFail else QtCore.Qt.CheckState.Unchecked
            brake_check_state = QtCore.Qt.CheckState.Checked if self.currentTrain.brakeFail else QtCore.Qt.CheckState.Unchecked

            self.signalFail.setCheckState(signal_check_state)
            self.engineFail.setCheckState(engine_check_state)
            self.brakeFail.setCheckState(brake_check_state)

        self.UIUpdate()
        
    def setEBrake(self):
        self.currentTrain.emergencyBrake = True
        self.eBrakeButton.setEnabled(False)
        signals.trainModel_send_emergency_brake.emit(self.currentTrain.train_id, True)
        print("button clicekd")
        
    def sendSignalFail(self, value):
        if (value):
            self.currentTrain.signalFail = True
        else:
            self.currentTrain.signalFail = False
            
    def sendBrakeFail(self, value):
        if (value):
            self.currentTrain.brakeFail = True
        else:
            self.currentTrain.brakeFail = False
            
    def sendEngineFail(self, value):
        if (value):
            self.currentTrain.engineFail = True
        else:
            self.currentTrain.engineFail = False
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModel()
    window.show()
    sys.exit(app.exec())