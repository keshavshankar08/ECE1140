import PyQt6
from PyQt6.QtCore import QObject

class Train(QObject):
    def __init__(self):
        # PI Controller Parameters
        self.Kp = 0
        self.Ki = 0
        # Intrinsic Properties
        self.mass = 0 # kg
        self.length = 0 # m
        self.height = 0 # m
        self.width = 0 # m
        self.numberOfCars = 0 # discrete integer
        # Doors and Lights 
        self.leftDoor = "OPEN" # or "CLOSED"
        self.rightDoor = "OPEN" # or "CLOSED"
        self.interiorLight = "OFF" # or "ON"
        self.exteriorLight = "OFF" # or "ON"
        # Interior Train Temperature
        self.temperature = 0 
        # Emergency Brake - either on or off
        self.emergencyBrake = "OFF" # or "ON"
        # Service Brake - ranges from 0.0 (no brake) to 1.0 (full brake)
        self.serviceBrake = 0.0

