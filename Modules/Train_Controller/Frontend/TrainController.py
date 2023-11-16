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


        #signals.train_controller_update_frontend.connect(self.update_frontend)
        
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
        self.driverThrottle.valueChanged.connect(self.receiveDriverThrottle)
    
    def timerHandler(self):
        self.comPowerVal.setText(format(self.trainController.commandedPower, '.2f'))
        self.authorityVal.setText(format(self.trainController.authority, '.2f'))
        self.curSpeedVal.setText(format(self.trainController.currentSpeed, '.2f'))
        if (self.trainController.emergencyBrake):
            self.emergencyBrake.setValue(1)
        else:
            self.emergencyBrake.setValue(0)

    # def update_frontend(self):
    #     self.trainController.KP = self.tb_KP
    #     self.trainController.KI = self.tb_KI
    #     self.trainController.trainTemp = self.tb_tempVal
    #     self.trainController.commandedSpeed = self.tb_comSpeed
    #     self.trainController.emergencyBrake = self.tb_eBrake
    #     self.trainController.serviceBrake = self.tb_serviceBrake
    #     self.trainController.mode = True
    #     self.trainController.Rdoor = self.tb_RDoorClosed
    #     self.trainController.Ldoor = self.tb_LDoorClosed
    #     self.trainController.intLights = self.tb_intLightsOn
    #     self.trainController.extLights = self.tb_extLightOn
        
    # def send_frontend_update(self):
    #     signals.train_controller_update_frontend.emit(self.trainController.KP, self.trainController.KI, self.trainController.trainTemp, 
    #                                                   self.trainController.commandedSpeed, self.trainController.emergencyBrake, self.trainController.serviceBrake, 
    #                                                   self.trainController.mode, self.trainController.Rdoor, self.trainController.Ldoor, 
    #                                                     self.trainController.intLights, self.trainController.extLights)

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

    #function for emergency brakes
    def eBrake(self, value):
        if (value == 1):
            self.trainController.emergencyBrakeOn()
            
        else:
            self.trainController.emergencyBrakeOff()
            
    def driverThrottleUpdate(self):
        self.comSpeedVal.setText(str(self.driverThrottle.value()))

    def updateEBrake(self, value):
        if value:
            self.emergencyBrake.setValue(1)
        else:
            self.emergencyBrake.setValue(0)

    # def eBrakeOn(self):
    #     self.emergencyBrake.setValue(1)

    # def eBrakeOff(self):
    #     self.emergencyBrake.setValue(0)
 
    #function for service brakes
    def updateServiceBrake(self, value):
        if value:
            self.serviceBrake.setValue(1)
        else:
            self.serviceBrake.setValue(0)
            
    #function will display the current speed
    def displayCurrentSpeed(self, speed):
        self.trainController.currentSpeed = speed

    #function will update commanded speed
    def updateCommandedSpeed(self, value):
        self.trainController.commandedSpeed = value

    #function will display Kp and Ki
    def displayKPKI(self, kp, ki):
        self.KPVal.setValue(kp)
        self.KIVal.setValue(ki)

    #function display power
    def updatePower(self, power):
        self.comPowerVal.setText(str(power))

    #function displays authority
    def updateAuthority(self, authority):
        self.authorityVal.setText(str(authority))

    #function will toggle int lights
    def intLightsOn(self):
            self.intLightOn.setStyleSheet("background-color: green;")
            self.intLightOff.setStyleSheet("background-color: white;")
            self.trainController.intLights = True

    def intLightsOff(self):
            self.intLightOn.setStyleSheet("background-color: white;")
            self.intLightOff.setStyleSheet("background-color: green;")
            self.trainController.intLights = False

    #function will toggle ext lights
    def extLightsOn(self):
        self.extLightOn.setStyleSheet("background-color: green;")
        self.extLightOff.setStyleSheet("background-color: white;")
        self.trainController.extLights = True

    def extLightsOff(self):
        self.extLightOn.setStyleSheet("background-color: white;")
        self.extLightOff.setStyleSheet("background-color: green;")
        self.trainController.extLights = False

    #function - right doors closed
    def rDoorsClosed(self):
        self.rightDoorClosed.setStyleSheet("background-color: green;")
        self.rightDoorOpen.setStyleSheet("background-color: white;")
        self.trainController.Rdoor = True

    def rDoorsOpen(self):
        self.rightDoorClosed.setStyleSheet("background-color: white;")
        self.rightDoorOpen.setStyleSheet("background-color: green;")
        self.trainController.Rdoor = False

    #function - left doors closed
    def lDoorsClosed(self):
        self.leftDoorClosed.setStyleSheet("background-color: green;")
        self.leftDoorOpen.setStyleSheet("background-color: white;")
        self.trainController.Ldoor = True

    def lDoorsOpen(self):
        self.leftDoorClosed.setStyleSheet("background-color: white;")
        self.leftDoorOpen.setStyleSheet("background-color: green;")
        self.trainController.Ldoor = False

    #function updates temp
    def updateTemp(self, temp):
        self.tempVal.setValue(temp)

    #function will display engine failure
    def displayEngineFailure(self, value):
        self.engineFailure.setChecked(value)

    #function will display brake failure
    def displayBrakeFailure(self, value):
        self.brakeFailure.setChecked(value)

    #function will display signal failure
    def displaySignalFailure(self, value):
        self.signalFailure.setChecked(value)
    

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
    window.show()
    app.exec()