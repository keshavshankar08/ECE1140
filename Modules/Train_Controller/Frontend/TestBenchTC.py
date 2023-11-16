#Frontend Implementation for Train Controller

from PyQt6 import QtWidgets, uic
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
        self.intLightsButton.clicked.connect(self.displayIntLightsOn)

        self.intLightsButton.clicked.connect(self.displayIntLightsOff)

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

    def sendValues(self):
        self.trainController.engineFail = self.tb_engineFail.isChecked()
        self.trainController.brakeFail = self.tb_brakeFail.isChecked()
        self.trainController.signalFail = self.tb_signalFail.isChecked()
        self.trainController.commandedPower = float(self.comPowerVal.text())
        self.trainController.currentSpeed = float(self.curSpeedVal.text())
        self.trainController.authority = float(self.authorityVal.text())
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
    
    def kpkiReceive(self, kp, ki):
        self.trainController.KP = kp
        self.trainController.KI = ki

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

    def displayKPKI(self, kp, ki):
        self.tb_KP.setValue(kp)
        self.tb_KI.setValue(ki)

    def displayEBrakeOn(self, value):
        self.emergencyBrake.setTickInterval(int(value))

    def displayEBrakeOff(self, value):
        self.emergencyBrake.setTickInterval(int(value))

    def displayServiceBrake(self, value):
        if value:
            self.serviceBrake.setTickInterval(int(value))
        else:
            self.serviceBrake.setTickInterval(int(value))

    def displayIntLightsOn(self):
        rejectButton = self.intLightsButton
        acceptButton = self.intLightsButton
        rejectButton.setStyleSheet(("background-color: white;"))
        acceptButton.setStyleSheet("background-color: green;")

    def displayIntLightsOff(self):
        acceptButton = self.intLightsButton
        rejectButton = self.intLightsButton
        acceptButton.setStyleSheet(("background-color: white;"))
        rejectButton.setStyleSheet("background-color: green;")

    def displayExtLightsOn(self):
        rejectButton = self.extLightsButton
        acceptButton = self.extLightsButton
        rejectButton.setStyleSheet(("background-color: white;"))
        acceptButton.setStyleSheet("background-color: green;")

    def displayExtLightsOff(self):
        acceptButton = self.extLightsButton
        rejectButton = self.extLightsButton
        acceptButton.setStyleSheet(("background-color: white;"))
        rejectButton.setStyleSheet("background-color: green;")

    def displayRDoorsClosed(self):
        rejectButton = self.rightDoorButton
        acceptButton = self.rightDoorButton
        rejectButton.setStyleSheet(("background-color: white;"))
        acceptButton.setStyleSheet("background-color: green;")

    def displayRDoorsOpen(self):
        acceptButton = self.rightDoorButton
        rejectButton = self.rightDoorButton
        acceptButton.setStyleSheet(("background-color: white;"))
        rejectButton.setStyleSheet("background-color: green;")

    def displayLDoorsClosed(self):
        rejectButton = self.leftDoorButton
        acceptButton = self.leftDoorButton
        rejectButton.setStyleSheet(("background-color: white;"))
        acceptButton.setStyleSheet("background-color: green;")

    def displayLDoorsOpen(self):
        acceptButton = self.leftDoorButton
        rejectButton = self.leftDoorButton
        acceptButton.setStyleSheet(("background-color: white;"))
        rejectButton.setStyleSheet("background-color: red;")

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TestBenchTrainControllerUI()
    window.show()
    sys.exit(app.exec())