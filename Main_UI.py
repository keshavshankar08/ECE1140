import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *



class Mainmenu(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("pyt\\MainLauncherUI.ui", self)

        self.ctcOfficeButt.clicked.connect(self.ctcOfficeClicked)
        self.trackModelButt.clicked.connect(self.trackModelClicked)
        self.trainModelButt.clicked.connect(self.trainModelClicked)
        self.swWaysideButt.clicked.connect(self.swWaysideClicked)
        self.hwWaysideButt.clicked.connect(self.hwWaysideClicked)
        self.trainControllerButt.clicked.connect(self.trainControllerClicked)

        self.show()

    #window for the ctc office
    def ctcOfficeClicked(self):
        super().__init__()
        uic.loadUi("", self)
        self.show()

    #window for the track model
    def trackModelClicked(self):
        super().__init__()
        uic.loadUi("", self)
        self.show()

    #window for the train model 
    def trainModelClicked(self):
        super().__init__()
        uic.loadUi("", self)
        self.show()

    #window for the se wayside controller
    def swWaysideClicked(self):
        super().__init__()
        uic.loadUi("", self)
        self.show()

    #window for the hw wayside controller
    def hwWaysideClicked(self):
        super().__init__()
        uic.loadUi("", self)
        self.show()

    #window for the train controller
    def trainControllerClicked(self):
        super().__init__()
        uic.loadUi("", self)
        self.show()


#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainmenu()
    app.exec()
