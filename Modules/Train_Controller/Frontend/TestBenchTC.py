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
        uic.loadUi("Modules/Train_Controller/Frontend/TCtestbenchUI.ui", self)
        self.trainController = trainController()
        self.Timer = QTimer()
        self.Timer.timeout.connect(signals.train_controller_update_backend)
        self.Timer.timeout.connect(self.timerHandler)
        self.Timer.start(INTERVAL)

        #Train Controller Signals
        #lights
        signals.train_controller_int_lights_on.connect(self.displayIntLights)
        signals.train_controller_int_lights_off.connect(self.displayIntLights)
        signals.train_controller_ext_lights_on.connect(self.displayExtLights)
        signals.train_controller_ext_lights_off.connect(self.displayExtLights)
        # #doors
        signals.train_controller_right_door_closed.connect(self.displayRDoors)
        signals.train_controller_right_door_open.connect(self.displayRDoors)
        signals.train_controller_left_door_closed.connect(self.displayLDoors)
        signals.train_controller_left_door_open.connect(self.displayLDoors)
        # #Bower
        signals.train_controller_send_power_command.connect(self.powerDisplay)
        # #Temperature
        signals.train_controller_temperature_value.connect(self.tempDisplay)
        # #Braking
        signals.train_controller_service_brake.connect(self.displayServiceBrake)
        signals.train_controller_emergency_brake_on.connect(self.displayEBrake)
        signals.train_controller_emergency_brake_off.connect(self.displayEBrake)

        #train model signals
        # signals.trainModel_send_engine_failure.connect(self.displayEngineFailure)
        # signals.trainModel_send_signal_failure.connect(self.displaySignalFailure)
        # signals.trainModel_send_brake_failure.connect(self.displayBrakeFailure)
        # signals.trainModel_send_actual_velocity.connect(self.displayCurrentSpeed)
        # signals.trainModel_send_emergency_brake.connect(self.updateEBrake)


        #inputs for test bench
        # self.automaticButton.clicked.connect(self.automaticButtonClicked)
        # self.manualButton.clicked.connect(self.manaulButtonClicked)
        # self.driverThrottle.valueChanged.connect(self.commandedSpeedReceive)
        # self.tb_eBrake.valueChanged.connect(self.eBrakeRecieve)
        # self.tb_serviceBrake.valueChanged.connect(self.serviceBrakeRecieve)
        # self.curSpeedVal.textChanged.connect(self.currentSpeedReceive)

        self.send_button.clicked.connect(self.sendValues)

    
        self.show()

    def timerHandler(self):
        self.comPowerVal.setText(format(self.trainController.commandedPower, '.2f'))
        self.authorityVal.setText(format(self.trainController.authority, '.2f'))
        self.curSpeedVal.setText(format(self.trainController.currentSpeed, '.2f'))

    #function send values to backend
    def sendValues(self):
        self.trainController.engineFail = self.tb_engineFail.isChecked()
        self.trainController.brakeFail = self.tb_brakeFail.isChecked()
        self.trainController.signalFail = self.tb_signalFail.isChecked()
        self.trainController.KP = self.tb_KP.value()
        self.trainController.KI = self.tb_KI.value()
        self.trainController.Rdoor = self.tb_RDoorClosed.value()
        self.trainController.Ldoor = self.tb_LDoorClosed.value()
        self.trainController.intLights = self.tb_intLightsOn.value()
        self.trainController.extLights = self.tb_extLightOn.value()

        if self.tb_serviceBrake.value() == 1:
            self.trainController.serviceBrake = True
        else:
            self.trainController.serviceBrake = False

        if self.tb_eBrake.value() == 1:
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

    #recieved functions

    def eBrakeRecieve(self, value):
        self.trainController.emergencyBrake = value

    def serviceBrakeRecieve(self, value):
        self.trainController.serviceBrake = value

    def kpRecieve(self, value):
        self.trainController.KP = value

    def kiRecieve(self, value):
        self.trainController.KI = value

    def rightDoorRecieve(self, value):
        self.trainController.Rdoor = value

    def leftDoorRecieve(self, value):
        self.trainController.Ldoor = value

    def intLightsRecieve(self, value):
        self.trainController.intLights = value

    def extLightsRecieve(self, value):
        self.trainController.extLights = value

    def tempReceive(self, value):
        self.trainController.trainTemp = value

    def engineFailReceive(self, value):
        self.trainController.engineFail = value
    
    def signalFailReceive(self, value):
        self.trainController.signalFail = value
    
    def brakeFailReceive(self, value):
        self.trainController.brakeFail = value

    def authorityReceive(self, value):
        self.trainController.authority = value

    def currentSpeedReceive(self, value):
        self.trainController.currentSpeed = value

    def commandedSpeedReceive(self, value):
        self.trainController.commandedSpeed = value

    def powerReceive(self, value):
        self.trainController.commandedPower = value


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
        self.authorityVal.setText(str(authority * 3.28, '.2f'))

    def tempDisplay(self, temp):
        self.tempVal.setValue(temp)

    def displayKP(self, kp):
        self.KPVal.setValue(kp)

    def displayKI(self, ki):
        self.KIVal.setValue(ki)

    def displayEBrake(self, value):
        if value:
            self.emergencyBrake.valueChanged(1)
        else:
            self.emergencyBrake.valueChanged(0)

    def displayServiceBrake(self, value):
        if value:
            self.serviceBrake.valueChanged(1)
        else:
            self.serviceBrake.valueChanged(0)

    def displayIntLights(self, value):
        if value:
            self.intLightButton.accepted()
        else:
            self.intLightButton.rejected()

    def displayExtLights(self, value):
        if value:
            self.extLightButton.accepted()
        else:
            self.extLightButton.rejected()

    def displayRDoors(self, value):
        if value:
            self.rightDoorButton.accepted()
        else:
            self.rightDoorButton.rejected()

    def displayLDoors(self, value):
        if value:
            self.leftDoorButton.accepted()
        else:
            self.leftDoorButton.rejected()
    

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainControllerUI()
    app.exec()