import unittest
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.Train import Train

class TrainModelTests(unittest.TestCase):
    def testTrackPolarity(self):
        train1 = Train()
        train1.distanceFromBlockStart = 100
        train1.receivePolarity(1)
        train1.TrainModelUpdateValues()
        self.assertEqual(train1.distanceFromBlockStart, 100)
        train1.TrainModelUpdateValues()
        train1.receivePolarity(-1)
        self.assertEqual(train1.distanceFromBlockStart, 0)
        
    def testGradient(self):
        train1 = Train()
        self.assertEqual(train1.slopeForce, 0)
        train1.receiveGradient(1.00)
        train1.TrainModelUpdateValues()
        self.assertEqual(train1.slopeForce, 3635.996484720533)
        
    def testPassengers(self):
        train1 = Train()
        self.assertEqual(train1.numPassengers, 0)
        train1.receivePassengers(10)
        train1.TrainModelUpdateValues()
        self.assertEqual(train1.numPassengers, 10)
        self.assertEqual(train1.mass, 37103.86 + 700)
        
    def testEmergencyBrake(self):
        train1 = Train()
        self.assertEqual(train1.emergencyBrake, False)
        train1.engineForce = 30000
        self.assertNotEqual(train1.engineForce, 0)
        train1.onEmergencyBrake(True)
        train1.TrainModelUpdateValues()
        self.assertEqual(train1.commandedPower, 0)
        self.assertEqual(train1.emergencyBrake, True)
        
    def testMurphyBrakeFailure(self):
        train1 = Train()
        train1.brakeFail = True
        train1.serviceBrakeReceive(True)
        train1.TrainModelUpdateValues()
        self.assertEqual(train1.serviceBrake, False)
        
        

if __name__ == '__main__':
    unittest.main()