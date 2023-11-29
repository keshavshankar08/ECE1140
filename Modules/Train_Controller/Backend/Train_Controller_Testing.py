import unittest
import sys
sys.path.append(".")
from Modules.Train_Controller.Backend.Train_Controller import *

class Testing(unittest.TestCase):
    def testRightDoors(self):
        train1 = trainController()
        train1.closeRightDoors()
        self.assertEqual(train1.Rdoor, True)

    def testLeftDoors(self):
        train1 = trainController()
        train1.openLeftDoors()
        self.assertEqual(train1.Ldoor, False)
    
    def testComSpeed(self):
        train1 = trainController()
        train1.updateCommandedSpeed(20)
        self.assertEqual(train1.commandedSpeed, 20)

    def testCurrSpeed(self):
        train1 = trainController()
        train1.updateCurrentSpeed(20)
        self.assertEqual(train1.currentSpeed, 20)

    def testEBrake(self):
        train1 = trainController()
        train1.emergencyBrakeOn()
        self.assertEqual(train1.emergencyBrake, True)

if __name__ == '__main__':
    unittest.main()
