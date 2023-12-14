import unittest
from unittest.mock import MagicMock
import sys
sys.path.append(".")
from Modules.Train_Model.Backend.Train import *
from Modules.Train_Model.Backend.TrainList import *

class TestTrain(unittest.TestCase):

    def setUp(self):
        self.train = Train()
        self.train.train_id = 1

    def test_eBrake(self):
        self.train.eBrake(True)
        self.assertTrue(self.train.emergencyBrake)

    def test_sBrake(self):
        self.train.sBrake(True)
        self.assertTrue(self.train.serviceBrake)

    def test_interiorLights(self):
        self.train.interiorLights(True)
        self.assertTrue(self.train.interiorLight)

    def test_exteriorLights(self):
        self.train.exteriorLights(True)
        self.assertTrue(self.train.exteriorLight)

    def test_leftDoors(self):
        self.train.leftDoors(True)
        self.assertTrue(self.train.leftDoor)

    def test_rightDoors(self):
        self.train.rightDoors(True)
        self.assertTrue(self.train.rightDoor)

    def test_receiveTemperature(self):
        self.train.receiveTemperature(65.0)
        self.assertEqual(self.train.temperatureCommand, 65.0)

    def test_setPowerCommand(self):
        self.train.setPowerCommand(50000)
        self.assertEqual(self.train.commandedPower, 50000)

    def test_receiveBeacon(self):
        self.train.receiveBeacon("Beacon123")
        self.assertEqual(self.train.currentBeacon, "Beacon123")

    def test_receiveSpeedLimit(self):
        self.train.receiveSpeedLimit(60.0)
        self.assertEqual(self.train.speedLimit, 60.0)

    def test_receiveAuthority(self):
        self.train.receiveAuthority(100.0)
        self.assertEqual(self.train.currentAuthority, 100.0)

    def test_receiveSuggestedSpeed(self):
        self.train.receiveSuggestedSpeed(15.0)
        self.assertEqual(self.train.suggestedSpeed, 15.0)

    def test_receivePassengers(self):
        self.train.receivePassengers(10)
        self.assertEqual(self.train.numPassengers, 10)
        self.assertEqual(self.train.mass, CAR_WEIGHT_EMPTY + 10 * 70)

    def test_receiveGradient(self):
        self.train.receiveGradient(5.0)
        self.assertEqual(self.train.currentGradient, 5.0)

    def test_receiveTunnel(self):
        self.train.receiveTunnel(True)
        self.assertTrue(self.train.tunnel)


class TestTrainList(unittest.TestCase):

    def setUp(self):
        self.trainList = TrainList()

    def test_addTrain(self):
        self.trainList.addTrain(1)
        self.assertIn(1, self.trainList.allTrains)

    def test_removeTrain(self):
        self.trainList.addTrain(1)
        self.trainList.removeTrain(1)
        self.assertNotIn(1, self.trainList.allTrains)

    def test_updateAllTrains(self):
        self.trainList.addTrain(1)
        self.trainList.updateAllTrains()
        self.assertIsInstance(self.trainList.allTrains[1], Train)


if __name__ == '__main__':
    unittest.main()
