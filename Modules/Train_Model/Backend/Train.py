import PyQt6
from PyQt6.QtCore import QObject

# Useful Constants
CAR_LENGTH = 32.2 # m
CAR_HEIGHT = 3.42 # m
CAR_WIDTH = 2.65 # m
CAR_WEIGHT_EMPTY = 40.9 # t
CAR_WEIGHT_LOADED = 56.7 # t
MAX_SPEED = 70 # km/h
MEDIUM_ACCEL = 0.5 # m/s^2 (2/3 load)
S_BRAKE_MAX_DECEL = 1.2 # m/s^2
E_BRAKE_DECEL = 2.73 # m/s^2

# Class to model a train.
# Written by Alex Ivensky

class Train(QObject):
    def __init__(self):
        super().__init__()
        #Train ID
        self.train_id = 0
        # Number of Cars
        self.numCars = 1
        # Number of Passengers
        self.numPassengers = 0
        # PI Controller Parameters
        self.Kp = 0
        self.Ki = 0
        # Intrinsic Properties
        self.mass = CAR_WEIGHT_EMPTY * self.numCars # kg
        self.length = CAR_LENGTH * self.numCars # m
        self.height = CAR_HEIGHT # m
        self.width = CAR_WIDTH # m
        # Doors and Lights 
        self.leftDoor = "CLOSED" # or "OPEN"
        self.rightDoor = "CLOSED" # or "OPEN"
        self.interiorLight = "OFF" # or "ON"
        self.exteriorLight = "OFF" # or "ON"
        # Interior Train Temperature
        self.temperature = 60 # F
        # Emergency Brake - either on or off
        self.emergencyBrake = "OFF" # or "ON"
        # Service Brake - ranges from 0.0 (no brake) to 1.0 (full brake)
        self.serviceBrake = 0.0 # dimensionless
        # Instantaneous Values
        self.currentSpeed = 0 # m/s
        self.currentAccel = 0 # m/s^2
        self.commandedPower = 0 # N*m / s
        self.currentAuthority = 0 # m
        self.currentBlock = 0 # dimensionless
        self.beaconList = [] # list of all beacons received



