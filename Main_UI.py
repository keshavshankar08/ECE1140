import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
sys.path.append(".")
from Modules.CTC.Frontend.CTC_UI import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.HW_Wayside.Frontend.HW_Wayside_UI import *
from Modules.Track_Model.Backend.Track_Model_Backend import *
#from Modules.CTC.Frontend.frontend import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.HW_Wayside.Frontend.HW_Wayside_UI import *
from Modules.Track_Model.Frontend.Track_Model_UI import *
from Modules.Train_Model.Frontend.Train_Model import *
from Modules.Train_Controller.Frontend.TrainController import *


class Mainmenu(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("MainLauncherUI.ui", self)

        self.ctc_office_button.clicked.connect(self.ctc_office_clicked)
        self.track_model_button.clicked.connect(self.track_model_clicked)
        self.train_model_button.clicked.connect(self.train_model_clicked)
        self.sw_wayside_button.clicked.connect(self.sw_wayside_clicked)
        self.hw_wayside_button.clicked.connect(self.hw_wayside_clicked)
        self.train_controller_button.clicked.connect(self.train_controller_clicked)
            
        self.show()

    #window for the ctc office
    def ctc_office_clicked(self):
        #self.ctcWindow = CTCUI()
        #self.ctcWindow.show()
        pass

    #window for the track model
    def track_model_clicked(self):
        self.trackModelWindow = TrackModelModule()
        self.trackModelWindow.show()

    #window for the train model 
    def train_model_clicked(self):
        self.trainModelWindow = TrainModel()
        self.trainModelWindow.show()
        pass

    #window for the se wayside controller
    def sw_wayside_clicked(self):
        self.swWaysideWindow = SWWaysideFrontend()
        self.swWaysideWindow.show()

    #window for the hw wayside controller
    def hw_wayside_clicked(self):
        self.hwWaysideWindow = HWWaysideFrontend()
        self.hwWaysideWindow.show()
        pass

    #window for the train controller
    def train_controller_clicked(self):
        pass


#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainmenu()
    app.exec()
