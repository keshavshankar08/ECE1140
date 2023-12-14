import PyQt6
import sys
from PyQt6.QtCore import QObject, QDateTime, pyqtSignal
sys.path.append(".")
from signals import signals
from CONSTANTS import constants

#This class represents the train controller
#This is written by John A Deibert for ECE1140

#CONSTANTS
MAX_POWER = 120000

class TrainController(QObject):
    def __init__(self):
        super().__init__()
        signals.current_system_time.connect(self.set_current_time)
        signals.train_controller_update_backend.connect(self.tc_update_values)

        #KP and KI values, true = auto, false = manual
        self.KP = 2000 
        self.KI = 1000 
        self.mode = True

        #Door/lightbulb values, True = Closed/on, False = Open/off
        self.R_door = True
        self.L_door = True
        self.int_lights = False
        self.ext_lights = False
        #Temperature
        self.train_temp = 70

        #speed
        self.commanded_speed = 0.0
        self.current_speed = 0.0
        self.suggested_speed = 0.0

        #power
        self.commanded_power = 0
        self.uk = 0
        self.uk1 = 0
        self.ek = 0
        self.ek1 = 0

        #authority and others
        self.authority = 0.0
        self.station = None
        self.station_side = None
        self.station_authority  = None
        self.train_id = None
        self.beacon_flag = False
        self.train_horn = False
        self.tunnel_status = False
        self.authority_flag = True

        #emergency brakes and service brakes, True = On, False = Off
        self.emergency_brake = False
        self.pEBrake = False
        self.service_brake = False

        #failures
        self.engine_fail = False
        self.brake_fail = False
        self.signal_fail = False

        #previous values
        self.previous_power_command = 0.0
        self.previous_current_speed = 0.0

        self.speed_limit = 70.0
        self.current_time = QDateTime(constants.START_YEAR, constants.START_MONTH, constants.START_MONTH, constants.START_DAY, 
                                      constants.START_HOUR, constants.START_MIN, constants.START_SEC)
        self.current_time = QDateTime()


    def updateCurrentTime(self, value):
        self.current_time = value

    def set_current_time(self, time):
        self.current_time = time

    def tc_update_values(self):
        signals.train_controller_send_power_command.emit(self.train_id, self.commanded_power)
        signals.train_controller_emergency_brake_status.emit(self.train_id, self.emergency_brake)
        signals.train_controller_service_brake_status.emit(self.train_id, self.service_brake)
        signals.train_controller_ext_lights_status.emit(self.train_id, self.ext_lights)
        signals.train_controller_int_lights_status.emit(self.train_id, self.int_lights)
        signals.train_controller_left_door_status.emit(self.train_id, self.L_door)
        signals.train_controller_right_door_status.emit(self.train_id, self.R_door)
        signals.train_controller_temperature_value.emit(self.train_id, self.train_temp)

        ###Power
        vError = 0
        if self.mode == True: #auto mode
            vError = (self.suggested_speed* 0.44704) - self.current_speed
        else: #manual mode
            vError = (self.commanded_speed * 0.44704) - self.current_speed

        #set the ek as sample of vError
        self.ek = vError
        if self.commanded_power < MAX_POWER:
            self.uk = self.uk1 + (constants.TIME_DELTA * 0.001/2)*(self.ek - self.ek1)
        else:
            self.uk = self.uk1
        
        #set previous power command
        #self.previous_power_command = self.commanded_power
        power1 = power2 = power3 = 0
        
        if self.emergency_brake == True or self.service_brake == True:
            self.commanded_power = 0
            self.uk = 0
            self.ek = 0
        else:
            #use triple redundancy to get power
            power1 = (self.KP*self.ek) + (self.KI*self.uk)
            power2 = (self.KP*self.ek) + (self.KI*self.uk)
            power3 = (self.KP*self.ek) + (self.KI*self.uk)

        #if any of the powers do not equal one another apply emergency brake
        if (power1 != power2) or (power1 != power3) or (power2 != power3):
            self.emergency_brake = True
        else:
            self.commanded_power = (self.KP*self.ek) + (self.KI*self.uk)

        # cut off power at appropriate time
        if(self.commanded_power > 120000):
            self.commanded_power = 120000
        elif(self.commanded_power < -120000):
            self.commanded_power = -120000

        #now we set uk1 to uk and ek1 to ek, since they are past values
        self.uk1 = self.uk
        self.ek1 = self.ek

    #this function will set the kp and ki by the engineer
    def set_KP(self, kp):
        self.KP = kp

    def set_KI(self, ki):
        self.KI = ki

    #this function updates the setpoint speed
    def update_suggested_speed(self, value):
        self.suggested_speed = value
              
    #this function updates the commanded speed
    def update_commanded_speed(self, value):
        self.commanded_speed = value

    #this function updates the current speed
    def update_current_speed(self, currSpeed):
        self.current_speed = currSpeed
        
    #this function updates the authority
    def update_authority(self, newAuthority):
        self.authority = newAuthority

    #this function updates the temp
    def update_temp_value(self, temperature):
        self.train_temp = temperature

    #this function toggles the service brake 
    def service_brake_status(self, value):
        if value:
            self.service_brake = True
        else:
            self.service_brake = False

    #this function report E brake on
    def emergency_brake_status(self, value):
        if value:
            self.emergency_brake = True
        else:
            self.emergency_brake = False

    #this function will report if passenger e brake status
    def passenger_EBrake(self, value):
        self.emergency_brake = value
            
    #this function will toggle modes
    def toggle_modes(self, value):
        if value:
            self.mode = True
        else:
            self.mode = False

    def interior_lights_status(self, value):
        if value:
            self.int_lights = True #on
        else:
            self.int_lights = False #off

    def exterior_lights_status(self, value):
        if value:
            self.ext_lights = True
        else:
            self.ext_lights = False

    def left_doors_status(self, value):
        if value:
            self.L_door = True #closed
        else:
            self.L_door = False #open

    def right_doors_status(self, value):
        if value:
            self.R_door = True
        else:
            self.R_door = False
            
    #this function is for announcements
    def beacon_receive(self, beacon):
        self.station = beacon
        if len(beacon) > 1:
                temp_string = beacon.split()
                if temp_string[0] == "CASTLE":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = temp_string[2]
                    self.station_authority = float(temp_string[3])
                elif temp_string[0] == "MT":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = temp_string[2]
                    self.station_authority = float(temp_string[3])
                #red line 
                elif temp_string[0] == "HERRON":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = temp_string[2]
                    self.station_authority = float(temp_string[3])
                elif temp_string[0] == "PENN":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = "Left/Right"
                    self.station_authority = float(temp_string[3])
                elif temp_string[0] == "STEEL":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = temp_string[2]
                    self.station_authority = float(temp_string[3])
                elif temp_string[0] == "FIRST":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = temp_string[2]
                    self.station_authority = float(temp_string[3])
                elif temp_string[0] == "STATION":
                    self.station = temp_string[0] + " " + temp_string[1]
                    self.station_side = temp_string[2]
                    self.station_authority = float(temp_string[3])
                elif temp_string[0] == "SOUTH":
                    self.station = temp_string[0] + " " + temp_string[1] + " " + temp_string[2]
                    self.station_side = temp_string[3]
                    #self.station_authority = float(temp_string[4])
                else:
                    self.station = temp_string[0]
                    self.station_side = temp_string[1]
                    self.station_authority = float(temp_string[2])

    #this function is for engine failure
    def engine_failure(self, failure):
        self.engine_fail = failure
    
    #this function is for brake failure
    def brake_failure(self, failure):
        self.brake_fail = failure
    
    #this function is for signal failure
    def signal_failure(self, failure):
        self.signal_fail = failure

    def train_horn_status(self, value):
        self.train_horn = value

    def receive_tunnel(self, value):
        if value:
            self.ext_lights = True
            self.int_lights = True
