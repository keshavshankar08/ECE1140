# Class to model a train.
# Constants reflect the properties of the Alstom/Bombardier Flexity 2.
# Written by Alex Ivensky for ECE 1140

from PyQt6.QtCore import QObject, QDateTime, pyqtSignal
import sys
sys.path.append(".")
from signals import signals
from CONSTANTS import START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC, TIME_DELTA

import math

#### Useful Constants
CAR_LENGTH = 32.2 # meters
CAR_HEIGHT = 3.42 # meters
CAR_WIDTH = 2.65 # meters
CAR_WEIGHT_EMPTY = 37103.86 # kg
CAR_WEIGHT_LOADED = 51437.37 # kg
MAX_SPEED = 19.444 # m/s
S_BRAKE_FORCE = 61716 # N
E_BRAKE_FORCE = 140404 # N
MAX_MOTOR_POWER = 120000 # Watts
GRAVITY = 9.8 # m/s^2
MAX_ENGINE_FORCE = 40000 # N
FRICTION_COEFF = 0 # dimensionless
    

class Train(QObject):
    def __init__(self):
        super().__init__()
        #### Signals
        signals.current_system_time.connect(self.setCurrentTime)
        signals.trainModel_backend_update.connect(self.TrainModelUpdateValues)
        signals.train_controller_send_power_command.connect(self.setPowerCommand)
        signals.train_controller_emergency_brake_off.connect(self.offEmergencyBrake)
        signals.train_controller_emergency_brake_on.connect(self.onEmergencyBrake)
        signals.train_controller_ext_lights_off.connect(self.offExteriorLights)
        signals.train_controller_ext_lights_on.connect(self.onExteriorLights)
        signals.train_controller_int_lights_off.connect(self.offInteriorLights)
        signals.train_controller_int_lights_on.connect(self.onInteriorLights)
        signals.train_controller_left_door_closed.connect(self.closeLeftDoors)
        signals.train_controller_right_door_closed.connect(self.closeRightDoors)
        signals.train_controller_left_door_open.connect(self.openLeftDoors)
        signals.train_controller_right_door_open.connect(self.openRightDoors)
        signals.train_controller_service_brake.connect(self.serviceBrakeReceive)
        signals.train_controller_temperature_value.connect(self.receiveTemperature)
        signals.current_system_time.connect(self.setCurrentTime)
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
        self.frictionForce = 0.0 # N
        ## Track
        self.currentAuthority = 0.0 # m
        self.currentBlock = 0 # dimensionless
        self.trackPolarity = 1 # or -1
        self.currentGradient = 0.0 # %
        self.currentAngle = 0.0 # radians
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
        self.speedLimit = 70.0
        self.currentTime = QDateTime()
        
    def updateCurrentTime(self, value):
        self.currentTime = value
        

    def TrainModelUpdateValues(self):
        self.previousAccel = self.currentAccel
        ### BRAKE
        if (self.serviceBrake and not self.emergencyBrake):
            self.brakeForce = S_BRAKE_FORCE
        if (self.emergencyBrake):
            self.brakeForce = E_BRAKE_FORCE
            self.commandedPower = 0
        if (not self.emergencyBrake and not self.serviceBrake):
            self.brakeForce = 0
        ### ENGINE
        try:
            self.engineForce = abs(self.commandedPower / self.currentSpeed)
        except ZeroDivisionError:
            if (self.commandedPower > 0):
                self.currentSpeed = 0.1 # ????
        ### SLOPE
        self.currentAngle = math.atan(self.currentGradient / 100)
        self.slopeForce = self.mass * GRAVITY * math.sin(self.currentAngle)
        ### FRICTION
        self.frictionForce = self.mass * GRAVITY * FRICTION_COEFF * math.cos(self.currentAngle)
        
        
        self.netForce = self.engineForce - self.slopeForce - self.brakeForce - self.frictionForce
        if (self.netForce > MAX_ENGINE_FORCE):
            self.netForce = MAX_ENGINE_FORCE
        self.currentAccel = self.netForce / self.mass
        
        if (self.commandedPower <= MAX_MOTOR_POWER):
            self.currentSpeed = self.currentSpeed + (TIME_DELTA * 0.001 / 2) * (self.currentAccel + self.previousAccel)
            
        if (self.currentSpeed < 0):
            self.currentSpeed = 0
            
        if (self.currentSpeed > MAX_SPEED):
            self.currentSpeed = MAX_SPEED
            
        if (self.currentSpeed > self.speedLimit):
            self.currentSpeed = self.speedLimit
        
            
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
    
    def serviceBrakeReceive(self, value):
        if (value == 1):
            self.serviceBrake = True
        else:
            self.serviceBrake = False

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
    
    def closeRightDoors(self):
        self.rightDoor = True

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
    
    
trains = {
    1: Train()
}
        

    


