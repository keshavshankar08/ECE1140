from PyQt6.QtCore import QObject, QDateTime
import sys
sys.path.append(".")
from signals import signals
from CONSTANTS import constants
from Modules.Train_Controller.Backend.Train_Controller import TrainController


class TrainControllerList(QObject):
    def __init__(self):
        super().__init__()
        self.total_trains = {} # id, Train

        signals.train_controller_update_backend.connect(self.update_all_trains)
        signals.ctc_added_train.connect(self.add_train)
        #Signals
        signals.trainModel_send_actual_velocity.connect(self.update_current_speed)
        signals.trainModel_send_authority.connect(self.update_authority)
        signals.trainModel_send_beacon.connect(self.beacon_receive)
        signals.trainModel_send_emergency_brake.connect(self.passenger_EBrake)
        signals.trainModel_send_speed_limit.connect(self.update_suggested_speed)
        signals.trainModel_send_suggested_speed.connect(self.update_suggested_speed)
        signals.trainModel_send_engine_failure.connect(self.engine_failure)
        signals.trainModel_send_brake_failure.connect(self.brake_failure)
        signals.trainModel_send_signal_failure.connect(self.signal_failure)
        signals.trainModel_send_tunnel.connect(self.exterior_lights_status)
        signals.trainModel_send_tunnel.connect(self.interior_lights_status)

    def add_train(self, id):
        if id in self.total_trains:
            raise ValueError(f"Train with ID {id} already exists in the train list.")
        train_controller = TrainController()
        train_controller.train_id = int(id)
        self.total_trains[id] = train_controller
        
    def remove_train(self, id):
        if id in self.total_trains:
            self.total_trains.pop(id)
        else:
            raise KeyError(f"{id} not found in train list.")
        
    def update_all_trains(self):
        for id in self.total_trains:
            self.total_trains[id].tc_update_values()


    #functions for train ID

    def update_current_speed(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].update_current_speed(value)

    def update_authority(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].update_authority(value)

    def beacon_receive(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].beacon_receive(value)

    def passenger_EBrake(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].passenger_EBrake(value)

    def update_suggested_speed(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].update_suggested_speed(value)

    def engine_failure(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].engine_failure(value)

    def brake_failure(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].brake_failure(value)

    def signal_failure(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].signal_failure(value)

    def update_suggested_speed(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].update_suggested_speed(value)

    def update_temp_value(self, id, value):
        self.total_trains[id].update_temp_value(value)

    def exterior_lights_status(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].exterior_lights_status(value)

    def interior_lights_status(self, id, value):
        if isinstance(self.total_trains[id], TrainController):
            self.total_trains[id].interior_lights_status(value)


train_controller_list = TrainControllerList()