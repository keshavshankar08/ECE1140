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
    train_controller_power = pyqtSignal(float)
    #Temperature
    train_controller_temperature_value = pyqtSignal(float)
    #Braking
    train_controller_service_brake_value = pyqtSignal(float)
    train_controller_emergency_brake_on = pyqtSignal(bool)
    train_controller_emergency_brake_off = pyqtSignal(bool)


signals = signalsList()


