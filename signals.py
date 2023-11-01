from PyQt6.QtCore import QObject, pyqtSignal, QTime
from Track_Resources.Track import *

class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QTime)
    stop_timer = pyqtSignal()
    main_backend_update_values = pyqtSignal()
    main_backend_update_track = pyqtSignal(Track)

    # SW Wayside Signals
    sw_wayside_track_update = pyqtSignal(Track)

    # Train Model Signals
    trainModel_test_changeSpeed = pyqtSignal(float)
    trainModel_send_actual_velocity = pyqtSignal(float)
    
    # Train Controller Signals
    trainController_send_power_command = pyqtSignal(float)

signals = signalsList()


