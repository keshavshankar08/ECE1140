import sys
sys.path.append(".")
from PyQt6.QtCore import QTime, QTimer, QThread, QCoreApplication, QObject
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *
from Modules.CTC.Backend.CTC_Backend import *
from Modules.SW_Wayside.Backend.SW_Wayside_Backend import *

# System clock constants
INTERVAL = 50
SYSTEM_SPEED = 5
TIME_DELTA = INTERVAL * SYSTEM_SPEED
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

        #CTC Office Instances
        self.activeTrains = ActiveTrains()
        signals.ctc_office_track_update.connect(self.updateTrackInstance)
        signals.ctc_office_active_trains_update.connect(self.updateActiveTrains)

        # SW Wayside Instances
        self.trackInstance = Track()
        signals.sw_wayside_track_update.connect(self.updateTrackInstance)        

    def timerHandler(self):
        self.current_time = self.current_time.addMSecs(TIME_DELTA)
        signals.current_system_time.emit(self.current_time)

    def stopTimer(self):
        self.system_timer.stop()

    #CTC Office Instance Updaters
    def updateActiveTrains(self, updatedActiveTrains):
        self.activeTrains = updatedActiveTrains

    # SW Wayside Instance Updaters
    def updateTrackInstance(self, updatedTrack):
        self.trackInstance = updatedTrack

mainInstance = SystemTime()

