from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.Train import Train
from signals import signals

class TrainModel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_UI.ui", self)
        signals.current_system_time.connect(self.displayTime)

    def displayTime(self, value):
        self.velocityDisplay.setText(value.toString('yyyy-MM-dd HH:mm:ss'))
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModel()
    window.show()
    sys.exit(app.exec())