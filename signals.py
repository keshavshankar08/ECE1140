from PyQt6.QtCore import QObject, pyqtSignal, QTime
from Track_Resources.Track import *

class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QTime)
    stop_timer = pyqtSignal()

    # SW Wayside Signals
    sw_wayside_track_update = pyqtSignal(Track)

    # Train Model Signals
    trainModel_test_changeSpeed = pyqtSignal(float)

signals = signalsList()


