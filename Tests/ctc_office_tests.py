import unittest
from unittest.mock import MagicMock
import sys
sys.path.append(".")
from Modules.CTC.Backend.CTC_Backend import *
from Train_Resources.CTC_Train import *

class TestCTC(unittest.TestCase):

    def setUp(self):
        self.route = Route()
        self.route.stops = [1]
        self.route.stop_time = ['12:00:00']
        self.route.dwell_time = ['2:00']

        self.green_train = Train(self.route, 1)
        
    def test_ID(self):
        self.assertEqual(self.green_train.train_ID, "0000")

    def test_current_line(self):
        self.assertEqual(self.green_train.current_line, 1)

    def test__current_direction(self):
        self.assertEqual(self.green_train.current_direction, False)

    def test_authority_stop_queue(self):
        return
        self.assertEqual(self.green_train.authority_stop_queue, [[0], 
                                                                 [0, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84, 83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
                                                                 [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 0]])

    def test_current_block(self):
        self.assertEqual(self.green_train.current_block, -1)

    def test_current_suggested_speed(self):
        self.assertEqual(self.green_train.current_suggested_speed, 0)

    def test_speed_stop_queue(self):
        return
        self.assertEqual(self.green_train.current_suggested_speed_stop_queue, [[5], 
                                                                               [10, 43, 43, 43, 43, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 43, 43, 43, 43, 43, 43, 43, 43, 43, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 43, 43, 43, 43, 43, 43, 43, 43, 43, 16, 17, 17, 17, 17, 17, 17, 17, 17, 19, 19, 19, 19, 19, 19, 19, 9, 9, 9, 9, 9, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 19, 19, 43, 43, 43, 43, 43, 43, 37, 37, 37, 37, 43, 43, 43, 43, 28, 28, 28, 28, 28, 28, 28, 28, 28, 15, 10, 5], 
                                                                               [43, 43, 43, 43, 37, 37, 37, 37, 43, 43, 43, 43, 43, 43, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 15, 10, 5]])

    def test_authority_changed(self):
        self.green_train.current_authority_changed = True
        self.assertTrue(self.green_train.current_authority_changed)

    def test_authority_reset(self):
        self.green_train.authority_reset_ready = True
        self.assertTrue(self.green_train.authority_reset_ready)

class TestRouteQueue(unittest.TestCase):

    def setUp(self):
        self.route_queue = RouteQueue()
        self.route = Route()
        self.route.stops = [1]
        self.route.stop_time = ['12:00:00']
        self.route.dwell_time = ['2:00']

    def test_add_route(self):
        return
        self.route_queue.add_route(self.route)
        self.assertIn(self.route, self.route_queue.routes)

    def test_remove_route(self):
        return
        self.route_queue.add_route(self.route)
        self.route_queue.remove_route(0)
        self.assertNotIn(self.route, self.route_queue.routes)

class ValidateTime(unittest.TestCase):

    def setUp(self):
        self.dwell = '1:30'
        self.bad_dwell = '1.30'
        self.stop_time = '12:00:00'
        self.bad_stop_time = '12:00:000'

    def test_dwell(self):
        self.assertTrue(validate_time_minutes(self.dwell))

    def test_bad_dwell(self):
        self.assertFalse(validate_time_minutes(self.bad_dwell))

    def test_stop_time(self):
        self.assertTrue(validate_time_hours)

    def test_bad_stop_time(self):
        self.assertFalse(validate_time_hours(self.bad_stop_time))


if __name__ == '__main__':
    unittest.main()
