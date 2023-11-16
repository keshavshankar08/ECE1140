import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
sys.path.append(".")

##from Modules.CTC.Frontend.frontend import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.HW_Wayside.Frontend.HW_Wayside_UI import *
from Modules.Track_Model.Frontend.Track_Model_UI import *
#from Modules.Train_Model.Frontend.Train_Model import *
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
        
        signals.current_system_time.connect(self.display_time)
        self.system_speed_select.valueChanged.connect(self.set_speed)
        
        self.trackModelWindow = TrackModelModule()
        self.trainModelWindow = TrainModel()
        self.swWaysideWindow = SWWaysideFrontend()
        #self.hwWaysideWindow = HWWaysideFrontend()
        self.show()
        
    def display_time(self, value):
        self.system_time_select.setDateTime(value)
        
    def set_speed(self, value):
        signals.change_system_speed.emit(value)

    #window for the ctc office
    def ctc_office_clicked(self):
        self.ctcWindow = CTCFrontend()
        self.ctcWindow.show()

    #window for the track model
    def track_model_clicked(self):
        self.trackModelWindow.show()

    #window for the train model 
    def train_model_clicked(self):
        self.trainModelWindow.show()
        pass

    #window for the se wayside controller
    def sw_wayside_clicked(self):
        self.swWaysideWindow.show()

    #window for the hw wayside controller
    def hw_wayside_clicked(self):
        #self.hwWaysideWindow.show()
        pass

    #window for the train controller
    def train_controller_clicked(self):
        pass
    
    


#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainmenu()
    app.exec()
