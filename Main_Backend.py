import sys
sys.path.append(".")
from PyQt6.QtCore import QTimer, QThread, QCoreApplication, QObject, QDateTime
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *
from Modules.CTC.Backend.CTC_Backend import *
from Modules.SW_Wayside.Backend.SW_Wayside_Backend import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Track_Resources.PLC import *
from Main_UI import *

# System clock constants
INTERVAL = 50
SYSTEM_SPEED = 5
TIME_DELTA = INTERVAL * SYSTEM_SPEED
START_YEAR = 2023
START_MONTH = 1
START_DAY = 1
START_HOUR = 12
START_MIN = 0
START_SEC = 0

class SystemTime(QObject):
    def __init__(self):
        super().__init__()
        self.current_time = QDateTime(START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC)
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.timerHandler)
        signals.stop_timer.connect(self.stopTimer)
        self.system_timer.start(INTERVAL)
        
        # SW Wayside Instances
        self.sw_wayside_backend_instance = WaysideBackend()
        self.plc_instance = PLC()
        self.track_instance = Track()
        signals.sw_wayside_backend_update.connect(self.updateTrackInstance)      
        
        self.menu_instance = Mainmenu()
        self.menu_instance.show()

    def timerHandler(self):
        self.current_time = self.current_time.addMSecs(TIME_DELTA)
        signals.current_system_time.emit(self.current_time) #Y:M:D:h:m:s
        signals.sw_wayside_update_backend.emit(self.track_instance) #sends current state of track out
        

    def stopTimer(self):
        self.system_timer.stop()

    #CTC Office Instance Updaters
    def updateActiveTrains(self, updatedActiveTrains):
        self.activeTrains = updatedActiveTrains

    # SW Wayside Instance Updaters
    def updateTrackInstance(self, updatedTrack):
        self.track_instance = updatedTrack

if __name__ == '__main__':
        app = QApplication([])
        thread = QThread() 
        system_time = SystemTime()
        system_time.moveToThread(thread) 
        thread.start()
        sys.exit(app.exec())

