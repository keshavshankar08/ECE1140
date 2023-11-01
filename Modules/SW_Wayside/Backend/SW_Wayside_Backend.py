import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *

class WaysideSystem():
    def __init__(self):
        signals.sw_wayside_backend_update.connect(self.UpdateWayside)
        self.trackInstanceCopy = Track()

    def UpdateUI(self):
        signals.sw_wayside_frontend_update.emit(self.trackInstanceCopy)

    def update_copy_track(self, updatedTrack):
        self.trackInstanceCopy = updatedTrack

    # The main function to carry out all necessary functions in a cycle
    def UpdateWayside(self, trackInstance):
        self.trackInstanceCopy = trackInstance
        self.UpdateUI()

        # Updates main instance at end of cycle
        signals.sw_wayside_track_update.emit(self.trackInstanceCopy)

    # all the damn functions to change switches and lights

    