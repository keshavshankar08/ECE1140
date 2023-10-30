import sys
import cv2
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
sys.path.append(".")
#THIS IS KESHAV'S FILE REPLACE WITH TIMS UI
#from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
#THIS IS KESHAV'S FILE REPLACE WITH NATES UI
#from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.Track_Model.Frontend.Track_Model_UI import *
from Modules.Train_Model.Frontend.train_model_ui import *
from Modules.Train_Controller.Frontend.TrainController import *



class Mainmenu(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__
        uic.loadUi("MainLauncherUI.ui", self)

        self.ctcOfficeButt.clicked.connect(self.ctcOfficeClicked)
        self.trackModelButt.clicked.connect(self.trackModelClicked)
        self.trainModelButt.clicked.connect(self.trainModelClicked)
        self.swWaysideButt.clicked.connect(self.swWaysideClicked)
        self.hwWaysideButt.clicked.connect(self.hwWaysideClicked)
        self.trainControllerButt.clicked.connect(self.trainControllerClicked)

        self.show()

    #window for the ctc office
    def ctcOfficeClicked(self):
        ctcWindow = SWWaysideModuleUI() #KESHAV UI NOT TIMS
        ctcWindow.show()

    #window for the track model
    def trackModelClicked(self):
        trackModelWindow = Ui_TrackModelModule()
        trackModelWindow.show()
        

    #window for the train model 
    def trainModelClicked(self):
        trainModelWindow = TrainModelUI()
        trainModelWindow.show()

    #window for the se wayside controller
    def swWaysideClicked(self):
        swWaysideWindow = SWWaysideModuleUI()
        swWaysideWindow.show()

    #window for the hw wayside controller
    def hwWaysideClicked(self):
        hwWaysideWindow = SWWaysideModuleUI() #KESHAV UI NOT NATE
        hwWaysideWindow.show()

    #window for the train controller
    def trainControllerClicked(self):
        trainWindow = TrainControllerUI()
        trainWindow.show()


#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainmenu()
    app.exec()
