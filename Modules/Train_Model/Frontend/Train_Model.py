from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.Train import Train, trains
from signals import signals

class TrainModel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_UI.ui", self)
        signals.trainModel_backend_update.connect(self.UIUpdate)
        signals.trainModel_update_beacon_UI.connect(self.updateBeacon)
        self.trainSelectComboBox.currentIndexChanged.connect(self.trainSelect)
        
        self.currentTrain = None
        self.trainSelectComboBox.addItem("< select train >")
        for key, value in trains.items():
            self.trainSelectComboBox.addItem(f"ID: {key}")
            self.trainSelectComboBox.setItemData(self.trainSelectComboBox.count() - 1, value)
        

    def UIUpdate(self):
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
        self.eBrakeSelect.setEnabled(self.trainSelectComboBox.currentIndex())
        self.sBrakeDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.lengthDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.widthDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.heightDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.massDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.velocityDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.accelDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
        self.beaconDisplay.setEnabled(self.trainSelectComboBox.currentIndex())
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
                self.eBrakeSelect.setCurrentIndex(1)
            else:
                self.eBrakeSelect.setCurrentIndex(0)
                
            self.lengthDisplay.setText(format(self.currentTrain.length * 3.281, '.2f')) # m * 3.281 = ft
            self.widthDisplay.setText(format(self.currentTrain.width * 3.281, '.2f'))
            self.heightDisplay.setText(format(self.currentTrain.height * 3.281, '.2f'))
            self.massDisplay.setText(format(self.currentTrain.mass * 2.205, '.2f')) # kg * 2.205 = lb
            self.velocityDisplay.setText(format(self.currentTrain.currentSpeed * 2.237, '.2f')) # m/s * 2.237 = mph
            self.accelDisplay.setText(format(self.currentTrain.currentAccel * 3.281, '.2f')) # m/s^2 * 3.281 = ft/s^2
            
            
    def updateBeacon(self, value):
        self.beaconDisplay.append(value)
        
    def trainSelect(self, idx):
        self.currentTrain = self.trainSelectComboBox.itemData(idx)
        
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModel()
    window.show()
    sys.exit(app.exec())