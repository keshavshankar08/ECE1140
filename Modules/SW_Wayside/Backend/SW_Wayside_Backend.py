import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class WaysideBackend():
    def __init__(self):
        self.track_instance_copy = Track()
        self.active_trains_instance_copy = ActiveTrains()
        self.plc_file_name = ""
        self.plc_line_number = -1
        self.plc_wayside_number = -1
        self.operation_mode = ""

        # receive update from main backend
        signals.sw_wayside_update_backend.connect(self.backend_update_backend)
        
        # receive update from plc
        signals.sw_wayside_plc_update.connect(self.plc_update_backend)

        # receive update from wayside frontend
        signals.sw_wayside_frontend_update.connect(self.frontend_update_backend)

    # Sends updates from wayside backend to wayside frontend
    def send_frontend_update(self):
        signals.sw_wayside_update_frontend.emit(self.track_instance_copy)

    # Sends udpate from wayside backend to wayside PLC
    def send_plc_update(self):
        signals.sw_wayside_update_plc.emit(self.track_instance_copy, self.active_trains_instance_copy, self.plc_file_name, self.plc_line_number, self.plc_wayside_number)
    
    # Sends updates from wayside backend to main backend
    def send_main_backend_update(self):
        signals.sw_wayside_backend_update.emit(self.track_instance_copy, self.active_trains_instance_copy)

    # Updates track instance
    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    # Updates active trains instance
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    # Main backend handler 
    def backend_update_backend(self, track_instance, active_trains):
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(active_trains)
        self.track_instance_copy.lines[1].blocks[0].block_occupancy = True
        self.send_frontend_update()
        if(self.operation_mode == "Automatic"):
            self.send_plc_update()
        self.send_main_backend_update()

    # Handler for update from SW Wayside Frontend
    def frontend_update_backend(self, track_instance, file_name, line_number, wayside_number, operation_mode):
        # update local instance variables
        self.update_copy_track(track_instance)
        self.plc_file_name = file_name
        self.plc_line_number = line_number
        self.plc_wayside_number = wayside_number
        self.operation_mode = operation_mode

    # Handler for update from PLC
    def plc_update_backend(self, track_instance, train_instance):
        # update local instance of track and train
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(train_instance)

    # Perform tripple redundancy verification on track devices and blocks
    def redundancy_verifcation(self):
        pass