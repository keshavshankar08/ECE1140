import unittest
import sys
sys.path.append(".")
from Track_Resources.PLC_Programs import *
from Track_Resources.PLC_Program_Interpreter import *
from signals import signals

class Variables():
    def __init__(self):
        self.track = Track()

    def readTrackObject(self, track):
        self.track = track
        
class testPLCInterpreter(unittest.TestCase):
    def testSingleFile(self):
        filename = "Track_Resources/PLC_Programs/Red Line/PLC_RD_WS1.txt"
        interpreter = Interpreter()
        sig = Variables()
        interpreter.interpretSingleFile(filename)
        signals.swtrack_track.connect(sig.readTrackObject)
        self.assertTrue(self.track.lines[0].lineColor == 0)
        self.assertTrue(self.track.lines[0].blocks[1].crossingActive == 0)
        self.assertTrue(self.track.lines[0].blocks[1].trafficLightColor == 0)
        self.assertTrue(self.track.lines[0].blocks[1].switchDirection == 0)

if __name__ == '__main__':
    unittest.main()