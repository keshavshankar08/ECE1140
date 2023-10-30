from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import cv2
sys.path.append(".")
import Track_Resources.Track as track
from Main_Backend import *
from signals import *

class SWWaysideModuleUI(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("Modules/SW_Wayside/Frontend/SW_Wayside_UI.ui", self)
                
                self.track = mainInstance.trackInstance

                self.show()

                

        # Opens file explorer to choose PLC programs
        def uploadPLCClicked(self):
                fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")


if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = SWWaysideModuleUI()
        app.exec()
