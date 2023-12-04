import PyQt6
import sys
from PyQt6.QtCore import QObject, QDateTime, pyqtSignal
sys.path.append(".")
from signals import signals
from CONSTANTS import START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC, TIME_DELTA

#This class represents the train controller
#This is written by John A Deibert for ECE1140

#CONSTANTS
MAX_POWER = 120000

class trainController():
    def __init__(self):
        signals.current_system_time.connect(self.setCurrentTime)
        signals.train_controller_update_backend.connect(self.tc_update_values)

        #KP and KI values, true = auto, false = manual
        self.KP = 400
        self.KI = 20
        self.mode = True

        #Door/lightbulb values, True = Closed/on, False = Open/off
        self.R_door = True
        self.L_door = True
        self.int_lights = True
        self.ext_lights = True
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
        self.train_ID = None
        self.train_list = []

        '''Emergency button AND DA SERVY WERVY BRAKEY WAKEY, True = On, False = Off 
        da SeRvIcE bRaKe is from range 0.0 to 1.0 (no to full brake), btw angry no green comment
        '''
        self.emergency_brake = False
        self.pEBrake = False
        self.service_brake = False
        self.service_brake = False

        #failures
        self.engine_fail = False
        self.brake_fail = False
        self.signal_fail = False

        #previous values
        self.previous_power_command = 0.0
        self.previous_current_speed = 0.0

        self.speed_limit = 70.0
        self.current_time = QDateTime(START_YEAR, START_MONTH, START_MONTH, START_DAY, 
                                      START_HOUR, START_MIN, START_SEC)
        self.current_time = QDateTime()

        #Signals
        signals.trainModel_send_actual_velocity.connect(self.update_current_speed)
        signals.trainModel_send_authority.connect(self.update_authority)
        signals.trainModel_send_beacon.connect(self.announceStation)
        signals.trainModel_send_emergency_brake.connect(self.passenger_EBrake)
        #signals.trainModel_send_speed_limit.connect(self.update_suggested_speed)
        signals.trainModel_send_suggested_speed.connect(self.update_suggested_speed)
        signals.trainModel_send_engine_failure.connect(self.engine_failure)
        signals.trainModel_send_brake_failure.connect(self.brake_failure)
        signals.trainModel_send_signal_failure.connect(self.signal_failure)

    def updateCurrentTime(self, value):
        self.current_time = value

    def setCurrentTime(self, time):
        self.current_time = time

    def tc_update_values(self):
        signals.train_controller_send_power_command.emit(self.commanded_power)
        signals.train_controller_emergency_brake_status.emit(self.emergency_brake)
        signals.train_controller_service_brake_status.emit(self.service_brake)
        signals.train_controller_ext_lights_status.emit(self.ext_lights)
        signals.train_controller_int_lights_status.emit(self.int_lights)
        signals.train_controller_left_door_status.emit(self.L_door)
        signals.train_controller_right_door_status.emit(self.R_door)
        signals.train_controller_temperature_value.emit(self.train_temp)

        #convert to right metrics
        self.commanded_speed * 0.44704
        #vError = 0
        vError = self.commanded_speed - self.current_speed
        # if self.mode == True: #autobot mode
        #     vError = self.commanded_speed - self.current_speed
        # else: #manual mode
        #     vError = self.suggested_speed - self.current_speed

        #set the ek as sample of vError
        self.ek = vError

        if self.commanded_power < MAX_POWER:
            self.uk = self.uk1 + TIME_DELTA/2 *(self.ek + self.ek1)
        else: 
            self.uk = self.uk1
        
        #set previous power command
        self.previous_power_command = self.commanded_power
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

        #now we set uk1 to uk and ek1 to ek, since they be past values now homie
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

    #this function goes through a station stop
    def train_station_stop(self):
        while self.current_speed != 0:
            pass
            #wait 1 second

        #activate service brake to stop moving
        #self.service_brake = True
        #toggle lights and doors for a station


        #wait 1 minute

        #deactivate the service brake to start moving again
        #self.service_brake = False
        #toggle lights and doors
       

    #this function updates the commanded speed
    def update_commanded_speed(self, value):
        self.commanded_speed = value


    #this function updates the current speed
    def update_current_speed(self, currSpeed):
        self.previous_current_speed = self.current_speed
        self.current_speed = currSpeed
        
        #check for engine failure
        if self.previous_power_command == self.commanded_power and\
            self.previous_current_speed > self.current_speed:

            self.engine_fail = True

    #this function updates the authority
    def update_authority(self, newAuthority):
        if newAuthority:
            if self.authority:
                if self.service_brake:
                    pass
                else:
                    self.service_brake = False
                    
            else:
                if self.KP == 0 or self.KI == 0:
                    pass
                else:
                    self.authority = newAuthority
                    self.service_brake = False
        else:
            self.authority = newAuthority
            #self.service_brake = True
            
    #this function updates the temp
    def updateTempValue(self, temperature):
        self.train_temp = temperature

    #this function toggles the service brake 
    def serviceBrakeStatus(self, value):
        if value:
            self.service_brake = True
        else:
            self.service_brake = False

    #this function report E brake on
    def emergencyBrakeStatus(self, value):
        if value or self.pEBrake == True:
            self.emergency_brake = True
        else:
            self.emergency_brake = False

    #this function will report if passenger e brake status
    def passenger_EBrake(self, value):
        if value:
            self.pEBrake = True
        else:
            self.pEBrake = False

    #this function will toggle modes
    def toggleModes(self):
        self.mode = not self.mode

    def interiorLightsStatus(self, value):
        if value:
            self.int_lights = True #on
        else:
            self.int_lights = False #off

    def exteriorLightsStatus(self, value):
        if value:
            self.ext_lights = True
        else:
            self.ext_lights = False

    def leftDoorsStatus(self, value):
        if value:
            self.L_door = True #closed
        else:
            self.L_door = False #open

    def rightDoorsStatus(self, value):
        if value:
            self.R_door = True
        else:
            self.R_door = False
            
    #this function is for announcements
    def announceStation(self, beacon):
        self.station = beacon

    #this function is for engine failure
    def engine_failure(self, failure):
        self.engine_fail = failure

        if self.engine_fail:
            self.emergency_brake = True
            self.commanded_power = 0
        else:
            self.emergency_brake = False
    
    #this function is for brake failure
    def brake_failure(self, failure):
        self.brake_fail = failure

        if self.brake_fail:
            self.emergency_brake = True
            self.service_brake = False
        else:
            self.emergency_brake = False
    
    #this function is for signal failure
    def signal_failure(self, failure):
        self.signal_fail = failure

        if self.signal_fail:
            self.emergency_brake = True
            #beacon will equal nothing
        else:
            self.emergency_brake = False




    
