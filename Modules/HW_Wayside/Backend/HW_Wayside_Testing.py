import unittest
import sys
sys.path.append(".")

from Modules.HW_Wayside.Backend.Arduino_PLC import *

class Testing_HW_Wayside(unittest.TestCase):
    def ard_connect(self):
        # ensure that connection exists (!= 0)
        SER = serial.Serial('COM3', 9600)
        self.assertNotEqual(SER, 0)
    
    def signal_test(self):
        # create 
        pass
        
if __name__ == '__main__':
    unittest.main()
