from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
sys.path.append(".")
from signals import signals

class TrainModelTestBenchUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_Test_Bench_UI.ui", self)

        self.velocitySelect.valueChanged.connect(self.changeVelocity)

    def changeVelocity(self, value):
        self.curSpeedDisplay.setText(str(value))

    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModelTestBenchUI()
    window.show()
    sys.exit(app.exec())