import sys
import serial
import time
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *

class WaysideBackend():
    def __init__(self):
        self.trackInstanceCopy = Track()

        # receives updates from main backend
        signals.sw_wayside_update_backend.connect(self.backend_update_backend)
        
        # receives updates from wayside frontend
        signals.sw_wayside_frontend_update.connect(self.frontend_update_backend)

    # Sends updates from wayside backend to wayside frontend
    def send_frontend_update(self):
        signals.sw_wayside_update_frontend.emit(self.trackInstanceCopy)

    # Sends updates from wayside backend to main backend
    def send_main_backend_update(self):
        signals.sw_wayside_backend_update.emit(self.trackInstanceCopy)

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

    # send PLC program serially
    def send_PLC(data):
        SER = serial.Serial('COM3', 9600)
        SER.write(data.encode('ascii'))
        time.sleep(1)
        response = SER.readline().decode('ascii').strip()
        print("Arduino output: \n", response)