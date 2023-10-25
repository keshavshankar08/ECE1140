from PyQt6.QtCore import QObject, pyqtSignal, QTime
# from src.backend.SW_Wayside.Track import *

class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QTime)
    stop_timer = pyqtSignal()
    #region SW Track Controller
    # Inputs
    
    swtrack_block_occupancy = pyqtSignal()
    swtrack_track_fault_detected = pyqtSignal()
    swtrack_maintenance_active = pyqtSignal()
    swtrack_suggested_speed = pyqtSignal()
    swtrack_suggested_authority = pyqtSignal()
    swtrack_system_clock = pyqtSignal()
    swtrack_system_speed = pyqtSignal()
    
    # Outputs
    #swtrack_output = pyqtSignal(Track)
    #endregion SW Track Controller

    # Train Model
    trainModel_test_changeSpeed = pyqtSignal(float)

signals = signalsList()


