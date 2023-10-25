from PyQt6.QtCore import QTime, QTimer, QThread, QCoreApplication, QObject
from signals import signals
import sys

# CONSTANTS
INTERVAL = 50
SYSTEM_SPEED = 1
TIME_DELTA = INTERVAL * SYSTEM_SPEED
START_HOUR = 8
START_MIN = 38
START_SEC = 0

class SystemTime(QObject):
    def __init__(self):
        super().__init__()
        self.current_time = QTime(START_HOUR, START_MIN, START_SEC)
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.timerHandler)
        signals.stop_timer.connect(self.stopTimer)
        self.system_timer.start(INTERVAL)


    def timerHandler(self):
        self.current_time = self.current_time.addMSecs(TIME_DELTA)
        signals.current_system_time.emit(self.current_time)

    def stopTimer(self):
        self.system_timer.stop()
