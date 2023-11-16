import sys
sys.path.append(".")
from signals import signals



class TimeConstants:
    def __init__(self):
        signals.change_system_speed.connect(self.setSystemSpeed)
        # System clock constants
        self.INTERVAL = 50
        self.SYSTEM_SPEED = 1
        self.TIME_DELTA = self.INTERVAL * self.SYSTEM_SPEED
        self.START_YEAR = 2023
        self.START_MONTH = 1
        self.START_DAY = 1
        self.START_HOUR = 12
        self.START_MIN = 0
        self.START_SEC = 0    
        
    def setSystemSpeed(self, value):
        self.SYSTEM_SPEED = value   
        self.TIME_DELTA = self.INTERVAL * self.SYSTEM_SPEED
        
constants = TimeConstants()

# System clock constants
INTERVAL = constants.INTERVAL
SYSTEM_SPEED = constants.SYSTEM_SPEED
TIME_DELTA = constants.INTERVAL * constants.SYSTEM_SPEED
START_YEAR = constants.START_YEAR
START_MONTH = constants.START_MONTH
START_DAY = constants.START_DAY
START_HOUR = constants.START_HOUR
START_MIN = constants.START_MIN
START_SEC = constants.START_SEC