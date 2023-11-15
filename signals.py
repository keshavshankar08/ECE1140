from PyQt6.QtCore import QObject, pyqtSignal, QDateTime
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *


class signalsList(QObject):
    #Timer
    current_system_time = pyqtSignal(QDateTime)
    stop_timer = pyqtSignal()

    #CTC Office Signals
    ctc_office_active_trains_update = pyqtSignal(ActiveTrains)
    ctc_office_track_update = pyqtSignal(Track)
    ctc_office_backend_update = pyqtSignal(Track)
    ctc_office_frontend_update = pyqtSignal(Track)

    # SW Wayside Signals
    sw_wayside_update_backend = pyqtSignal(Track, ActiveTrains) # update from main backend to sw wayside backend
    sw_wayside_update_plc = pyqtSignal(Track, ActiveTrains, str, int, int) # update from sw wayside backend to plc
    sw_wayside_update_frontend = pyqtSignal(Track) # update from sw wayside backend to sw wayside frontend
    sw_wayside_frontend_update = pyqtSignal(Track, str, int, int, str) # update from sw wayside frontend to sw wayside backend
    sw_wayside_plc_update = pyqtSignal(Track, ActiveTrains) # update from plc to sw wayside backend
    sw_wayside_backend_update = pyqtSignal(Track, ActiveTrains) # update from sw wayside backend to main backend
    
    # Track Model
    track_model_block_occupancy = pyqtSignal(int)
    track_model_ticket_sales = pyqtSignal(int)
    track_model_speed_limit = pyqtSignal(int)
    track_model_authority = pyqtSignal(float)
    track_model_beacon = pyqtSignal(str)
    # Train Model Signals
    trainModel_send_actual_velocity = pyqtSignal(float)
    trainModel_send_emergency_brake = pyqtSignal(bool)
    trainModel_send_suggested_speed = pyqtSignal(float)
    trainModel_send_authority = pyqtSignal(float)
    trainModel_send_speed_limit = pyqtSignal(float)
    trainModel_send_beacon = pyqtSignal(str)
    trainModel_send_train_length = pyqtSignal(float)
    trainModel_send_distance_from_yard = pyqtSignal(float)
    trainModel_send_distance_from_block_start = pyqtSignal(float)
    trainModel_send_engine_failure = pyqtSignal(bool)
    trainModel_send_brake_failure = pyqtSignal(bool)
    trainModel_send_signal_failure = pyqtSignal(bool)
    
    # Train Controller Signals
    trainController_send_power_command = pyqtSignal(float)

signals = signalsList()


