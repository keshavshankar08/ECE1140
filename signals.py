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

    # SW Wayside Signals
    sw_wayside_update_backend = pyqtSignal(Track, ActiveTrains) # update from main backend to sw wayside backend
    sw_wayside_update_plc = pyqtSignal(Track, ActiveTrains, str, int, int) # update from sw wayside backend to plc
    sw_wayside_update_frontend = pyqtSignal(Track) # update from sw wayside backend to sw wayside frontend
    
    sw_wayside_frontend_update = pyqtSignal(Track, str, int, int, str) # update from sw wayside frontend to sw wayside backend
    sw_wayside_plc_update = pyqtSignal(Track, ActiveTrains) # update from plc to sw wayside backend
    sw_wayside_backend_update = pyqtSignal(Track, ActiveTrains) # update from sw wayside backend to main backend


    # HW Wayside signals
    hw_wayside_update_backend = pyqtSignal(Track)
    hw_wayside_update_frontend = pyqtSignal(Track)
    hw_wayside_frontend_update = pyqtSignal(Track)
    hw_wayside_backend_update = pyqtSignal(Track)
    
    # Track Model signals receive and send to CTC / Wayside
    track_model_update_backend = pyqtSignal(Track,ActiveTrains)
    track_model_backend_update = pyqtSignal(Track)
    track_model_ticket_sales = pyqtSignal(int)
    track_model_track_fault = pyqtSignal(bool)
    
    # Track Model signals send to train model
    track_model_passengers = pyqtSignal(int,int)
    track_model_speed_limit = pyqtSignal(int,int)
    track_model_suggested_speed = pyqtSignal(int,int)
    track_model_authority = pyqtSignal(int,float)
    track_model_block_grade = pyqtSignal(int,float)
    track_model_beacon = pyqtSignal(int,str)
    
    # Train Model signals
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
    trainModel_update_beacon_UI = pyqtSignal(str)
    
    # Train Controller signals
    # train_controller_update_frontend = pyqtSignal(int, int, int, float, bool, bool, bool, bool, bool, bool, bool)#TC backend to TC frontend
    # train_controller_frontend_update = pyqtSignal(bool,bool,bool,float, float, float) #TC frontend to TC backend
    train_controller_update_backend = pyqtSignal() #main backend to TC backend
    # train_controller_backend_update = pyqtSignal()#TC backend to Main backend
    #lights
    train_controller_int_lights_status = pyqtSignal(bool)
    train_controller_ext_lights_status = pyqtSignal(bool)
    #doors
    train_controller_right_door_status = pyqtSignal(bool)
    train_controller_left_door_status = pyqtSignal(bool)
    #Bower
    train_controller_send_power_command = pyqtSignal(float)
    #Temperature
    train_controller_temperature_value = pyqtSignal(float)
    #Braking
    train_controller_emergency_brake_status = pyqtSignal(bool)
    train_controller_service_brake_status = pyqtSignal(bool)

signals = signalsList()


