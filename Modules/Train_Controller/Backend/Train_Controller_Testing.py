import unittest
import sys
sys.path.append(".")
from Modules.Train_Controller.Backend.Train_Controller import *
from Modules.Train_Controller.Backend.Train_Controller_List import *

class Testing(unittest.TestCase):
    def setUp(self):
        self.train_controller = TrainController()
        self.train_controller.train_id = 1

    def test_ebrake(self):
        self.train_controller.emergency_brake_status(True)
        self.assertTrue(self.train_controller.emergency_brake)

    def test_sbrake(self):
        self.train_controller.service_brake_status(True)
        self.assertTrue(self.train_controller.service_brake)

    def test_int_lights(self):
        self.train_controller.interior_lights_status(True)
        self.assertTrue(self.train_controller.int_lights)

    def test_ext_lights(self):
        self.train_controller.exterior_lights_status(True)
        self.assertTrue(self.train_controller.ext_lights)

    def test_ldoors(self):
        self.train_controller.left_doors_status(True)
        self.assertTrue(self.train_controller.L_door)

    def test_rdoors(self):
        self.train_controller.right_doors_status(True)
        self.assertTrue(self.train_controller.R_door)

    def test_current_speed(self):
        self.train_controller.update_current_speed(25)
        self.assertEqual(self.train_controller.current_speed, 25)

    def test_beacon(self):
        self.train_controller.beacon_receive("DORMONT LEFT 100 0")
        self.assertEqual(self.train_controller.station, "DORMONT")

    def test_suggested_speed(self):
        self.train_controller.update_suggested_speed(30)
        self.assertEqual(self.train_controller.suggested_speed, 30)

    def test_authority(self):
        self.train_controller.update_authority(100.0)
        self.assertEqual(self.train_controller.authority, 100.0)

class TestTrainControllerList(unittest.TestCase):

    def setUp(self):
        self.train_controller = TrainControllerList()

    def test_addTrain(self):
        self.train_controller.add_train(1)
        self.assertIn(1, self.train_controller.total_trains)

    def test_removeTrain(self):
        self.train_controller.add_train(1)
        self.train_controller.remove_train(1)
        self.assertNotIn(1, self.train_controller.total_trains)

    def test_updateAllTrains(self):
        self.train_controller.add_train(1)
        self.train_controller.update_all_trains()
        self.assertIsInstance(self.train_controller.total_trains[1], TrainController)


if __name__ == '__main__':
    unittest.main()
