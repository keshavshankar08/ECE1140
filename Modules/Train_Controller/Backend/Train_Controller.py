import PyQt6
import sys
from PyQt6.QtCore import QObject
from signals import signals
from Main_Backend import START_HOUR, START_MIN, START_SEC, TIME_DELTA

#This class represents the train controller
#There will be a separate class that incorporates the entire train system(maybe, prob would be best but idk)
#This is written by John A Deibert for ECE1140

#think about number of trains, maybe use train id
#think about automatic/manuel mode
#must report position to the train model by using commanded speed and time
#Think about failures within train

#OUTPUTS
    #braking
    #commanded speed
    #R and L doors
    #int lights and ext lights
    #temperature
    #KP and KI
    #commanded power

#CONSTANTS
MAX_POWER = 120000
TRAIN_SAMPLE_PERIOD = 1 #change for later when we find out tample meriod

class trainController(QObject):
    def __init__(self):
        #KP and KI values I also amded the mode so we chillin hom slice btw false = manuel, true = autobots assemble
        self.KP = 0
        self.KI = 0
        self.mode = True

        #Door/lightboolb values, True = Closed/on, False = Open/off
        self.Rdoor = True
        self.Ldoor = True
        self.intLights = True
        self.extLights = True
        #Temperature (i am heat meiser)
        self.trainTemp = 70.0

        #I am SPEED kachow mf (range from any value up to speed limit)
        self.commandedSpeed = 0.0
        self.currentSpeed = 0.0 #make setter for getting curr speed from TM
        self.setpointSpeed = 0.0

        #BOWER (Juan Bazerque evil laugh.mp3) and tings
        self.commandedPower = 0.0
        self.uk = 0
        self.uk1 = 0
        self.ek = 0
        self.ek1 = 0

        #authority and stupid things that i need
        self.authority = 0.0
        self.announcements = 0
        self.advertisements = 0

        '''Emergency button AND DA SERVY WERVY BRAKEY WAKEY, True = On, False = Off 
        da SeRvIcE bRaKe is from range 0.0 to 1.0 (no to full brake), btw angry no green comment
        '''
        self.emergencyBrake = False
        self.serviceBrake = 0.0

    #this function will calculate power, uks = m, eks = m/s, speeds = m/s
    def calculatePower(self):
        vError = 0
        if self.mode == True: #autobot mode
            vError = self.commandedSpeed - self.currentSpeed
        else: #manual mode
            vError = self.setpointSpeed - self.currentSpeed

        #set the ek as sample of vError
        self.ek = vError

        if self.commandedPower < MAX_POWER:
            self.uk = self.uk1 + TRAIN_SAMPLE_PERIOD/2 *(self.ek - self.ek1)
        else: 
            self.uk = self.uk1

        if self.emergencyBrake == True or self.serviceBrake == 1.0:
            self.commandedPower = 0
            self.uk = 0
            self.ek = 0
        else:
            pass
        
        self.commandedPower = self.KP*self.ek + self.KI*self.uk
        signals.train_controller_power.emit()
        
        #now we set uk1 to uk and ek1 to ek, since they be past values now homie
        self.uk1 = self.uk
        self.ek1 = self.ek

    #this function will set the kp by the engineer
    def setKP(self, kp):
        self.KP = kp

    #this function will set the ki by the engineer
    def setKP(self, ki):
        self.KI = ki

    #this function updates the setpoint speed
    def updateSetPointSpeed(self, setPointSpeed):
        self.setpointSpeed = setPointSpeed

    #this function goes through a station stop
    def trainStationStop(self):
        pass

    #this function updates the commanded speed
    def updateCommandedSpeed(self, commandSpeed):
        self.commandedSpeed = commandSpeed

    #this function updates the current speed
    def updateCurrentSpeed(self):
        pass

    #this function updates the authority
    def updateAuthority(self):
        pass

    #this function updates the temp
    def updateTempValue(self, temperature):
        self.trainTemp = temperature
        signals.train_controller_temperature_value.emit()

    #this function updates the service brake value
    def updateServiceBrakeValue(self, braking):
        self.serviceBrake = braking
        signals.train_controller_service_brake_value.emit()
        #reminder that service brake is 0 to 10 so the final result must be divided by 10

    #this function report E brake on
    def emergencyBrakeOn(self):
        self.emergencyBrake = True
        signals.train_controller_emergency_brake_on.emit()

    #this function will report e brake off
    def emergencyBrakeOff(self):
        self.emergencyBrake = False
        signals.train_controller_emergency_brake_off.emit()

    #this function will toggle modes
    def toggleModes(self):
        self.mode = not self.mode

    #this function will report left doors
    def toggleDoorsLeft(self):
        self.Ldoor = not self.Ldoor
        if(self.Ldoor == True):
            signals.train_controller_left_door_closed.emit()
        else:
            signals.train_controller_left_door_open.emit()

    #this function will report right doors
    def toggleDoorsRight(self):
        self.Rdoor = not self.Rdoor
        if(self.Rdoor == True):
            signals.train_controller_right_door_closed.emit()
        else:
            signals.train_controller_right_door_open.emit()

    #this function will report int lights 
    def toggleLightsInt(self):
        self.intLights = not self.intLights
        if(self.intLights == True):
            signals.train_controller_int_lights_on.emit()
        else:
            signals.train_controller_int_lights_off.emit()

    #this function will report ext lights 
    def toggleLightsExt(self):
        self.extLights = not self.extLights
        if(self.extLights == True):
            signals.train_controller_ext_lights_on.emit()
        else:
            signals.train_controller_ext_lights_off.emit()
        

    #this function is for announcements
    def toggleAnnouncements(self):
        pass






    

    




    
