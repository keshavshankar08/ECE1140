from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.Train import Train

INTERVAL = 50

class TrainModelTestBenchUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_Test_Bench_UI.ui", self)
        self.testTrain = Train(1)
        self.testingTimer = QTimer()
        self.testingTimer.timeout.connect(self.testTrain.TrainModelUpdateValues)
        self.testingTimer.start(INTERVAL)
        self.velocitySelect.valueChanged.connect(self.changeVelocity)
        self.tb_beaconEntry.textChanged.connect(self.displayBeacon)

    def testTimerHandler(self):
        pass

    def changeVelocity(self, value):
        self.tb_curSpeedDisplay.setText(str(value))
        
    def displayBeacon(self, value):
        self.tb_beaconDisplay.setText(str(value))
        

    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModelTestBenchUI()
    window.show()
    sys.exit(app.exec())