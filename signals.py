from PyQt6.QtCore import QObject, pyqtSignal
from src.backend.SW_Wayside.Track import *

class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QTime)
    stop_timer = pyqtSignal()
    main_backend_update_values = pyqtSignal()
    main_backend_update_track = pyqtSignal(Track)

    # SW Wayside Signals
    sw_wayside_update_backend = pyqtSignal(Track) # update from main backend to sw wayside backend
    sw_wayside_update_frontend = pyqtSignal(Track) # update from sw wayside backend to sw wayside frontend
    sw_wayside_frontend_update = pyqtSignal(Track) # update from sw wayside frontend to sw wayside backend
    sw_wayside_backend_update = pyqtSignal(Track) # update from sw wayside backend to main backend
    '''
    Main Backend    ->  SW Wayside Backend  ->  SW Wayside Frontend
                                                        |
                                                        ▼
                        Main Backend    <-      SW Wayside Backend             
    '''
    

    # Train Model Signals
    trainModel_test_changeSpeed = pyqtSignal(float)
    trainModel_send_actual_velocity = pyqtSignal(float)
    
    # Train Controller Signals
    trainController_send_power_command = pyqtSignal(float)

signals = signalsList()


