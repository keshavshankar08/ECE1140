import sys
sys.path.append(".")
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from Modules.CTC.Frontend.CTC_UI import *
from Modules.Track_Model.Backend.Track_Model_Backend import *
#from Modules.CTC.Frontend.frontend import *
from Modules.SW_Wayside.Frontend.SW_Wayside_Frontend import *
from Modules.HW_Wayside.Frontend.HW_Wayside_Frontend import *
from Modules.Track_Model.Frontend.Track_Model_UI import *
from Modules.Train_Model.Frontend.Train_Model import *
from Modules.Train_Controller.Frontend.Train_Controller_UI import *
from Admin_UI import *

# provides UI functionality to main launcher

class MainFrontend(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("MainLauncherUI.ui", self)
        
        self.ctc_office_button.setEnabled(False)
        self.sw_wayside_button.setEnabled(False)
        self.hw_wayside_button.setEnabled(False)
        self.train_model_button.setEnabled(False)
        self.train_controller_button.setEnabled(False)

        self.ctc_office_button.clicked.connect(self.ctc_office_clicked)
        self.track_model_button.clicked.connect(self.track_model_clicked)
        self.train_model_button.clicked.connect(self.train_model_clicked)
        self.sw_wayside_button.clicked.connect(self.sw_wayside_clicked)
        self.hw_wayside_button.clicked.connect(self.hw_wayside_clicked)
        self.train_controller_button.clicked.connect(self.train_controller_clicked)
        
        self.resumeButton.setEnabled(False)
        self.pauseButton.clicked.connect(self.pauseTimer)
        self.resumeButton.clicked.connect(self.resumeTimer)
        
        signals.current_system_time.connect(self.display_time)
        self.system_speed_select.valueChanged.connect(self.set_speed)
        
        self.adminButton.setEnabled(False)
        self.passwordBox.textChanged.connect(self.checkPassword)
        self.adminButton.clicked.connect(self.admin_clicked)
        
        
        self.ctcWindow = CTCFrontend()
        self.trackModelWindow = TrackModelModule()
        self.trainModelWindow = TrainModel()
        self.swWaysideWindow = SWWaysideFrontend()
        self.hwWaysideWindow = HWWaysideFrontend()
        self.trainControllerWindow = TrainControllerUI()
        self.adminWindow = ADMIN()
        self.show()
        
    def checkPassword(self, text):
        if (text == "1234"):
            self.adminButton.setEnabled(True)
        else:
            self.adminButton.setEnabled(False)
            
    def admin_clicked(self):
        self.adminWindow.show()
        
    def pauseTimer(self):
        signals.pause_timer.emit()
        self.pauseButton.setEnabled(False)
        self.resumeButton.setEnabled(True)
        
    def resumeTimer(self):
        signals.resume_timer.emit()
        self.resumeButton.setEnabled(False)
        self.pauseButton.setEnabled(True)
        
    def display_time(self, value):
        self.system_time_select.setDateTime(value)
        
    def set_speed(self, value):
        signals.change_system_speed.emit(value)

    #window for the ctc office
    def ctc_office_clicked(self):
        self.ctcWindow.show()

    #window for the track model
    def track_model_clicked(self):
        self.sw_wayside_button.setEnabled(True)
        self.hw_wayside_button.setEnabled(True)
        self.trackModelWindow.show()

    #window for the train model 
    def train_model_clicked(self):
        self.trainModelWindow.show()

    #window for the se wayside controller
    def sw_wayside_clicked(self):
        self.ctc_office_button.setEnabled(True)
        self.train_model_button.setEnabled(True)
        self.train_controller_button.setEnabled(True)
        self.swWaysideWindow.show()
        self.hw_wayside_button.setEnabled(False)
        signals.wayside_choice.emit(0)

    #window for the hw wayside controller
    def hw_wayside_clicked(self):
        self.ctc_office_button.setEnabled(True)
        self.train_model_button.setEnabled(True)
        self.train_controller_button.setEnabled(True)
        self.hwWaysideWindow.show()
        self.sw_wayside_button.setEnabled(False)
        signals.wayside_choice.emit(1)

    #window for the train controller
    def train_controller_clicked(self):
        self.trainControllerWindow.show()
