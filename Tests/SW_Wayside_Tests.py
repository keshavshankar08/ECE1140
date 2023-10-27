import unittest
import sys
sys.path.append(".")
from Track_Resources.PLC_Program_Interpreter import *
from signals import signals
from Main_Backend import *
        
class testPLCInterpreter(unittest.TestCase):
    def testSingleFile(self):
        filename = "Track_Resources/PLC_Programs/Red Line/PLC_RD_WS1.txt"
        interpreter = Interpreter()
        trkUpdated = interpreter.interpretSingleFile(filename)
        self.assertTrue(mainInstance.trackInstance == trkUpdated)

if __name__ == '__main__':
    unittest.main()