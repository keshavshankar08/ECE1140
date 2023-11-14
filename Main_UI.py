import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
sys.path.append(".")
#from Modules.CTC.Frontend.frontend import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.HW_Wayside.Frontend.frontend import *
from Modules.Track_Model.Frontend.Track_Model_UI import *
#from Modules.Train_Model.Frontend.train_model_test_bench_ui import *
from Modules.Train_Controller.Frontend.TrainController import *

class Mainmenu(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("MainLauncherUI.ui", self)

        self.ctcOfficeButt.clicked.connect(self.ctc_office_clicked)
        self.trackModelButt.clicked.connect(self.track_model_clicked)
        self.trainModelButt.clicked.connect(self.train_model_clicked)
        self.swWaysideButt.clicked.connect(self.sw_wayside_clicked)
        self.hwWaysideButt.clicked.connect(self.hw_wayside_clicked)
        self.trainControllerButt.clicked.connect(self.train_controller_clicked)
            
        self.show()

    #window for the ctc office
    def ctc_office_clicked(self):
        #self.ctcWindow = CTCUI()
        #self.ctcWindow.show()
        pass

    #window for the track model
    def track_model_clicked(self):
        self.trackModelWindow = QtWidgets.QMainWindow()
        ui = Ui_TrackModelModule()
        ui.setupUi(self.trackModelWindow)
        self.trackModelWindow.show()

    #window for the train model 
    def train_model_clicked(self):
        #self.trainModelWindow = TrainModelUI()
        #self.trainModelWindow.show()
        pass

    #window for the se wayside controller
    def sw_wayside_clicked(self):
        self.swWaysideWindow = SWWaysideFrontend()
        self.swWaysideWindow.show()

    #window for the hw wayside controller
    def hw_wayside_clicked(self):
        #self.hwWaysideWindow = HWWaysideModuleUI()
        #self.hwWaysideWindow.show()
        pass

    #window for the train controller
    def train_controller_clicked(self):
        self.trainWindow = TrainModelTestBenchUI()
        self.trainWindow.show()


#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainmenu()
    app.exec()
