import sys
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *

class WaysideSystem():
    def __init__(self):
        self.trackSystem = Track()

    def updateTrack(self, track):
        self.trackSystem = track

if __name__ == "__main__":
    waysideSystem = WaysideSystem()
    signals.swtrack_update_track.connect(waysideSystem.updateTrack)
    signals.swtrack_track.emit(waysideSystem.trackSystem)
