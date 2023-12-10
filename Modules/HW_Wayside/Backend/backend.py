import sys
import serial
import time
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class HWWaysideBackend():
    def __init__(self):
        self.trackInstanceCopy = Track()
        self.active_trains_instance_copy = ActiveTrains()
        self.plc_file_name = ""
        self.plc_line_number = -1
        self.plc_wayside_number = -1
        self.operation_mode = ""

        # receives updates from main backend
        signals.hw_wayside_update_backend.connect(self.backend_update_backend)
        
        # receives updates from wayside frontend
        signals.hw_wayside_frontend_update.connect(self.frontend_update_backend)

    # Sends updates from wayside backend to wayside frontend
    def send_frontend_update(self):
        signals.hw_wayside_update_frontend.emit(self.trackInstanceCopy)

    # Sends updates from wayside backend to main backend
    def send_main_backend_update(self):
        signals.hw_wayside_backend_update.emit(self.trackInstanceCopy)

    # Updates local instance of track
    def update_copy_track(self, updated_track):
        self.trackInstanceCopy = updated_track

    # The main function to carry out all necessary functions in a cycle
    def backend_update_backend(self, track_instance):
        # update local instance of track
        self.update_copy_track(track_instance)

        # send updated signals to wayside frontend
        self.send_frontend_update()

        # all the backend logic function calls

        # send updated signals to main backend
        self.send_main_backend_update()

    # Apply updates from UI
    def frontend_update_backend(self, track_instance):
        # update local instance of track
        self.update_copy_track(track_instance)
