from PyQt6.QtCore import QObject, pyqtSignal, QTime
from Track_Resources.Track import *

class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QTime)
    stop_timer = pyqtSignal()

    #region SW Track Controller
    swtrack_update_track = pyqtSignal(Track)
    swtrack_track = pyqtSignal(Track)
    #endregion SW Track Controller

    # Train Model
    trainModel_test_changeSpeed = pyqtSignal(float)

signals = signalsList()


