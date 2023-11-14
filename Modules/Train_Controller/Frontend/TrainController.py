#Frontend Implementation for CTC Office

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import sys

INTERVAL = 50

##main module setup
class TrainControllerUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Controller/Frontend/TrainControllerUI.ui", self)
        # self.testController = trainController()
        # self.testingTimer = QTimer()
        # self.testingTimer.timeout.connect(self.testController.TrainModelUpdateValues)
        # self.testingTimer.start(INTERVAL)
        # self.velocitySelect.valueChanged.connect(self.changeVelocity)
        # self.tb_beaconEntry.textChanged.connect(self.displayBeacon)


        #inputs for test bench
        self.automaticButton.clicked.connect(self.Automatic_Button_clicked)
        self.manualButton.clicked.connect(self.Manual_Button_clicked)

        self.emergencyButton.setCheckable(True)
        self.emergencyButton.clicked.connect(self.Emergency_Button_clicked)

        #self.driverSpeedChanged.valueChanged.connect()
        #self.serviceBrakeChanged.valueChanged.connect()
    
        self.show()

    #function for automatic mode
    def Automatic_Button_clicked(self):
        self.automaticButton.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.manualButton.setStyleSheet("background-color: rgb(255, 255, 255)")

    #function for manual mode
    def Manual_Button_clicked(self):
        self.automaticButton.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.manualButton.setStyleSheet("background-color: rgb(199, 199, 199)")    

    #function for emergency brakes
    def Emergency_Button_clicked(self):
        pass
            

    #function will display the current speed
    def displayCurrentSpeed(self,value):
        pass

    #function will display the commanded speed
    def displayCommandedSpeed(self, value):
        pass

    #function will display Kp and Ki
    def displayKPKI(self, ki, kp):
        pass

    #function will toggle int lights
    def updateIntLights(self, value):
        pass

    #function will toggle ext lights
    def updateExtLights(self, value):
        pass

    #function will toggle right doors
    def updateRDoors(self, value):
        pass

    #function will toggle left doors
    def updateLDoors(self, value):
        pass

    #function will update temp value
    def updateTempValue(self, value):
        pass
    

    #functions for Qspinbox to text
    # def UpdateValueAuthority(self):
    #     self.authority_val.setText(str(self.authorityinput.value()))

    # def UpdateValueComSpeed(self):
    #     self.ComSpeed_val.setText(str(self.commandedspeedinput.value()))

    # def UpdateValueComPower(self):
    #     self.ComPower_val.setText(str(self.commandedpowerinput.value()))

    # def UpdateValueKI(self):
    #     self.KI_val.setText(str(self.KIinput.value()))

    # def UpdateValueKP(self):
    #     self.KP_val.setText(str(self.Kpinput.value()))

    # def UpdateValueDriverSpeed(self):
    #     self.Curspeed_val.setText(str(self.driverspeedinput.value()))

    
            
#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainControllerUI()
    app.exec()