import sys
sys.path.append(".")
from PyQt6.QtCore import QTimer, QThread, QCoreApplication, QObject, QDateTime
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *
from Modules.CTC.Backend.CTC_Backend import *
from Modules.SW_Wayside.Backend.SW_Wayside_Backend import *
from Modules.SW_Wayside.Frontend.SW_Wayside_UI import *
from Modules.Track_Model.Backend.Track_Model_Backend import *
from Modules.Track_Model.Frontend.Track_Model_UI import *
from Track_Resources.PLC import *
from Main_UI import *
from CONSTANTS import *


class SystemTime(QObject):
    def __init__(self):
        super().__init__()
        self.current_time = QDateTime(START_YEAR, START_MONTH, START_DAY, START_HOUR, START_MIN, START_SEC)
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.timerHandler)
        signals.stop_timer.connect(self.stopTimer)
        self.system_timer.start(INTERVAL)
        
        # CTC Instances
        self.active_trains_instance = ActiveTrains()

        # SW Wayside Instances
        self.sw_wayside_backend_instance = WaysideBackend()
        self.plc_instance = PLC()
        self.track_instance = Track()
        signals.sw_wayside_backend_update.connect(self.sw_wayside_backend_update)

        # Track Model Instances
        self.track_model_backend_instance = TrackModelModule()     
        self.track_instance = Track()
        signals.track_model_backend_update.connect(self.update_track_instance)
        
        self.menu_instance = Mainmenu()
        self.menu_instance.show()

    def timerHandler(self):
        self.current_time = self.current_time.addMSecs(TIME_DELTA)
        signals.current_system_time.emit(self.current_time) #Y:M:D:h:m:s
        signals.sw_wayside_update_backend.emit(self.track_instance, self.active_trains_instance)
        signals.trainModel_backend_update.emit()

    def stopTimer(self):
        self.system_timer.stop()

    # Handler for update from SW Wayside
    def sw_wayside_backend_update(self, updated_track, updated_active_trains):
        self.update_active_trains(updated_active_trains)
        self.update_track_instance(updated_track)

    # Active trains instance updater
    def update_active_trains(self, updated_active_trains):
        self.active_trains_instance = updated_active_trains

    # Track instance updater
    def update_track_instance(self, updated_track):
        self.track_instance = updated_track
        
    def updateMainMenu(self):
        pass

if __name__ == '__main__':
        app = QApplication([])
        thread = QThread() 
        system_time = SystemTime()
        system_time.moveToThread(thread) 
        thread.start()
        sys.exit(app.exec())

