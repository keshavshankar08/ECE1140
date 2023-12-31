from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
import sys

sys.path.append(".")
from Modules.Train_Model.Backend.Train import Train
from signals import signals

INTERVAL = 50


class TrainModelTestBenchUI(QtWidgets.QMainWindow):
    def __init__(self):
        # setup
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_Test_Bench_UI.ui", self)
        self.testTrain = Train()
        self.testingTimer = QTimer()
        self.testingTimer.timeout.connect(signals.trainModel_backend_update)
        self.testingTimer.timeout.connect(self.testTimerHandler)
        self.testingTimer.start(INTERVAL)
        self.send.clicked.connect(self.sendValues)

        # Actual Signals
        signals.trainModel_send_engine_failure.connect(self.engineFailCheckBoxDisplay)
        signals.trainModel_send_signal_failure.connect(self.signalFailCheckBoxDisplay)
        signals.trainModel_send_brake_failure.connect(self.brakeFailCheckBoxDisplay)
        signals.trainModel_send_actual_velocity.connect(self.currentSpeedDisplay)
        signals.trainModel_send_emergency_brake.connect(self.emergencyBrakeDisplay)
        signals.trainModel_send_distance_from_block_start.connect(self.DFBSDisplay)
        signals.trainModel_send_distance_from_yard.connect(self.SDFYDisplay)
        signals.trainModel_send_train_length.connect(self.lenDisplay)
        signals.trainModel_send_beacon.connect(self.beaconDisplay)
        signals.trainModel_send_authority.connect(self.authorityDisplay)
        signals.trainModel_send_speed_limit.connect(self.speedLimitDisplay)
        signals.trainModel_send_suggested_speed.connect(self.suggestedSpeedDisplay)

    def testTimerHandler(self):  # WORKS
        self.engForceDisplay.setText(format(self.testTrain.engineForce, '.2f'))
        self.tb_slopeForceDisplay.setText(format(self.testTrain.slopeForce, '.2f'))
        self.tb_brakeForce.setText(format(self.testTrain.brakeForce, '.2f'))
        self.tb_fricForce.setText(format(self.testTrain.frictionForce, '.2f'))
        self.tb_netForce.setText(format(self.testTrain.netForce, '.2f'))
        self.tb_accel.setText(format(self.testTrain.currentAccel, '.2f'))
        self.tb_mass.setText(format(self.testTrain.mass, '.2f'))
        self.tb_psgrDis.setText(format(self.testTrain.numPassengers, '.0f'))

    #### UI INPUTS 

    def sendValues(self):
        self.testTrain.engineFail = self.tb_engFail.isChecked()
        self.testTrain.brakeFail = self.tb_brakeFail.isChecked()
        self.testTrain.signalFail = self.tb_sigFail.isChecked()
        self.testTrain.currentAuthority = self.authoritySelect.value()
        self.testTrain.speedLimit = self.tb_speedLimitSelect.value()
        self.testTrain.currentBeacon = self.tb_beaconEntry.text()
        if (self.tb_eBrakeToggle.currentText() == "on"):
            self.testTrain.emergencyBrake = True
        else:
            self.testTrain.emergencyBrake = False
        if (self.tb_sBrakeToggle.currentText() == "on"):
            self.testTrain.serviceBrake = True
        else:
            self.testTrain.serviceBrake = False
        if (self.tb_polarity.currentText() == "1"):
            signals.track_model_track_circuit_polarity.emit(1)
        else:
            signals.track_model_track_circuit_polarity.emit(-1)
        self.testTrain.commandedPower = self.tb_power.value()
        self.testTrain.currentGradient = self.tb_gradient.value()
        self.testTrain.speedLimit = self.tb_speedLimitSelect.value()
        self.testTrain.currentBeacon = self.tb_beaconEntry.text()
        self.testTrain.numPassengers += self.tb_psgr.value()
        

    def engineFailCheckBoxReceive(self, value):
        self.testTrain.engineFail = value

    def signalFailCheckBoxReceive(self, value):
        self.testTrain.signalFail = value

    def brakeFailCheckBoxReceive(self, value):
        self.testTrain.brakeFail = value

    def authorityReceive(self, value):
        self.testTrain.currentAuthority = value

    def gradientReceive(self, value):
        self.testTrain.currentGradient = value

    def speedLimitReceive(self, value):
        self.testTrain.speedLimit = value

    def trackPolarityReceive(self, value):  # change to switch case
        if (value == "1"):
            self.testTrain.trackPolarity = 1
        else:
            self.testTrain.trackPolarity = -1

    def beaconReceive(self, value):
        self.testTrain.currentBeacon = value

    def eBrakeReceive(self, value):
        if (value == "on"):
            self.testTrain.emergencyBrake = True
        else:
            self.testTrain.emergencyBrake = False

    def sBrakeReceive(self, value):
        if (value == "on"):
            self.testTrain.serviceBrake = True
        else:
            self.testTrain.serviceBrake = False

    def powerReceive(self, value):
        self.testTrain.commandedPower = value

    #### DISPLAYS

    def engineFailCheckBoxDisplay(self, value):
        self.tb_engFailDisplay.setChecked(value)

    def signalFailCheckBoxDisplay(self, value):
        self.tb_sigFailDisplay.setChecked(value)

    def brakeFailCheckBoxDisplay(self, value):
        self.tb_brakeFailDisplay.setChecked(value)

    def currentSpeedDisplay(self, value):
        self.tb_curSpeedDisplay.setText(format(value, '.2f')) 

    def emergencyBrakeDisplay(self, value):
        if (value):
            self.eBrakeDisplay.setText("on")
        else:
            self.eBrakeDisplay.setText("off")

    def DFBSDisplay(self, value):
        self.tb_DFBS.setText(format(value, '.2f'))

    def SDFYDisplay(self, value):
        self.tb_DFY.setText(format(value, '.2f'))

    def lenDisplay(self, value):
        self.tb_lenDisplay.setText(format(value, '.2f'))
        
    def beaconDisplay(self, value):
        self.tb_beaconDisplay.setText(value)
        
    def authorityDisplay(self, value):
        self.tb_authorityDisplay.setText(format(value, '.2f'))
        
    def speedLimitDisplay(self, value):
        self.tb_speedLimit.setText(format(value, '.2f'))
        
    def suggestedSpeedDisplay(self, value):
        self.tb_suggestedSpeed.setText(format(value, '.2f'))
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModelTestBenchUI()
    window.show()
    sys.exit(app.exec())
