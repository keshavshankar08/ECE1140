#Frontend Implementation for CTC Office

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from signals import *
from Modules.Train_Controller.Backend.Train_Controller import *


##main module setup
class TrainControllerUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Controller/Frontend/TrainControllerUI.ui", self)
        self.trainController = trainController()
        signals.train_controller_update_backend.connect(self.timerHandler)
        
        self.automaticButton.clicked.connect(self.automaticButtonClicked)
        self.manualButton.clicked.connect(self.manaulButtonClicked)
        self.intLightOn.clicked.connect(self.intLightsOn)
        self.intLightOff.clicked.connect(self.intLightsOff)
        self.extLightOn.clicked.connect(self.extLightsOn)
        self.extLightOff.clicked.connect(self.extLightsOff)
        self.rightDoorClosed.clicked.connect(self.rDoorsClosed)
        self.rightDoorOpen.clicked.connect(self.rDoorsOpen)
        self.leftDoorClosed.clicked.connect(self.lDoorsClosed)
        self.leftDoorOpen.clicked.connect(self.lDoorsOpen)
        self.KPVal.valueChanged.connect(self.displayKP)
        self.KIVal.valueChanged.connect(self.displayKI)
        
        '''
        #Bower
        signals.train_controller_send_power_command.connect(self.updatePower)
        #Temperature
        signals.train_controller_temperature_value.connect(self.updateTemp)
        #Braking
        signals.train_controller_service_brake.connect(self.updateServiceBrake)
        signals.train_controller_emergency_brake_on.connect(self.eBrakeOn)
        signals.train_controller_emergency_brake_off.connect(self.eBrakeOff)
        '''
        self.emergencyBrake.valueChanged.connect(self.eBrake)
        self.serviceBrake.valueChanged.connect(self.sBrake)
        self.driverThrottle.valueChanged.connect(self.receiveDriverThrottle)
    
    def timerHandler(self):
        self.comPowerVal.setText(format(self.trainController.commandedPower, '.2f'))
        self.authorityVal.setText(format(self.trainController.authority, '.2f'))
        self.curSpeedVal.setText(format(self.trainController.currentSpeed, '.2f'))

        if (self.trainController.emergencyBrake):
            self.emergencyBrake.setValue(1)
        else:
            self.emergencyBrake.setValue(0)

        if (self.trainController.serviceBrake):
            self.serviceBrake.setValue(1)
        else:
            self.serviceBrake.setValue(0)
        
        self.KPVal.setValue(self.trainController.KP)
        self.KIVal.setValue(self.trainController.KI)
        self.tempVal.textFromValue(self.trainController.trainTemp)

    #function for automatic mode
    def automaticButtonClicked(self):
        self.automaticButton.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.manualButton.setStyleSheet("background-color: rgb(255, 255, 255)")
        
    #function for manual mode
    def manaulButtonClicked(self):
        self.automaticButton.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.manualButton.setStyleSheet("background-color: rgb(199, 199, 199)")    

    def receiveDriverThrottle(self, value):
        self.trainController.commandedSpeed = value
        self.comSpeedVal.setText(str(self.trainController.commandedSpeed))

    #function for emergency brakes
    def eBrake(self, value):
        if (value == 1):
            self.trainController.emergencyBrakeOn()
        else:
            self.trainController.emergencyBrakeOff()

    def sBrake(self, value):
        if value == 1:
            self.trainController.serviceBrakeOn()
        else:
            self.trainController.serviceBrakeOff()

    #function will display the current speed
    def displayCurrentSpeed(self, speed):
        self.trainController.currentSpeed = speed
        self.curSpeedVal.setText(format(self.trainController.currentSpeed, '.2f'))

    #function will display Kp and Ki
    def displayKP(self, kp):
        self.trainController.KP = kp
        self.KPVal.setValue(self.trainController.KP)

    def displayKI(self, ki):
        self.trainController.KI = ki
        self.KIVal.setValue(self.trainController.KI)

    #function display power
    def updatePower(self, power):
        self.trainController.commandedPower = power
        self.comPowerVal.setText(str(self.trainController.commandedPower))

    #function displays authority
    def updateAuthority(self, authority):
        self.trainController.authority = authority
        self.authorityVal.setText(str(self.trainController.authority))

    #function will toggle int lights
    def intLightsOn(self):
            self.intLightOn.setStyleSheet("background-color: green;")
            self.intLightOff.setStyleSheet("background-color: white;")
            self.trainController.onInteriorLights()

    def intLightsOff(self):
            self.intLightOn.setStyleSheet("background-color: white;")
            self.intLightOff.setStyleSheet("background-color: green;")
            self.trainController.offInteriorLights()

    #function will toggle ext lights
    def extLightsOn(self):
        self.extLightOn.setStyleSheet("background-color: green;")
        self.extLightOff.setStyleSheet("background-color: white;")
        self.trainController.onExteriorLights()

    def extLightsOff(self):
        self.extLightOn.setStyleSheet("background-color: white;")
        self.extLightOff.setStyleSheet("background-color: green;")
        self.trainController.offExteriorLights()

    #function - right doors closed
    def rDoorsClosed(self):
        self.rightDoorClosed.setStyleSheet("background-color: green;")
        self.rightDoorOpen.setStyleSheet("background-color: white;")
        self.trainController.closeRightDoors()

    def rDoorsOpen(self):
        self.rightDoorClosed.setStyleSheet("background-color: white;")
        self.rightDoorOpen.setStyleSheet("background-color: green;")
        self.trainController.openRightDoors()

    #function - left doors closed
    def lDoorsClosed(self):
        self.leftDoorClosed.setStyleSheet("background-color: green;")
        self.leftDoorOpen.setStyleSheet("background-color: white;")
        self.trainController.closeLeftDoors()

    def lDoorsOpen(self):
        self.leftDoorClosed.setStyleSheet("background-color: white;")
        self.leftDoorOpen.setStyleSheet("background-color: green;")
        self.trainController.openLeftDoors()

    #function updates temp
    def updateTemp(self, temp):
        self.trainController.trainTemp = temp
        self.tempVal.textFromValue(self.trainController.trainTemp)

    #function will display engine failure
    def displayEngineFailure(self, value):
        self.engineFailure.setChecked(value)

    #function will display brake failure
    def displayBrakeFailure(self, value):
        self.brakeFailure.setChecked(value)

    #function will display signal failure
    def displaySignalFailure(self, value):
        self.signalFailure.setChecked(value)
    
            
#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainControllerUI()
    window.show()
    app.exec()