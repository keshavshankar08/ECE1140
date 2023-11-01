# Class to model a train.
# Constants reflect the properties of the Alstom/Bombardier Flexity 2.
# Written by Alex Ivensky for ECE 1140

from PyQt6.QtCore import QObject, QTime
from signals import signals
from Main_Backend import START_HOUR, START_MIN, START_SEC, TIME_DELTA

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

class TrainEnums(Enum):
    DOOR_CLOSED = "CLOSED"
    DOOR_OPEN = "OPEN"
    LIGHT_ON = "ON"
    LIGHT_OFF = "OFF"
    E_BRAKE_OFF = "OFF"
    E_BRAKE_ON = "ON"
    NORMAL = 0
    ENGINE_FAIL = 1
    BRAKE_FAIL = 2
    SIGNAL_FAIL = 3
    

class Train(QObject):
    def __init__(self):
        super().__init__()
        #### Signals
        signals.current_system_time.connect(self.setCurrentTime)
        signals.main_backend_update_values.connect(self.TrainModelUpdateValues)
        signals.trainController_send_power_command.connect(self.setPowerCommand)
        #### Train ID
        self.train_id = 0
        #### Number of Cars
        self.numCars = 1
        #### Number of Passengers
        self.numPassengers = 0
        #### Intrinsic Properties
        self.mass = CAR_WEIGHT_EMPTY * self.numCars # kg
        self.length = CAR_LENGTH * self.numCars # m
        self.height = CAR_HEIGHT # m
        self.width = CAR_WIDTH # m
        #### Doors and Lights 
        self.leftDoor = TrainEnums.DOOR_CLOSED
        self.rightDoor = TrainEnums.DOOR_CLOSED
        self.interiorLight = TrainEnums.LIGHT_OFF
        self.exteriorLight = TrainEnums.LIGHT_OFF
        #### Interior Train Temperature
        self.temperature = 60 # F
        #### Emergency Brake - either on or off
        self.emergencyBrake = TrainEnums.E_BRAKE_OFF
        #### Service Brake - ranges from 0.0 (no brake) to 1.0 (full brake)
        self.serviceBrake = 0.0 # dimensionless
        #### Instantaneous Values
        self.currentSpeed = 0 # m/s
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
        self.current_time = QTime(START_HOUR, START_MIN, START_SEC)
        #### Failure
        self.current_failureMode = TrainEnums.NORMAL
        #### Advertisemenets
        

    def TrainModelUpdateValues(self):
        self.previousAccel = self.currentAccel
        self.engineForce = self.commandedPower / self.currentSpeed
        self.slopeForce = self.mass * GRAVITY * math.atan(self.currentGradient / 100)
        self.netForce = self.engineForce - self.slopeForce
        self.currentAccel = self.netForce / self.mass
        
        if (self.commandedPower <= MAX_MOTOR_POWER):
            self.currentSpeed = self.currentSpeed + (TIME_DELTA / 2) * (self.currentAccel + self.previousAccel)
        else:
            self.currentSpeed = self.currentSpeed
            
        # emit wherever

    def trainModelServiceBrake(self, value):
        pass

    def onEmergencyBrake(self):
        self.emergencyBrake = TrainEnums.E_BRAKE_OFF
        
    def offEmergencyBrake(self):
        self.emergencyBrake = TrainEnums.E_BRAKE_ON

    def onInteriorLights(self):
        self.interiorLight = TrainEnums.LIGHT_ON
    
    def offInteriorLights(self):
        self.interiorLight = TrainEnums.LIGHT_OFF

    def onExteriorLights(self):
        self.exteriorLight = TrainEnums.LIGHT_ON
    
    def offExteriorLights(self):
        self.exteriorLight = TrainEnums.LIGHT_OFF

    def openLeftDoors(self):
        self.leftDoor = TrainEnums.DOOR_OPEN
    
    def closeLeftDoors(self):
        self.leftDoor = TrainEnums.DOOR_CLOSED

    def openRightDoors(self):
        self.rightDoor = TrainEnums.DOOR_OPEN
    
    def closeLeftDoors(self):
        self.leftDoor = TrainEnums.DOOR_CLOSED

    def setTemperature(self, value):
        pass
    
    def setCurrentTime(self, time):
        self.current_time = time
        
    def setPowerCommand(self, value):
        self.commandedPower = value
        
    def receiveBeacon(self, beacon):
        self.beaconList.append(beacon)
        

    


