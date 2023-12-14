import os
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from playsound import playsound
import sys
import threading
sys.path.append(".")
from signals import *
from CONSTANTS import constants
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
        self.automatic_button.setEnabled(False)
        self.manual_button.setEnabled(False)
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
        self.password_val.setPlaceholderText("Enter password")
        self.password_val.setEnabled(False)

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
        self.password_val.textChanged.connect(self.check_password)
        self.train_horn.clicked.connect(self.play_sound)
        self.train_selection.currentIndexChanged.connect(self.train_select)

        self.current_train_controller = None
        self.train_selection.addItem("< select train >")
        

    def train_select(self, idx):
        self.current_train_controller = self.train_selection.itemData(idx)
        if isinstance(self.current_train_controller, TrainController):
            if self.current_train_controller.tunnel_status:
                self.ext_lights_on()
                self.int_lights_on()
            else:
                self.ext_lights_off()
                self.int_lights_off()

            if self.current_train_controller.int_lights:
                self.int_lights_on()
            else:
                self.int_lights_off()

            if self.current_train_controller.ext_lights:
                self.ext_lights_on()
            else:
                self.ext_lights_off()

            if self.current_train_controller.R_door:
                self.r_doors_closed()
            else:
                self.r_doors_open()

            if self.current_train_controller.L_door:
                self.l_doors_closed()
            else:
                self.l_doors_open()

            if self.current_train_controller.mode:
                self.receive_driver_throttle(self.current_train_controller.suggested_speed)
                self.driver_throttle.setValue(int(self.current_train_controller.suggested_speed))
            else:
                self.receive_driver_throttle(self.current_train_controller.commanded_speed)
                self.driver_throttle.setValue(int(self.current_train_controller.commanded_speed))

            if self.current_train_controller.mode:
                self.automatic_button_clicked()
            else:
                self.manual_button_clicked()
            
            self.temp_val.setValue(self.current_train_controller.train_temp)
                

            self.update_UI()

    def add_train_to_box(self, id):
        train_contoller = train_controller_list.total_trains[id]
        self.train_selection.addItem(f"ID: {id}")
        self.train_selection.setItemData(self.train_selection.count() - 1, train_contoller)
    
    def update_UI(self):
        if self.current_train_controller is not None:
            self.cur_speed_val.setText(format(self.current_train_controller.current_speed*2.237, '.2f'))
            self.com_power_val.setText(format(self.current_train_controller.commanded_power, '.2f'))
            self.authority_val.setText(format(self.current_train_controller.authority*3.28084, '.2f'))
            self.password_val.setEnabled(True)
            self.automatic_button.setEnabled(True)
            self.manual_button.setEnabled(True)

            if self.current_train_controller.authority <= 0:
                self.station_name.setText("APPROACHING " + self.current_train_controller.station + " STATION")
            if self.current_train_controller.authority == 0 and self.current_train_controller.current_speed == 0:
                if self.current_train_controller.station_side == "Right":
                    self.int_lights_on()
                    self.ext_lights_on()
                    self.r_doors_open()
                elif self.current_train_controller.station_side == "Left":
                    self.int_lights_on()
                    self.ext_lights_on()
                    self.l_doors_open()
                elif self.current_train_controller.station_side == "Right/Left":
                    self.int_lights_on()
                    self.ext_lights_on()
                    self.r_doors_open()
                    self.l_doors_open()
                self.current_train_controller.service_brake = True

            if self.current_train_controller.authority != 0 and self.current_train_controller.current_speed != 0:
                    self.ext_lights_off()
                    self.int_lights_off()
                    self.r_doors_closed()
                    self.l_doors_closed()
                    self.station_name.setText(" ")

            if self.current_train_controller.tunnel_status:
                self.ext_lights_on()
                self.int_lights_on()


            if self.current_train_controller.mode:
                self.receive_driver_throttle(self.current_train_controller.suggested_speed)
                self.driver_throttle.setValue(int(self.current_train_controller.suggested_speed))
            else:
                self.receive_driver_throttle(self.current_train_controller.commanded_speed)
                self.driver_throttle.setValue(int(self.current_train_controller.commanded_speed))

            if self.current_train_controller.emergency_brake:
                self.emergency_brake.setValue(1)
            else:
                self.emergency_brake.setValue(0)

            if self.current_train_controller.service_brake:
                self.service_brake.setValue(1)
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
                elif self.current_train_controller.emergency_brake == False and self.current_train_controller.brake_fail == False and\
                    self.current_train_controller.signal_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(False)

            #iteration for brake failure along with e brake
            if self.current_train_controller.brake_fail:
                self.brake_fail.setChecked(True)
                self.current_train_controller.emergency_brake = True
            else:
                self.brake_fail.setChecked(False)
                if self.current_train_controller.emergency_brake and self.current_train_controller.engine_fail == False and\
                    self.current_train_controller.signal_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(True)
                elif self.current_train_controller.emergency_brake == False and self.current_train_controller.engine_fail == False and\
                    self.current_train_controller.signal_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(False)

            #iteration for signal failure along with e brake
            if self.current_train_controller.signal_fail:
                self.signal_fail.setChecked(True)
                self.current_train_controller.emergency_brake = True
            else:
                self.signal_fail.setChecked(False)
                if self.current_train_controller.emergency_brake and self.current_train_controller.engine_fail == False and\
                    self.current_train_controller.brake_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(True)
                elif self.current_train_controller.emergency_brake == False and self.current_train_controller.engine_fail == False and\
                    self.current_train_controller.brake_fail == False and self.current_train_controller.mode == True:
                    self.emergency_brake.setEnabled(False)


            # ###CONVERT CURRENT SPEED TO MPH
            if self.current_train_controller.authority: #authority has some value

                if self.current_train_controller.suggested_speed == 15 and\
                    (self.current_train_controller.current_speed*2.23694) > self.current_train_controller.suggested_speed: #suggested speed is 15
                        self.s_brake(True)

                        if self.current_train_controller.suggested_speed == 10 and\
                            (self.current_train_controller.current_speed*2.23694) > self.current_train_controller.suggested_speed: #suggested speed is 10
                                self.s_brake(True)

                                if self.current_train_controller.authority != 0: #authority is not 0
                                    self.s_brake(False)

                                else:
                                    pass

                        else:# current speed is equal to suggested speed
                            self.s_brake(False)
                else:
                    self.s_brake(False)
            else: #authority is 0
                self.s_brake(True)



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
        signals.train_controller_emergency_brake_status.emit(self.current_train_controller.train_id, value)

    def s_brake(self, value):
        if value:
            self.current_train_controller.service_brake = True
        else:
            self.current_train_controller.service_brake = False
        signals.train_controller_service_brake_status.emit(self.current_train_controller.train_id, value)

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
    def check_password(self, text):
        if (text == "2023"):
            self.KI_val.setEnabled(True)
            self.KP_val.setEnabled(True)
        else:
            self.KI_val.setEnabled(False)
            self.KP_val.setEnabled(False)

    def annouce_stations(self, value):
        self.current_train_controller.station = value

    #function for train horn
    def play_sound(self):
        def play_audio():
            sound_file = os.path.abspath('Train Horn.mp3')
            playsound(sound_file)
        audio_thread = threading.Thread(target=play_audio)
        audio_thread.start()


        
#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrainControllerUI()
    window.show()
    app.exec()