from PyQt6.QtCore import QObject, pyqtSignal, QDateTime
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class signalsList(QObject):
    # Timer signals
    current_system_time = pyqtSignal(QDateTime)
    current_system_speed = pyqtSignal(float)
    change_system_speed = pyqtSignal(float)
    stop_timer = pyqtSignal()
    pause_timer = pyqtSignal()
    resume_timer = pyqtSignal()

    # ADMIN signals
    update_admin = pyqtSignal(Track, ActiveTrains) # update from main backend to admin
    admin_update = pyqtSignal(Track, ActiveTrains, int) # update from admin to main backend

    # CTC signals
    ctc_office_update_backend = pyqtSignal(Track, ActiveTrains, int) # update from main backend to ctc office backend
    ctc_office_update_frontend = pyqtSignal(Track, ActiveTrains, int) # update from ctc office backend to ctc office frontend
    ctc_office_frontend_update = pyqtSignal(Track, ActiveTrains, int, QueueTrains) # update from ctc office frontend to ctc office backend
    ctc_office_backend_update = pyqtSignal(Track, ActiveTrains, int) # update from ctc office backend to main backend
    ctc_added_train = pyqtSignal(int)
    ctc_removed_train = pyqtSignal(int)

    # SW Wayside Signals
    sw_wayside_update_backend = pyqtSignal(Track, ActiveTrains) # update from main backend to sw wayside backend
    sw_wayside_update_plc = pyqtSignal(Track, ActiveTrains, str, int, int) # update from sw wayside backend to plc
    sw_wayside_update_frontend = pyqtSignal(Track) # update from sw wayside backend to sw wayside frontend
    
    sw_wayside_frontend_update = pyqtSignal(Track, str, int, int, str) # update from sw wayside frontend to sw wayside backend
    sw_wayside_plc_update = pyqtSignal(Track, ActiveTrains) # update from plc to sw wayside backend
    sw_wayside_backend_update = pyqtSignal(Track, ActiveTrains) # update from sw wayside backend to main backend

    wayside_choice = pyqtSignal(bool) # which wayside is chosen at start (false = sw, true = hw)

    # HW Wayside signals
    hw_wayside_update_backend = pyqtSignal(Track, ActiveTrains) # update main backend to hw
    hw_wayside_update_frontend = pyqtSignal(Track) # update hw backend to frontend
    hw_wayside_update_plc = pyqtSignal(Track, ActiveTrains, str, int, int) # hw wayside to plc

    hw_wayside_frontend_update = pyqtSignal(Track, str, int, int, str) # update hw wayside frontend to sw wayside backend
    hw_wayside_plc_update = pyqtSignal(Track, ActiveTrains) # update from plc to hw wayside backend
    hw_wayside_backend_update = pyqtSignal(Track, ActiveTrains) # update from hw wayside backend to main backend
    
    # Track Model signals
    track_model_update_backend = pyqtSignal(Track,ActiveTrains)
    track_model_backend_update = pyqtSignal(Track)
    track_model_block_occupancy = pyqtSignal(int)
    track_model_ticket_sales = pyqtSignal(list)
    track_model_speed_limit = pyqtSignal(int,int)
    track_model_track_circuit_polarity = pyqtSignal(int)
    track_model_suggested_speed = pyqtSignal(int,int)
    track_model_track_fault = pyqtSignal(bool)
    track_model_authority = pyqtSignal(int,float)
    track_model_block_grade = pyqtSignal(int,float)
    track_model_beacon = pyqtSignal(int,str)
    
    # Train Model signals
    trainModel_backend_update = pyqtSignal()
    trainModel_send_actual_velocity = pyqtSignal(int, float)
    trainModel_send_emergency_brake = pyqtSignal(int, bool)
    trainModel_send_suggested_speed = pyqtSignal(int, float)
    trainModel_send_authority = pyqtSignal(int, float)
    trainModel_send_speed_limit = pyqtSignal(int, float)
    trainModel_send_beacon = pyqtSignal(int, str)
    trainModel_send_train_length = pyqtSignal(int, float)
    trainModel_send_distance_from_yard = pyqtSignal(int, float)
    trainModel_send_distance_from_block_start = pyqtSignal(int, float)
    trainModel_send_engine_failure = pyqtSignal(int, bool)
    trainModel_send_brake_failure = pyqtSignal(int, bool)
    trainModel_send_signal_failure = pyqtSignal(int, bool)
    trainModel_update_beacon_UI = pyqtSignal(int, str)
    
    # Train Controller signals
    # train_controller_update_frontend = pyqtSignal(int, int, int, float, bool, bool, bool, bool, bool, bool, bool)#TC backend to TC frontend
    # train_controller_frontend_update = pyqtSignal(bool,bool,bool,float, float, float) #TC frontend to TC backend
    train_controller_update_backend = pyqtSignal() #main backend to TC backend
    # train_controller_backend_update = pyqtSignal()#TC backend to Main backend
    #lights
    train_controller_int_lights_status = pyqtSignal(int, bool)
    train_controller_ext_lights_status = pyqtSignal(int, bool)
    #doors
    train_controller_right_door_status = pyqtSignal(int, bool)
    train_controller_left_door_status = pyqtSignal(int, bool)
    #Bower
    train_controller_send_power_command = pyqtSignal(int, float)
    #Temperature
    train_controller_temperature_value = pyqtSignal(int, float)
    #Braking
    train_controller_emergency_brake_status = pyqtSignal(int, bool)
    train_controller_service_brake_status = pyqtSignal(int, bool)

signals = signalsList()