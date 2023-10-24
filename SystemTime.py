from PyQt6.QtCore import QTime, QTimer, Qt, QCoreApplication, QObject
import time

class SystemTime(QObject):
    def __init__(self):
        # System Speed Chosen By User
        self.systemSpeed = 1.0
        # HH:MM:SS info
        self.currentTime = QTime(0, 0, 0) # starting at 00:00:00 for now
        ##### CAUTION - THIS VALUE SHOULD NOT BE CHANGED  #####
        self.timerPeriod = 0.005 # timer will have a period of 50 ms
        # Time Delta for Module Calculations
        self.timeDelta_MS = (self.timerPeriod) * self.systemSpeed # time delta that should be used by individual modules for their time-related calculations.
        # for example, if system speed is set to 1, then the time delta will be 50 ms, as standard.
        # if system speed is set to 3, the time delta will be 150 ms, but 50 ms will have passed between actual timer iterations.

    def run(self):
        self.app.exec()


timerTest = SystemTime()
print(timerTest.currentTime.hour())

