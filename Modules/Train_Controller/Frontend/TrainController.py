#Frontend Implementation for CTC Office

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import time


##main module setup
class TrainControllerUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Controller/Frontend/TrainControllerUI.ui", self) 


        #inputs for test bench
        self.Automaticbutton.clicked.connect(self.Automatic_Button_clicked)
        self.manualbutton.clicked.connect(self.Manual_Button_clicked)
        self.EmergencyButton.clicked.connect(self.Emergency_Button_clicked)

        #self.ResumeButton.clicked.connect(self.Resume_Button_clicked)
        self.leftDoorOpen.clicked.connect(self.LeftDoorOpen_Button_clicked)
        self.leftDoorClosed.clicked.connect(self.LeftDoorClosed_Button_clicked)
        self.rightDoorOpen.clicked.connect(self.RightDoorOpen_Button_clicked)
        self.rightDoorClosed.clicked.connect(self.RightDoorClosed_Button_clicked)
        self.intLightOn.clicked.connect(self.IntLightOn_Button_clicked)
        self.intLightOff.clicked.connect(self.IntLightOff_Button_clicked)
        self.extLightOn.clicked.connect(self.ExtLightOn_Button_clicked)
        self.extLightOff.clicked.connect(self.ExtLightOff_Button_clicked)
        self.authorityinput.valueChanged.connect(self.UpdateValueAuthority)
        self.commandedpowerinput.valueChanged.connect(self.UpdateValueComPower)
        self.KIinput.valueChanged.connect(self.UpdateValueKI)
        self.Kpinput.valueChanged.connect(self.UpdateValueKP)
        #self.driverSpeedChanged.valueChanged.connect()
        #self.serviceBrakeChanged.valueChanged.connect()

        self.show()

    #function for automatic mode
    def Automatic_Button_clicked(self):
        self.Automaticbutton.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.manualbutton.setStyleSheet("background-color: rgb(255, 255, 255)")

    #function for manual mode
    def Manual_Button_clicked(self):
        self.Automaticbutton.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.manualbutton.setStyleSheet("background-color: rgb(199, 199, 199)")    

    #function for emergency brakes
    def Emergency_Button_clicked(self):
        self.EmergencyButton.setStyleSheet("background-color: red")
        # self.ServiceBrake.setStyleSheet("background-color: white")

    #function for service brake
    def Service_Button_clicked(self):
        self.ServiceBrake.setStyleSheet("background-color: blue")
        # self.EmergencyButton.setStyleSheet("background-color: white")

    #function for exiting brakes
    def Resume_Button_clicked(self):
        self.ResumeButton.setStyleSheet("background-color: white")
        self.EmergencyButton.setStyleSheet("background-color: white")
        self.ServiceBrake.setStyleSheet("background-color: white")
    
    #function for left door mode
    def LeftDoorOpen_Button_clicked(self):
        self.leftDoorClosed.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.leftDoorOpen.setStyleSheet("background-color: rgb(199, 199, 199)") 

    #function for left door mode
    def LeftDoorClosed_Button_clicked(self):
        self.leftDoorClosed.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.leftDoorOpen.setStyleSheet("background-color: rgb(255, 255, 255)")  

    #function for right door mode
    def RightDoorOpen_Button_clicked(self):
        self.rightDoorClosed.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.rightDoorOpen.setStyleSheet("background-color: rgb(199, 199, 199)") 

    #function for right door mode
    def RightDoorClosed_Button_clicked(self):
        self.rightDoorClosed.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.rightDoorOpen.setStyleSheet("background-color: rgb(255, 255, 255)") 

    #function for int light mode
    def IntLightOn_Button_clicked(self):
        self.intLightOn.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.intLightOff.setStyleSheet("background-color: rgb(255, 255, 255)") 

    #function for int light mode
    def IntLightOff_Button_clicked(self):
        self.intLightOn.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.intLightOff.setStyleSheet("background-color: rgb(199, 199, 199)") 
    
    #function for int light mode
    def ExtLightOn_Button_clicked(self):
        self.extLightOn.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.extLightOff.setStyleSheet("background-color: rgb(255, 255, 255)") 

    #function for ext light mode
    def ExtLightOff_Button_clicked(self):
        self.extLightOn.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.extLightOff.setStyleSheet("background-color: rgb(199, 199, 199)")

    #functions for Qspinbox to text
    def UpdateValueAuthority(self):
        self.authority_val.setText(str(self.authorityinput.value()))

    def UpdateValueComSpeed(self):
        self.ComSpeed_val.setText(str(self.commandedspeedinput.value()))

    def UpdateValueComPower(self):
        self.ComPower_val.setText(str(self.commandedpowerinput.value()))

    def UpdateValueKI(self):
        self.KI_val.setText(str(self.KIinput.value()))

    def UpdateValueKP(self):
        self.KP_val.setText(str(self.Kpinput.value()))

    def UpdateValueDriverSpeed(self):
        self.Curspeed_val.setText(str(self.driverspeedinput.value()))

    
            
#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainControllerUI()
    app.exec()