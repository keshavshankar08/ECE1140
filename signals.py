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
    sw_wayside_update_backend = pyqtSignal(Track) # update from main backend to sw wayside backend
    sw_wayside_update_frontend = pyqtSignal(Track) # update from sw wayside backend to sw wayside frontend
    sw_wayside_frontend_update = pyqtSignal(Track) # update from sw wayside frontend to sw wayside backend
    sw_wayside_backend_update = pyqtSignal(Track) # update from sw wayside backend to main backend

    # HW Wayisde Singnals
    hw_wayside_update_backend = pyqtSignal(Track)
    hw_wayside_update_frontend = pyqtSignal(Track)
    hw_wayside_frontend_update = pyqtSignal(Track)
    hw_wayside_backend_update = pyqtSignal(Track)
    '''
    Main Backend    ->  SW Wayside Backend  ->  SW Wayside Frontend
                                                        |
                                                        ▼
                        Main Backend    <-      SW Wayside Backend             
    '''
    
    
    # Track Model
    track_model_block_occupancy = pyqtSignal(int)
    track_model_ticket_sales = pyqtSignal(int)
    track_model_speed_limit = pyqtSignal(int)
    track_model_authority = pyqtSignal(float)
    track_model_beacon = pyqtSignal(str)
    # Train Model Signals
    trainModel_backend_update = pyqtSignal()
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
    
    #Train Controller Signals
    #lights
    train_controller_int_lights_on = pyqtSignal(bool)
    train_controller_int_lights_off = pyqtSignal(bool)
    train_controller_ext_lights_on = pyqtSignal(bool)
    train_controller_ext_lights_off = pyqtSignal(bool)
    #doors
    train_controller_right_door_closed = pyqtSignal(bool)
    train_controller_right_door_open = pyqtSignal(bool)
    train_controller_left_door_closed = pyqtSignal(bool)
    train_controller_left_door_open = pyqtSignal(bool)
    #Bower
    train_controller_send_power_command = pyqtSignal(float)
    #Temperature
    train_controller_temperature_value = pyqtSignal(float)
    #Braking
    train_controller_service_brake = pyqtSignal(float)
    train_controller_emergency_brake_on = pyqtSignal(bool)
    train_controller_emergency_brake_off = pyqtSignal(bool)


signals = signalsList()


