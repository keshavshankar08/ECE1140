import unittest
import sys
sys.path.append(".")
from Modules.Train_Controller.Backend.Train_Controller import *

class Testing(unittest.TestCase):
    def testRightDoors(self):
        train1 = trainController()
        train1.rightDoorsStatus(True)
        train1.tc_update_values()
        self.assertEqual(train1.R_door, True)

    def testLeftDoors(self):
        train1 = trainController()
        train1.leftDoorsStatus(False)
        train1.tc_update_values()
        self.assertEqual(train1.L_door, False)
    
    def testComSpeed(self):
        train1 = trainController()
        train1.update_commanded_speed(20)
        self.assertEqual(train1.commanded_speed, 20)

    def testCurrSpeed(self):
        train1 = trainController()
        train1.update_current_speed(20)
        train1.tc_update_values()
        self.assertEqual(train1.current_speed, 20)

    def testEBrake(self):
        train1 = trainController()
        train1.emergencyBrakeStatus(True)
        train1.tc_update_values()
        self.assertEqual(train1.emergency_brake, True)

    def test_signals(self):
        train1 = trainController()
        train1.engine_fail = True
        train1.emergencyBrakeStatus(train1.engine_fail)
        train1.tc_update_values()
        self.assertEqual(train1.emergency_brake, True)

if __name__ == '__main__':
    unittest.main()
