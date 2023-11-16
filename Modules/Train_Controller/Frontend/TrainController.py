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
        self.Timer = QTimer()
        self.Timer.timeout.connect(signals.train_controller_backend_update)
        self.Timer.timeout.connect(self.timerHandler)
        self.Timer.start(INTERVAL)

        #Train Controller Signals
        #lights
        signals.train_controller_int_lights_on.connect(self.updateIntLights)
        signals.train_controller_int_lights_off.connect(self.updateIntLights)
        signals.train_controller_ext_lights_on.connect(self.updateExtLights)
        signals.train_controller_ext_lights_off.connect(self.updateExtLights)
        # #doors
        signals.train_controller_right_door_closed.connect(self.updateRDoors)
        signals.train_controller_right_door_open.connect(self.updateRDoors)
        signals.train_controller_left_door_closed.connect(self.updateLDoors)
        signals.train_controller_left_door_open.connect(self.updateLDoors)
        # #Bower
        signals.train_controller_send_power_command.connect(self.updatePower)
        # #Temperature
        signals.train_controller_temperature_value.connect(self.updateTemp)
        # #Braking
        signals.train_controller_service_brake.connect(self.updateServiceBrake)
        signals.train_controller_emergency_brake_on.connect(self.updateEBrake)
        signals.train_controller_emergency_brake_off.connect(self.updateEBrake)

        #train model signals
        signals.trainModel_send_engine_failure.connect(self.displayEngineFailure)
        signals.trainModel_send_signal_failure.connect(self.displaySignalFailure)
        signals.trainModel_send_brake_failure.connect(self.displayBrakeFailure)
        signals.trainModel_send_actual_velocity.connect(self.displayCurrentSpeed)
        signals.trainModel_send_emergency_brake.connect(self.updateEBrake)


        #inputs for test bench
        self.automaticButton.clicked.connect(self.automaticButtonClicked)
        self.manualButton.clicked.connect(self.manaulButtonClicked)
        self.driverThrottle.valueChanged.connect(self.updateCommandedSpeed)
        self.emergencyBrake.valueChanged.connect(self.updateEBrake)
        self.serviceBrake.valueChanged.connect(self.updateServiceBrake)
        self.curSpeedVal.textChanged.connect(self.displayCurrentSpeed)

    
        self.show()

    def timerHandler(self):
        self.comPowerVal.setText(format(self.trainController.commandedPower, '.2f'))
        self.authorityVal.setText(format(self.trainController.authority, '.2f'))
        self.curSpeedVal.setText(format(self.trainController.currentSpeed, '.2f'))

    #function send values to backend
    def sendValues(self):
        self.trainController.engineFail = self.engineFailure.isChecked()
        self.trainController.brakeFail = self.brakeFailure.isChecked()
        self.trainController.signalFail = self.signalFaiure.isChecked()
        self.trainController.KP = self.KpVal
        self.trainController.KI = self.KiVal
        # self.trainController.Rdoor =
        # self.trainController.Ldoor = 
        # self.trainController.intLights = 
        # self.trainController.extLights =

        if self.serviceBrake.value() == 1:
            self.trainController.serviceBrake = True
        else:
            self.trainController.serviceBrake = False

        if self.emergencyBrake.value() == 1:
            self.trainController.emergencyBrake = True
        else:
            self.trainController.emergencyBrake = False

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