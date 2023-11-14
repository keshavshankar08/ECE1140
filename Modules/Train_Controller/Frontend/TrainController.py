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
        #self.Timer.timeout.connect(signals.main_backend_update_values)
        #self.Timer.timeout.connect(self.TimerHandler)
        # self.testingTimer.start(INTERVAL)


        #Train Controller Signals
        #lights
        # train_controller_int_lights_on.connect()
        # train_controller_int_lights_off.connect()
        # train_controller_ext_lights_on.connect()
        # train_controller_ext_lights_off.connect()
        # #doors
        # train_controller_right_door_closed.connect()
        # train_controller_right_door_open.connect()
        # train_controller_left_door_closed.connect()
        # train_controller_left_door_open.connect()
        # #Bower
        # train_controller_send_power_command.connect()
        # #Temperature
        # train_controller_temperature_value.connect()
        # #Braking
        # train_controller_service_brake.connect()
        # train_controller_emergency_brake_on.connect()
        # train_controller_emergency_brake_off.connect()

        #train model signals
        # signals.trainModel_send_engine_failure.connect(self.engineFailCheckBoxDisplay)
        # signals.trainModel_send_signal_failure.connect(self.signalFailCheckBoxDisplay)
        # signals.trainModel_send_brake_failure.connect(self.brakeFailCheckBoxDisplay)
        signals.trainModel_send_actual_velocity.connect(self.displayCurrentSpeed)
        signals.trainModel_send_emergency_brake.connect(self.updateEBrake)


        #inputs for test bench
        self.automaticButton.clicked.connect(self.automaticButtonClicked)
        self.manualButton.clicked.connect(self.manaulButtonClicked)
        self.leftDoorClosed.clicked.connect(self.closeLDoors)
        self.rightDoorClosed.clicked.connect(self.closeRDoors)
        # self.engineFailure.stateChanged.connect(self.displayEngineFailure)
        # self.signalFailure.stateChanged.connect(self.displaySignalFailure)
        # self.brakeFailure.stateChanged.connect(self.displayBrakeFailure)
        


        #self.driverSpeedChanged.valueChanged.connect()
        #self.serviceBrakeChanged.valueChanged.connect()
    
        self.show()

    def timeHandler(self):
        pass

    #function send values to backend
    def sendValues(self):
        self.trainController.engineFail = self.engineFailure.isChecked()
        self.trainController.brakeFail = self.brakeFailure.isChecked()
        self.trainController.signalFail = self.signalFaiure.isChecked()
        self.trainController.commandedSpeed = self.driverThrottle.value()
        self.trainController.trainTemp = self.tempVal

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
        self.curSpeedVal.setText(str(speed))

    #function will display Kp and Ki
    def displayKPKI(self, kp, ki):
        self.KPVal.value()
        self.KIVal.value()

    #function display power
    def updatePower(self, power):
        self.comPowerVal.setText(str(self.trainController.commandedPower))

    #function displays authority
    def updateAuthority(self, authority):
        pass

    #function will toggle int lights
    def updateIntLights(self, value):
        if value:
            self.intLightOn.setStyleSheet("background-color: green")
            self.intLightOff.setStyleSheet("background-color: white")
        else:
            self.intLightOn.setStyleSheet("background-color: white")
            self.intLightOff.setStyleSheet("background-color: green")

    #function will toggle ext lights
    def updateExtLights(self, value):
        pass

    #function - right doors closed
    def closeRDoors(self, value):
        pass

    #function - left doors closed
    def closeLDoors(self, value):
        pass

    #function updates temp
    def updateTemp(self, temp):
        pass

    # #function will display engine failure
    # def displayEngineFailure(self, value):
    #     self.engineFailure.setChecked(value)

    # #function will display brake failure
    # def displayBrakeFailure(self, value):
    #     self.brakeFailure.setChecked(value)

    # #function will display signal failure
    # def displaySignalFailure(self, value):
    #     self.signalFailure.setChecked(value)
    

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