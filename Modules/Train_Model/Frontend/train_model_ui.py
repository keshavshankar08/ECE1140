from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

class TrainModelUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("src/frontend/Train_Model/Train_Model_UI.ui", self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainModelUI()
    window.show()
    sys.exit(app.exec())