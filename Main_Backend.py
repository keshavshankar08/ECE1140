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


class MainBackend(QObject):
    def __init__(self):
        super().__init__()
        self.current_time = QDateTime(constants.START_YEAR, constants.START_MONTH, constants.START_DAY, constants.START_HOUR, constants.START_MIN, constants.START_SEC)
        self.system_timer = QTimer()
        self.system_timer.timeout.connect(self.timerHandler)
        signals.stop_timer.connect(self.stopTimer)
        self.system_timer.start(constants.INTERVAL)
        
        # CTC Office Instances
        self.ctc_office_backend_instance = CTCBackend()
        self.active_trains_instance = ActiveTrains()
        self.ticket_sales_instance = 0
        signals.ctc_office_backend_update.connect(self.ctc_office_backend_update)

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
        self.current_time = self.current_time.addMSecs(int(constants.TIME_DELTA))
        signals.current_system_time.emit(self.current_time) #Y:M:D:h:m:s
        signals.ctc_office_update_backend.emit(self.track_instance, self.active_trains_instance, self.ticket_sales_instance)
        signals.sw_wayside_update_backend.emit(self.track_instance, self.active_trains_instance)
        signals.trainModel_backend_update.emit()

    def stopTimer(self):
        self.system_timer.stop()

    #Handler for uppdate from CTC Office
    def ctc_office_backend_update(self, updated_track, updated_active_trains, updated_ticket_sales):
        self.update_track_instance(updated_track)
        self.update_active_trains(updated_active_trains)
        self.update_ticket_sales(updated_ticket_sales)
        
    # Handler for update from SW Wayside
    def sw_wayside_backend_update(self, updated_track, updated_active_trains):
        self.update_active_trains(updated_active_trains)
        self.update_track_instance(updated_track)

    # Active trains instance updater
    def update_active_trains(self, updated_active_trains):
        self.active_trains_instance = updated_active_trains

    def update_ticket_sales(self, updated_ticket_sales):
         self.ticket_sales_instance = updated_ticket_sales

    # Track instance updater
    def update_track_instance(self, updated_track):
        self.track_instance = updated_track
        
    def updateMainMenu(self):
        pass

if __name__ == '__main__':
        app = QApplication([])
        thread = QThread() 
        backend = MainBackend()
        backend.moveToThread(thread) 
        thread.start()
        sys.exit(app.exec())

