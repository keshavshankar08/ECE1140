import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *

class WaysideBackend():
    def __init__(self):
        self.track_instance_copy = Track()
        self.active_trains_instance_copy = 1#ActiveTrains()
        self.plc_file_name = ""
        self.plc_line_number = -1
        self.plc_wayside_number = -1

        # receives updates from main backend
        signals.sw_wayside_update_backend.connect(self.backend_update_backend)
        
        # receives updates from plc
        signals.sw_wayside_plc_update.connect(self.plc_update_backend)

        # receives updates from wayside frontend
        signals.sw_wayside_frontend_update.connect(self.frontend_update_backend)

    # Sends updates from wayside backend to wayside frontend
    def send_frontend_update(self):
        signals.sw_wayside_update_frontend.emit(self.track_instance_copy)

    # Sends udpates from wayside backend to wayside PLC
    def send_plc_update(self):
        signals.sw_wayside_update_plc.emit(self.track_instance_copy, self.active_trains_instance_copy, self.plc_file_name, self.plc_line_number, self.plc_wayside_number)
    
    # Sends updates from wayside backend to main backend
    def send_main_backend_update(self):
        signals.sw_wayside_backend_update.emit(self.track_instance_copy)

    # Updates local instance of track
    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    # Updates local instance of active trains
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    # The main function to carry out all necessary functions in a cycle
    def backend_update_backend(self, track_instance):
        # update local instance of track
        self.update_copy_track(track_instance)

        # send updated signals to wayside frontend
        self.send_frontend_update()

        # send updated signals to  plc
        self.send_plc_update()

        # send updated signals to main backend
        self.send_main_backend_update()

    # Apply updates from UI
    def frontend_update_backend(self, track_instance, file_name, line_number, wayside_number):
        # update local instance variables
        self.update_copy_track(track_instance)
        self.plc_file_name = file_name
        self.plc_line_number = line_number
        self.plc_wayside_number = wayside_number

    # Apply updates from PLC
    def plc_update_backend(self, track_instance, train_instance):
        # update local instance of track and train
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(train_instance)

    # Perform tripple redundancy verification on track devices and blocks
    def redundancy_verifcation(self):
        pass