# Class to model a train.
# Constants reflect the properties of the Alstom/Bombardier Flexity 2.
# Written by Alex Ivensky for ECE 1140

from PyQt6.QtCore import QObject, QDateTime, pyqtSignal
from signals import signals
from Main_Backend import START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC, TIME_DELTA

import math
from enum import Enum

#### Useful Constants
CAR_LENGTH = 32.2 # meters
CAR_HEIGHT = 3.42 # meters
CAR_WIDTH = 2.65 # meters
CAR_WEIGHT_EMPTY = 40.9 # tons
CAR_WEIGHT_LOADED = 56.7 # tons
MAX_SPEED = 70 # km/h
MEDIUM_ACCEL = 0.5 # m/s^2 (2/3 load)
S_BRAKE_MAX_DECEL = 1.2 # m/s^2
E_BRAKE_DECEL = 2.73 # m/s^2
MAX_MOTOR_POWER = 120000 # Watts
GRAVITY = 9.8 # m/s^2
    

class Train(QObject):
    def __init__(self, numCars):
        super().__init__()
        #### Signals
        signals.current_system_time.connect(self.setCurrentTime)
        signals.main_backend_update_values.connect(self.TrainModelUpdateValues)
        signals.trainController_send_power_command.connect(self.setPowerCommand)
        #### Train ID
        self.train_id = 0
        #### Number of Cars
        self.numCars = numCars
        #### Number of Passengers
        self.numPassengers = 0
        #### Intrinsic Properties
        self.mass = CAR_WEIGHT_EMPTY * self.numCars # kg
        self.length = CAR_LENGTH * self.numCars # m
        self.height = CAR_HEIGHT # m
        self.width = CAR_WIDTH # m
        #### Doors - False is open, True is closed
        self.leftDoor = False 
        self.rightDoor = False
        #### Lights - False is off, True is on
        self.interiorLight = False
        self.exteriorLight = False
        #### Interior Train Temperature
        self.temperature = 60 # F
        #### Emergency Brake - either on or off
        self.emergencyBrake = False
        #### Service Brake - ranges from 0.0 (no brake) to 1.0 (full brake)
        self.serviceBrake = 0.0 # dimensionless
        #### Instantaneous Values
        self.currentSpeed = 0 # m/s
        self.previousSpeed = 0 # m/s
        self.currentAccel = 0 # m/s^2
        self.previousAccel = 0 # m/s^2
        self.accelSum = 0 # m/s^2 ??
        self.commandedPower = 0 # N*m / s
        self.engineForce = 0 # N
        self.slopeForce = 0 # N
        self.netForce = 0 # N
        self.currentAuthority = 0 # m
        self.currentBlock = 0 # dimensionless
        self.currentGradient = 0.0 # %
        self.beaconList = [] # list of all beacons received
        #### Time
        self.current_time = QDateTime(START_YEAR, START_MONTH, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC)
        #### Failure
        self.engineFail = False
        self.brakeFail = False
        self.signalFail = False
        #### Advertisements
        # not implemented haha hahahaha
        #### UI Signals
        self.displayBeacon = pyqtSignal(str)
        

    def TrainModelUpdateValues(self):
        self.previousAccel = self.currentAccel
        try:
            self.engineForce = self.commandedPower / self.currentSpeed
        except ZeroDivisionError:
            self.engineForce = 0
        self.slopeForce = self.mass * GRAVITY * math.atan(self.currentGradient / 100)
        self.netForce = self.engineForce - self.slopeForce
        self.currentAccel = self.netForce / self.mass
        
        if (self.commandedPower <= MAX_MOTOR_POWER):
            self.currentSpeed = self.currentSpeed + (TIME_DELTA / 2) * (self.currentAccel + self.previousAccel)
        else:
            self.currentSpeed = self.currentSpeed
            
        # Signals to Train Controller
        
        # Signals to Track Model

    def trainModelServiceBrake(self, value):
        pass

    def onEmergencyBrake(self):
        self.emergencyBrake = True
        
    def offEmergencyBrake(self):
        self.emergencyBrake = False

    def onInteriorLights(self):
        self.interiorLight = True
    
    def offInteriorLights(self):
        self.interiorLight = False

    def onExteriorLights(self):
        self.exteriorLight = True
    
    def offExteriorLights(self):
        self.exteriorLight = False

    def openLeftDoors(self):
        self.leftDoor = False
    
    def closeLeftDoors(self):
        self.leftDoor = True

    def openRightDoors(self):
        self.rightDoor = False
    
    def closeLeftDoors(self):
        self.leftDoor = True

    def setTemperature(self, value):
        pass
    
    def setCurrentTime(self, time):
        self.current_time = time
        
    def setPowerCommand(self, value):
        self.commandedPower = value
        
    def receiveBeacon(self, beacon):
        self.beaconList.append(beacon)
        
    def receiveSuggestedSpeed(self, value):
        pass
    
    def receiveSuggestedAuthority(self, value):
        pass
    
    def receiveSpeedLimit(self, value):
        pass
    
    def showAdvertisement(self):
        pass
    
    
        

    


