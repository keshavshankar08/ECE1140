# Class to model a train.
# Constants reflect the properties of the Alstom/Bombardier Flexity 2.
# Written by Alex Ivensky for ECE 1140

from PyQt6.QtCore import QObject, QDateTime, pyqtSignal
import sys
sys.path.append(".")
from signals import signals
from Main_Backend import START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC, TIME_DELTA

import math

#### Useful Constants
CAR_LENGTH = 32.2 # meters
CAR_HEIGHT = 3.42 # meters
CAR_WIDTH = 2.65 # meters
CAR_WEIGHT_EMPTY = 37103.86 # kg
CAR_WEIGHT_LOADED = 51437.37 # kg
MAX_SPEED = 70 # km/h
S_BRAKE_FORCE = 61716 # N
E_BRAKE_FORCE = 140404 # N
MAX_MOTOR_POWER = 120000 # Watts
GRAVITY = 9.8 # m/s^2
    

class Train(QObject):
    def __init__(self):
        super().__init__()
        #### Signals
        signals.current_system_time.connect(self.setCurrentTime)
        signals.main_backend_update_values.connect(self.TrainModelUpdateValues)
        signals.trainController_send_power_command.connect(self.setPowerCommand)
        #### Train ID
        self.train_id = 0
        #### Number of Passengers
        self.numPassengers = 0
        #### Intrinsic Properties
        self.mass = CAR_WEIGHT_EMPTY # kg
        self.length = CAR_LENGTH # m
        self.height = CAR_HEIGHT # m
        self.width = CAR_WIDTH # m
        #### Doors - False is open, True is closed
        self.leftDoor = False 
        self.rightDoor = False
        #### Lights - False is off, True is on
        self.interiorLight = False
        self.exteriorLight = False
        #### Interior Train Temperature
        self.temperatureCommand = 60.0 # F
        self.temperatureActual = 60.0 # F
        #### Emergency Brake - either on or off
        self.emergencyBrake = False
        #### Service Brake - either on or off
        self.serviceBrake = False
        #### Instantaneous Values
        ## Speed
        self.currentSpeed = 0.0 # m/s
        self.previousSpeed = 0.0 # m/s
        self.currentAccel = 0.0 # m/s^2
        self.previousAccel = 0.0 # m/s^2
        self.accelSum = 0.0 # m/s^2 ??
        ## Force
        self.commandedPower = 0.0 # N*m / s
        self.engineForce = 0.0 # N
        self.slopeForce = 0.0 # N
        self.netForce = 0.0 # N
        self.brakeForce = 0.0 # N
        ## Track
        self.currentAuthority = 0.0 # m
        self.currentBlock = 0 # dimensionless
        self.trackPolarity = 1 # or -1
        self.currentGradient = 0.0 # %
        self.distanceFromYard = 0.0
        self.distanceFromBlockStart = 0.0
        self.currentBeacon = None
        self.beaconList = [] # list of all beacons received
        #### Time
        self.current_time = QDateTime(START_YEAR, START_MONTH, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC)
        #### Failure
        self.engineFail = False
        self.brakeFail = False
        self.signalFail = False
        #### Advertisements
        # not implemented haha hahahaha
        #### Passthroughs
        self.speedLimit = 0.0
        
        

    def TrainModelUpdateValues(self):
        self.previousAccel = self.currentAccel
        if (self.serviceBrake and not self.emergencyBrake):
            self.brakeForce = S_BRAKE_FORCE
        if (self.emergencyBrake):
            self.brakeForce = E_BRAKE_FORCE
            self.commandedPower = 0
        if (not self.emergencyBrake and not self.serviceBrake):
            self.brakeForce = 0
        try:
            self.engineForce = abs(self.commandedPower / self.currentSpeed)
        except ZeroDivisionError:
            if (self.commandedPower > 0):
                self.currentSpeed = 0.01 # ????
        self.slopeForce = self.mass * GRAVITY * math.sin(math.atan(self.currentGradient / 100))
        self.netForce = self.engineForce - self.slopeForce - self.brakeForce
        self.currentAccel = self.netForce / self.mass
        
        if (self.commandedPower <= MAX_MOTOR_POWER):
            self.currentSpeed = self.currentSpeed + (TIME_DELTA * 0.001 / 2) * (self.currentAccel + self.previousAccel)
            
        if (self.currentSpeed < 0):
            self.currentSpeed = 0
            
        if (self.currentSpeed > MAX_SPEED):
            self.currentSpeed = MAX_SPEED
            
        # Signals to Train Controller
        signals.trainModel_send_engine_failure.emit(self.engineFail)
        signals.trainModel_send_signal_failure.emit(self.signalFail)
        signals.trainModel_send_brake_failure.emit(self.brakeFail)
        signals.trainModel_send_actual_velocity.emit(self.currentSpeed)
        signals.trainModel_send_emergency_brake.emit(self.emergencyBrake)
        # Signals to Track Model
        signals.trainModel_send_train_length.emit(self.length)
        signals.trainModel_send_distance_from_block_start.emit(self.distanceFromBlockStart)
        signals.trainModel_send_distance_from_yard.emit(self.distanceFromYard)

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

    def receiveTemperature(self, value):
        self.temperatureCommand = value
    
    def setCurrentTime(self, time):
        self.current_time = time
        
    def setPowerCommand(self, value):
        self.commandedPower = value
        
    def receiveBeacon(self, beacon):
        self.beaconList.append(beacon)
    
    def showAdvertisement(self):
        pass
    
    
        

    


