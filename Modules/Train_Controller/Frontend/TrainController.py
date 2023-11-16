#Frontend Implementation for CTC Office

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from signals import *
from Modules.Train_Controller.Backend.Train_Controller import *


INTERVAL = 50

##main module setup
class TrainControllerUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Controller/Frontend/TrainControllerUI.ui", self)
        self.trainController = trainController()
        self.testingTimer = QTimer()
        self.testingTimer.timeout.connect(signals.train_controller_update_backend)
        self.testingTimer.timeout.connect(self.timerHandler)
        self.testingTimer.start(INTERVAL)

        #signals.train_controller_update_frontend.connect(self.update_frontend)
        self.intLightsButton.accepted.connect(self.displayIntLightsOn)

        self.intLightsButton.rejected.connect(self.displayIntLightsOff)

        self.extLightsButton.accepted.connect(self.displayExtLightsOn)

        self.extLightsButton.rejected.connect(self.displayExtLightsOff)

        self.rightDoorButton.accepted.connect(self.displayRDoorsClosed)

        self.rightDoorButton.rejected.connect(self.displayRDoorsOpen)

        self.leftDoorButton.accepted.connect(self.displayLDoorsClosed)
        
        self.leftDoorButton.rejected.connect(self.displayLDoorsOpen)

        self.send_button.clicked.connect(self.sendValues)

        signals.train_controller_int_lights_on.connect(self.displayIntLightsOn)
        signals.train_controller_int_lights_off.connect(self.displayIntLightsOff)
        signals.train_controller_ext_lights_on.connect(self.displayExtLightsOn)
        signals.train_controller_ext_lights_off.connect(self.displayExtLightsOff)
        #doors
        signals.train_controller_right_door_closed.connect(self.displayRDoorsClosed)
        signals.train_controller_right_door_open.connect(self.displayRDoorsOpen)
        signals.train_controller_left_door_closed.connect(self.displayLDoorsClosed)
        signals.train_controller_left_door_open.connect(self.displayLDoorsOpen)
        #Bower
        signals.train_controller_send_power_command.connect(self.powerDisplay)
        #Temperature
        signals.train_controller_temperature_value.connect(self.tempDisplay)
        #Braking
        signals.train_controller_service_brake.connect(self.displayServiceBrake)
        signals.train_controller_emergency_brake_on.connect(self.displayEBrakeOn)
        signals.train_controller_emergency_brake_off.connect(self.displayEBrakeOff)
    
    def timerHandler(self):
        self.comPowerVal.setText(format(self.trainController.commandedPower, '.2f'))
        self.authorityVal.setText(format(self.trainController.authority, '.2f'))
        self.curSpeedVal.setText(format(self.trainController.currentSpeed, '.2f'))
        
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

    #function for emergency brakes
    def updateEBrake(self, value):
        if value:
            self.emergencyBrake.valueChanged(1)
        else:
            self.emergencyBrake.valueChanged(0)

    #function for service brakes
    def updateServiceBrake(self, value):
        if value:
            self.serviceBrake.valueChanged(1)
        else:
            self.serviceBrake.valueChanged(0)
            
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
    def updateIntLights(self, value):
        if value:
            self.intLightButton.accepted()
        else:
            self.intLightButton.rejected()

    #function will toggle ext lights
    def updateExtLights(self, value):
        if value:
            self.extLightButton.accepted()
        else:
            self.extLightButton.rejected()

    #function - right doors closed
    def updateRDoors(self, value):
        if value:
            self.rightDoorButton.accpeted()
        else:
            self.rightDoorButton.rejected()

    #function - left doors closed
    def updateLDoors(self, value):
        if value:
            self.leftDoorButton.accepted()
        else:
            self.leftDoorButton.rejected()

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
    app.exec()