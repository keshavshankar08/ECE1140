from PyQt6.QtCore import QObject, pyqtSignal, QTime
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QTime)
    stop_timer = pyqtSignal()

    #CTC Office Signals
    ctc_office_active_trains_update = pyqtSignal(ActiveTrains)
    ctc_office_track_update = pyqtSignal(Track)
    ctc_office_backend_update = pyqtSignal(Track)
    ctc_office_frontend_update = pyqtSignal(Track)

    # SW Wayside Signals
    sw_wayside_track_update = pyqtSignal(Track)

    # Train Model Signals
    trainModel_test_changeSpeed = pyqtSignal(float)

signals = signalsList()


