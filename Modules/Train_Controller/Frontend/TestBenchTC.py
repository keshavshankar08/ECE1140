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
class TestBenchTrainControllerUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Controller/Frontend/TCtestbenchUI.ui", self)
        self.trainController = trainController()
        self.testingTimer = QTimer()
        self.testingTimer.timeout.connect(signals.train_controller_update_backend)
        self.testingTimer.timeout.connect(self.timerHandler)
        self.testingTimer.start(INTERVAL)

        #signals.train_controller_update_frontend.connect(self.update_frontend)

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

    def sendValues(self):
        self.trainController.engineFail = self.tb_engineFail.isChecked()
        self.trainController.brakeFail = self.tb_brakeFail.isChecked()
        self.trainController.signalFail = self.tb_signalFail.isChecked()
        self.trainController.commandedPower = self.comPowerVal
        self.trainController.currentSpeed = self.curSpeedVal
        self.trainController.authority = self.authorityVal
        self.trainController.emergencyBrake = self.tb_eBrake
        self.trainController.serviceBrake = self.tb_serviceBrake
        
    #function for automatic mode
    def automaticButtonClicked(self):
        self.automaticButton.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.manualButton.setStyleSheet("background-color: rgb(255, 255, 255)")
        

    #function for manual mode
    def manaulButtonClicked(self):
        self.automaticButton.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.manualButton.setStyleSheet("background-color: rgb(199, 199, 199)")

    #received

    def engineFailCheckBoxReceive(self, value):
        self.trainController.engineFail = value

    def signalFailCheckBoxReceive(self, value):
        self.trainController.signalFail = value

    def brakeFailCheckBoxReceive(self, value):
        self.trainController.brakeFail = value

    def authorityReceive(self, value):
        self.trainController.authority = value
    
    def currentSpeedReceive(self, value):
        self.trainController.currentSpeed = value
    
    def kpReceive(self, value):
        self.trainController.KP = value

    def kiReceive(self, value):
        self.trainController.KI = value

    #displays

    def engineFailDisplay(self, value):
        self.engineFailure.setChecked(value)
        
    def signalFailDisplay(self, value):
        self.signalFailure.setChecked(value)
        
    def brakeFailDisplay(self, value):
        self.brakeFailure.setChecked(value)
    
    def currentSpeedDisplay(self, value):
        self.curSpeedVal.setText(format(value * 2.237, '.2f'))

    def powerDisplay(self, value):
        self.comPowerVal.setText(format(value * 2.237, '.2f'))

    def authorityDisplay(self, authority):
        self.authorityVal.setText(format(authority * 3.28, '.2f'))

    def tempDisplay(self, temp):
        self.tempVal.setValue(temp)

    def displayKP(self, kp, ki):
        self.KPVal.setValue(kp)
        self.KIVal.setValue(ki)

    def displayEBrakeOn(self, value):
        self.emergencyBrake.valueChanged(value)

    def displayEBrakeOff(self, value):
        self.emergencyBrake.valueChanged(value)

    def displayServiceBrake(self, value):
        if value:
            self.serviceBrake.valueChanged(1)
        else:
            self.serviceBrake.valueChanged(0)

    def displayIntLightsOn(self):
        self.intLightButton.accepted()

    def displayIntLightsOff(self):
        self.intLightButton.rejected()

    def displayExtLightsOn(self):
        self.extLightButton.accepted()

    def displayExtLightsOff(self):
        self.extLightButton.rejected()

    def displayRDoorsClosed(self):
        self.rightDoorButton.accepted()

    def displayRDoorsOpen(self):
        self.rightDoorButton.rejected()

    def displayLDoorsClosed(self):
        self.leftDoorButton.accepted()

    def displayLDoorsOpen(self):
        self.leftDoorButton.rejected()

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TestBenchTrainControllerUI()
    window.show()
    sys.exit(app.exec())