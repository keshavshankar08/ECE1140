from PyQt6.QtCore import QTime, QTimer, QThread, QCoreApplication, QObject
from signals import signals
import sys

# CONSTANTS
INTERVAL = 50
START_HOUR = 12
START_MIN = 0
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
        self.current_time = self.current_time.addMSecs(INTERVAL)
        signals.current_system_time.emit(self.current_time)

    def stopTimer(self):
        self.system_timer.stop()
