import PyQt6
import sys
from PyQt6.QtCore import QObject, QDateTime, pyqtSignal
sys.path.append(".")
from signals import signals
from CONSTANTS import START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC, TIME_DELTA

#This class represents the train controller
#This is written by John A Deibert for ECE1140

#think about number of trains, maybe use train id

#CONSTANTS
MAX_POWER = 120000

class trainController():
    def __init__(self):
        signals.current_system_time.connect(self.setCurrentTime)
        signals.train_controller_backend_update.connect(self.updateValuesTC)
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
        self.currentSpeed = 0.0
        self.setpointSpeed = 0.0

        #BOWER (Juan Bazerque evil laugh.mp3) and tings
        self.commandedPower = 1200
        self.uk = 0
        self.uk1 = 0
        self.ek = 0
        self.ek1 = 0

        #authority and stupid things that i need
        self.authority = 0.0
        self.station = None
        self.trainID = None

        '''Emergency button AND DA SERVY WERVY BRAKEY WAKEY, True = On, False = Off 
        da SeRvIcE bRaKe is from range 0.0 to 1.0 (no to full brake), btw angry no green comment
        '''
        self.emergencyBrake = False
        self.serviceBrake = True

        #failures
        self.engineFail = False
        self.brakeFail = False
        self.signalFail = False

        #previous values
        self.previousPowerCommand = 0.0
        self.previousCurrentSpeed = 0.0

        self.speedLimit = 70.0
        self.currentTime = QDateTime()

        #Signals
        signals.trainModel_send_actual_velocity.connect(self.updateCurrentSpeed)
        signals.trainModel_send_authority.connect(self.updateAuthority)
        signals.trainModel_send_beacon.connect(self.announceStation)
        signals.trainModel_send_emergency_brake.connect(self.passengerEBrake)
        signals.trainModel_send_speed_limit.connect(self.updateSetPointSpeed)
        signals.trainModel_send_suggested_speed.connect(self.updateCommandedSpeed)
        signals.trainModel_send_engine_failure.connect(self.engineFailure)
        signals.trainModel_send_brake_failure.connect(self.brakeFailure)
        signals.trainModel_send_signal_failure.connect(self.signalFailure)


    #updating values function
    def updateValuesTC(self):

        #Train Controller Signals
        #lights
        signals.train_controller_int_lights_on.emit(self.toggleLightsInt)
        signals.train_controller_int_lights_off.emit(self.toggleLightsInt)
        signals.train_controller_ext_lights_on.emit(self.toggleLightsExt)
        signals.train_controller_ext_lights_off.emit(self.toggleLightsExt)
        #doors
        signals.train_controller_right_door_closed.emit(self.toggleDoorsRight)
        signals.train_controller_right_door_open.emit(self.toggleDoorsRight)
        signals.train_controller_left_door_closed.emit(self.toggleDoorsLeft)
        signals.train_controller_left_door_open.emit(self.toggleDoorsLeft)
        #Bower
        signals.train_controller_send_power_command.emit(self.calculatePower)
        #Temperature
        signals.train_controller_temperature_value.emit(self.updateTempValue)
        #Braking
        signals.train_controller_service_brake.emit(self.toggleServiceBrake)
        signals.train_controller_emergency_brake_on.emit(self.emergencyBrakeOn)
        signals.train_controller_emergency_brake_off.emit(self.emergencyBrakeOff)



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
            self.uk = self.uk1 + TIME_DELTA/2 *(self.ek + self.ek1)
            pass
        else: 
            self.uk = self.uk1
        
        #set previous power command
        self.previousPowerCommand = self.commandedPower

        if self.emergencyBrake == True or self.serviceBrake == True:
            self.commandedPower = 0
            self.uk = 0
            self.ek = 0
        else:
            #use triple redundancy to get power
            power1 = (self.KP*self.ek) + (self.KI*self.uk)
            power2 = (self.KP*self.ek) + (self.KI*self.uk)
            power3 = (self.KP*self.ek) + (self.KI*self.uk)

        #if any of the powers do not equal one another apply emergency brake
        if (power1 != power2) or (power1 != power3) or (power2 != power3):
            self.emergencyBrake = True
        
        signals.train_controller_send_power_command.emit()
        
        #now we set uk1 to uk and ek1 to ek, since they be past values now homie
        self.uk1 = self.uk
        self.ek1 = self.ek

    #this function will set the kp and ki by the engineer
    def setKPKI(self, kp, ki):
        self.KP = kp
        self.KI = ki
        #make sure service brake is off to start moving
        self.serviceBrake = False
        signals.train_controller_service_brake.emit()

    #this function updates the setpoint speed
    def updateSetPointSpeed(self, setPointSpeed):
        self.setpointSpeed = setPointSpeed

    #this function goes through a station stop
    def trainStationStop(self):
        while self.currentSpeed != 0:
            pass
            #wait 1 second

        #activate service brake to stop moving
        self.serviceBrake = True
        #toggle lights and doors for a station
        self.toggleDoorsLeft()
        self.toggleDoorsRight()
        self.toggleLightsInt()

        #wait 1 minute

        #deactivate the service brake to start moving again
        self.serviceBrake = False
        #toggle lights and doors
        self.toggleDoorsLeft()
        self.toggleDoorsRight()
        self.toggleLightsInt()

    #this function updates the commanded speed
    def updateCommandedSpeed(self, commandedSpeed):
        self.commandedSpeed = commandedSpeed

        if self.setpointSpeed > commandedSpeed:
            self.setpointSpeed = commandedSpeed

    #this function updates the current speed
    def updateCurrentSpeed(self, currSpeed):
        self.previousCurrentSpeed = self.currentSpeed
        self.currentSpeed = currSpeed

        #check for engine failure
        if self.previousPowerCommand == self.commandedPower and\
            self.previousCurrentSpeed > self.currentSpeed and\
            self.engineFail:

            #an engine failure is happening
            self.engineFail = True


    #this function updates the authority
    def updateAuthority(self, newAuthority):
        if newAuthority:
            if self.authority:
                if self.serviceBrake:
                    pass
                else:
                    self.serviceBrake = False
                    signals.train_controller_service_brake.emit()
            else:
                if self.KP == 0 or self.KI == 0:
                    pass
                else:
                    self.authority = newAuthority
                    self.serviceBrake = False
                    signals.train_controller_service_brake.emit()
        else:
            self.authority = newAuthority
            self.serviceBrake = True
            signals.train_controller_service_brake.emit()

    #this function updates the temp
    def updateTempValue(self, temperature):
        self.trainTemp = temperature
        signals.train_controller_temperature_value.emit(temperature)

    #this function toggles the service brake 
    def toggleServiceBrake(self):
        if self.serviceBrake == True:
            #if brake fail is occuring then must keep service brake on
            if self.brakeFail == True:
                pass
            else:
                self.serviceBrake = not self.serviceBrake
        else:
            self.serviceBrake = not self.serviceBrake

    #this function report E brake on
    def emergencyBrakeOn(self):
        self.emergencyBrake = True
        signals.train_controller_emergency_brake_on.emit()

    #this function will report e brake off
    def emergencyBrakeOff(self):
        self.emergencyBrake = False
        signals.train_controller_emergency_brake_off.emit()

    #this function will report if passenger e brake status
    def passengerEBrake(self, status):
        if status == True:
            self.emergencyBrakeOn()

    #this function will toggle modes
    def toggleModes(self):
        self.mode = not self.mode

    #this function will report left doors
    def toggleDoorsLeft(self):
        self.Ldoor = not self.Ldoor
        if self.Ldoor == True:
            signals.train_controller_left_door_closed.emit()
        else:
            signals.train_controller_left_door_open.emit()

    #this function will report right doors
    def toggleDoorsRight(self):
        self.Rdoor = not self.Rdoor
        if self.Rdoor == True:
            signals.train_controller_right_door_closed.emit()
        else:
            signals.train_controller_right_door_open.emit()

    #this function will report int lights 
    def toggleLightsInt(self):
        self.intLights = not self.intLights
        if self.intLights == True:
            signals.train_controller_int_lights_on.emit()
        else:
            signals.train_controller_int_lights_off.emit()

    #this function will report ext lights 
    def toggleLightsExt(self):
        self.extLights = not self.extLights
        if self.extLights == True:
            signals.train_controller_ext_lights_on.emit()
        else:
            signals.train_controller_ext_lights_off.emit()
        
    #this function is for announcements
    def announceStation(self, beacon):
        self.station = beacon

    #this function is for engine failure
    def engineFailure(self, failure):
        self.engineFail = failure

        #activate emergency brake
        if self.engineFail == True :
            self.emergencyBrake = True
        else:
            self.emergencyBrake = False
    
    #this function is for brake failure
    def brakeFailure(self, failure):
        self.brakeFail = failure

        #activate emergency brake
        if self.engineFail == True :
            self.emergencyBrake = True
        else:
            self.emergencyBrake = False
    
    #this function is for signal failure
    def signalFailure(self, failure):
        self.signalFail = failure

        #activate emergency brake
        if self.engineFail == True :
            self.emergencyBrake = True
        else:
            self.emergencyBrake = False

    #timing functions
    def updateCurrentTime(self, value):
        self.currentTime = value

    def setCurrentTime(self, time):
        self.current_time = time

traincontroller = trainController()




    

    




    
