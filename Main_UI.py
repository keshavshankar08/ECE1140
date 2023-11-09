import sys
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
        super().__init__()
        uic.loadUi("MainLauncherUI.ui", self)

        self.ctc_office_button.clicked.connect(self.ctcOfficeClicked)
        self.track_model_button.clicked.connect(self.trackModelClicked)
        self.train_model_button.clicked.connect(self.trainModelClicked)
        self.sw_wayside_button.clicked.connect(self.swWaysideClicked)
        self.hw_wayside_button.clicked.connect(self.hwWaysideClicked)
        self.train_controller_button.clicked.connect(self.trainControllerClicked)
            
        self.show()

    #window for the ctc office
    def ctcOfficeClicked(self):
        self.ctcWindow = SWWaysideModuleUI() #KESHAV UI NOT TIMS
        self.ctcWindow.show()

    #window for the track model
    def trackModelClicked(self):
        self.trackModelWindow = QtWidgets.QMainWindow()
        ui = Ui_TrackModelModule()
        ui.setupUi(self.trackModelWindow)
        self.trackModelWindow.show()

    #window for the train model 
    def trainModelClicked(self):
        self.trainModelWindow = TrainModelUI()
        self.trainModelWindow.show()

    #window for the se wayside controller
    def swWaysideClicked(self):
        self.swWaysideWindow = SWWaysideModuleUI()
        self.swWaysideWindow.show()

    #window for the hw wayside controller
    def hwWaysideClicked(self):
        self.hwWaysideWindow = SWWaysideModuleUI() #KESHAV UI NOT NATE
        self.hwWaysideWindow.show()

    #window for the train controller
    def trainControllerClicked(self):
        self.trainWindow = TrainControllerUI()
        self.trainWindow.show()


#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainmenu()
    app.exec()
