import os
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from playsound import playsound
import sys
import threading
sys.path.append(".")
from signals import *
from Modules.Train_Controller.Backend.Train_Controller_List import train_controller_list
from Modules.Train_Controller.Backend.Train_Controller import TrainController

##main module setup
class TrainControllerUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/Train_Controller/Frontend/Train_Controller_UI.ui", self)
        signals.train_controller_update_backend.connect(self.update_UI)
        signals.ctc_added_train.connect(self.add_train_to_box)
        self.current_train_controller = TrainController()

        #initialize Values
        self.com_power_val.setText(format(0, '.0f'))
        self.authority_val.setText(format(0, '.0f'))
        self.cur_speed_val.setText(format(0, '.0f'))
        self.com_speed_val.setText(format(0, '.0f'))
        self.KI_val.setEnabled(False)
        self.KP_val.setEnabled(False)
        self.int_lights_off()
        self.ext_lights_off()
        self.r_doors_closed()
        self.l_doors_closed()
        #self.automatic_button_clicked()
        self.password_val.setPlaceholderText("Enter password")

        #connect functions
        self.automatic_button.clicked.connect(self.automatic_button_clicked)
        self.manual_button.clicked.connect(self.manual_button_clicked)
        self.int_light_on.clicked.connect(self.int_lights_on)
        self.int_light_off.clicked.connect(self.int_lights_off)
        self.ext_light_on.clicked.connect(self.ext_lights_on)
        self.ext_light_off.clicked.connect(self.ext_lights_off)
        self.right_door_closed.clicked.connect(self.r_doors_closed)
        self.right_door_open.clicked.connect(self.r_doors_open)
        self.left_door_closed.clicked.connect(self.l_doors_closed)
        self.left_door_open.clicked.connect(self.l_doors_open)
        self.KP_val.valueChanged.connect(self.display_KP)
        self.KI_val.valueChanged.connect(self.display_KI)
        self.temp_val.valueChanged.connect(self.update_temp)
        self.emergency_brake.valueChanged.connect(self.e_brake)
        self.service_brake.valueChanged.connect(self.s_brake)
        self.driver_throttle.valueChanged.connect(self.receive_driver_throttle)
        self.password_val.textChanged.connect(self.checkPassword)
        self.train_horn.clicked.connect(self.play_sound)
        self.train_selection.currentIndexChanged.connect(self.train_select)

        self.current_train_controller = None
        self.train_selection.addItem("< select train >")
        

    def train_select(self, idx):
        self.current_train_controller = self.train_selection.itemData(idx)

    def add_train_to_box(self, id):
        train_contoller = train_controller_list.total_trains[id]
        self.train_selection.addItem(f"ID: {id}")
        self.train_selection.setItemData(self.train_selection.count() - 1, train_contoller)
    
    def update_UI(self):
        if self.current_train_controller is not None:
            self.com_power_val.setText(format(self.current_train_controller.commanded_power, '.2f'))
            self.authority_val.setText(format(self.current_train_controller.authority*3.28084, '.2f'))
            self.cur_speed_val.setText(format(self.current_train_controller.current_speed*2.237, '.2f'))

            if self.current_train_controller.emergency_brake:
                self.emergency_brake.setValue(1)
                #self.driver_throttle.setValue(0)
            else:
                self.emergency_brake.setValue(0)

            if self.current_train_controller.service_brake:
                self.service_brake.setValue(1)
                #self.driver_throttle.setValue(0)
            else:
                self.service_brake.setValue(0)
            
            self.KP_val.setValue(self.current_train_controller.KP)
            self.KI_val.setValue(self.current_train_controller.KI)
            self.temp_val.setValue(self.current_train_controller.train_temp)

            #iteration for engine failure along with e brake
            if self.current_train_controller.engine_fail:
                self.engine_fail.setChecked(True)
                self.current_train_controller.emergency_brake = True
            else:
                self.engine_fail.setChecked(False)
                if self.current_train_controller.emergency_brake and self.current_train_controller.brake_fail == False and\
                    self.current_train_controller.signal_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(True)

            #iteration for brake failure along with e brake
            if self.current_train_controller.brake_fail:
                self.brake_fail.setChecked(True)
                self.current_train_controller.emergency_brake = True
            else:
                self.brake_fail.setChecked(False)
                if self.current_train_controller.emergency_brake and self.current_train_controller.engine_fail == False and\
                    self.current_train_controller.signal_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(True)

            #iteration for signal failure along with e brake
            if self.current_train_controller.signal_fail:
                self.signal_fail.setChecked(True)
                self.current_train_controller.emergency_brake = True
            else:
                self.signal_fail.setChecked(False)
                if self.current_train_controller.emergency_brake and self.current_train_controller.engine_fail == False and\
                    self.current_train_controller.brake_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(True)



    #function for automatic mode
    def automatic_button_clicked(self):
        self.automatic_button.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.manual_button.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.service_brake.setEnabled(False)
        self.emergency_brake.setEnabled(False)
        self.driver_throttle.setEnabled(False)
        self.ext_light_on.setEnabled(False)
        self.ext_light_off.setEnabled(False)
        self.int_light_on.setEnabled(False)
        self.int_light_off.setEnabled(False)
        self.right_door_closed.setEnabled(False)
        self.right_door_open.setEnabled(False)
        self.left_door_closed.setEnabled(False)
        self.left_door_open.setEnabled(False)
        self.temp_val.setEnabled(False)
        self.train_horn.setEnabled(False)
        self.current_train_controller.mode = True
        #QMessageBox.information(self, "Alert", "The Train is in Automatic Mode.")
        
    #function for manual mode
    def manual_button_clicked(self):
        self.automatic_button.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.manual_button.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.service_brake.setEnabled(True)
        self.emergency_brake.setEnabled(True)
        self.driver_throttle.setEnabled(True)
        self.ext_light_on.setEnabled(True)
        self.ext_light_off.setEnabled(True)
        self.int_light_on.setEnabled(True)
        self.int_light_off.setEnabled(True)
        self.right_door_closed.setEnabled(True)
        self.right_door_open.setEnabled(True)
        self.left_door_closed.setEnabled(True)
        self.left_door_open.setEnabled(True)
        self.temp_val.setEnabled(True)
        self.train_horn.setEnabled(True)
        self.current_train_controller.mode = False
        QMessageBox.information(self, "Alert", "The Train is in Manual Mode.")

    def receive_driver_throttle(self, value):
        self.current_train_controller.commanded_speed = value
        self.com_speed_val.setText(str(self.current_train_controller.commanded_speed))

    #function for emergency brakes
    def e_brake(self, value):
        if value:
            self.current_train_controller.emergency_brake = True
        else:
            self.current_train_controller.emergency_brake = False

    def s_brake(self, value):
        if value:
            self.current_train_controller.service_brake = True
        else:
            self.current_train_controller.service_brake = False

    #function will display the current speed
    def display_current_speed(self, speed):
        self.current_train_controller.current_speed = speed
        self.cur_speed_val.setText(format(self.current_train_controller.current_speed, '.2f'))

    #function will display Kp and Ki
    def display_KP(self, kp):
        self.current_train_controller.KP = kp
        self.KP_val.setValue(self.current_train_controller.KP)

    def display_KI(self, ki):
        self.current_train_controller.KI = ki
        self.KI_val.setValue(self.current_train_controller.KI)

    #function display power
    def update_power(self, power):
        self.current_train_controller.commanded_power = power
        self.com_power_val.setText(str(self.current_train_controller.commanded_power))

    #function displays authority
    def update_authority(self, authority):
        self.current_train_controller.authority = authority
        self.authority_val.setText(str(self.current_train_controller.authority))

    #function will toggle int lights
    def int_lights_on(self):
            self.int_light_on.setStyleSheet("background-color: green;")
            self.int_light_off.setStyleSheet("background-color: white;")
            self.current_train_controller.int_lights = True

    def int_lights_off(self):
            self.int_light_on.setStyleSheet("background-color: white;")
            self.int_light_off.setStyleSheet("background-color: green;")
            self.current_train_controller.int_lights = False

    #function will toggle ext lights
    def ext_lights_on(self):
        self.ext_light_on.setStyleSheet("background-color: green;")
        self.ext_light_off.setStyleSheet("background-color: white;")
        self.current_train_controller.ext_lights = True

    def ext_lights_off(self):
        self.ext_light_on.setStyleSheet("background-color: white;")
        self.ext_light_off.setStyleSheet("background-color: green;")
        self.current_train_controller.ext_lights = False

    #function - right doors closed
    def r_doors_closed(self):
        self.right_door_closed.setStyleSheet("background-color: green;")
        self.right_door_open.setStyleSheet("background-color: white;")
        self.current_train_controller.R_door = True

    def r_doors_open(self):
        self.right_door_closed.setStyleSheet("background-color: white;")
        self.right_door_open.setStyleSheet("background-color: green;")
        self.current_train_controller.R_door = False

    #function - left doors closed
    def l_doors_closed(self):
        self.left_door_closed.setStyleSheet("background-color: green;")
        self.left_door_open.setStyleSheet("background-color: white;")
        self.current_train_controller.L_door = True

    def l_doors_open(self):
        self.left_door_closed.setStyleSheet("background-color: white;")
        self.left_door_open.setStyleSheet("background-color: green;")
        self.current_train_controller.L_door = False

    #function updates temp
    def update_temp(self, temp):
        self.current_train_controller.train_temp = temp
        self.temp_val.setValue(temp)

    #function for password
    def checkPassword(self, text):
        if (text == "2023"):
            self.KI_val.setEnabled(True)
            self.KP_val.setEnabled(True)
        else:
            self.KI_val.setEnabled(False)
            self.KP_val.setEnabled(False)

    #function for train horn
    def play_sound(self):
        def play_audio():
            sound_file = os.path.abspath('Easter Egg Horn.mp3')
            playsound(sound_file)
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()


        
#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainControllerUI()
    window.show()
    app.exec()