from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QTimer
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.Train import Train, trains
from signals import signals

class TrainModel(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Modules/Train_Model/Frontend/Train_Model_UI.ui", self)
        signals.trainModel_backend_update.connect(self.UIUpdate)
        self.trainSelectUpdate()

    def UIUpdate(self):
        pass
    
    def trainSelectUpdate(self):
        for key, value in trains.items():
            self.trainSelectComboBox.addItem(f"ID: {key}")
        
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModel()
    window.show()
    sys.exit(app.exec())