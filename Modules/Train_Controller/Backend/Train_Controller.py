import PyQt6
import sys
from PyQt6.QtCore import QObject

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
KP_VALUE = 0
KI_VALUE = 0

class trainController(QObject):
    def __init__(self):
        #KP and KI values I also amded the mode so we chillin hom slice btw false = manuel, true = autobots assemble
        self.KP = 0
        self.KI = 0
        self.mode = False

        #Door/lightboolb values, True = Closed/on, False = Open/off
        self.Rdoor = True
        self.Ldoor = True
        self.intLights = True
        self.extLights = True
        #Temperature (i am heat meiser)
        self.trainTemp = 70.0

        #I am SPEED kachow mf (range from any value up to speed limit)
        self.commandedSpeed = 0.0
        self.currentSpeed = 0.0
        self.setpointSpeed = 0.0

        #BOWER (Juan Bazerque evil laugh.mp3) and tings
        self.commandedPower = 0.0
        self.newCommandedPower = 0.0
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
            self.uk = self.uk1 + TRAIN_SAMPLE_PERIOD/2 *(self.ek + self.ek1)
        else: #train sample period would now be 0
            self.uk = self.uk1

        if self.emergencyBrake == True or self.serviceBrake == 1.0:
            self.commandedPower = 0
            self.uk = 0
            self.ek = 0
        elif self.serviceBrake != 1.0 or self.serviceBrake != 0.0:
            pass
        else:
            pass

        #now we set uk1 to uk and ek1 to ek, since they be past values now homie
        self.uk1 = self.uk
        self.ek1 = self.ek

    #this function updates the setpoint speed
    def updateSetPointSpeed(self):
        pass

    #this function goes through a station stop
    def trainStationStop(self):
        pass

    #this function updates the commanded speed
    def updateCommandedSpeed(self):
        pass

    #this function updates the current speed
    def updateCurrentSpeed(self):
        pass

    #this function updates the authority
    def updateAuthority(self):
        pass

    #this function updates the temp
    def updateTempValue(self):
        pass

    #this function updates the service brake value
    def updateServiceBrakeValue(self):
        pass

    #this function will toggle the emergency brake
    def toggleEmergencyBrake(self):
        self.emergencyBrake = not self.emergencyBrake

    #this function will toggle modes
    def toggleModes(self):
        self.mode = not self.mode

    #this function will toggle the doors back and forth
    def toggleDoors(self):
        self.Rdoor = not self.Rdoor
        self.Ldoor = not self.Ldoor

    #this function will toggle the lights back and forth
    def toggleLights(self):
        self.intLights = not self.intLights
        self.extLights = not self.extLights

    #this function is for announcements
    def toggleAnnouncements(self):
        pass

    #this function is for advertisements
    def toggleAds(self):
        pass

#SIGNALS
#signal.sendPower.connect()
#signal.sendDoorStatus.connect()
#signal.sendLightStatus.connect()
#signal.sendTempValue.connect()
#signal.sendEBrakeStatus.connect()
#signal.sendServiceBrakeStatus.connect()
#signal.updateSetPointSpeed.connect()
#signal.modeType.connect()
#signal.sendKPKI.connect()
#signal.updateCommandSpeed()






    

    




    
