import unittest
import sys
sys.path.append(".")
from Modules.SW_Wayside.Backend.SW_Wayside_Backend import *
from Main_Backend import *
from Track_Resources.PLC import *

class sw_wayside_tests(unittest.TestCase):
    # ----- PLC load tests -----
    def test_plc_file_uploaded(self):
        # Arrange
        plc = PLC()
        # Act
        plc.update_plc_program("Track_Resources/PLC_Programs/Green Line/ws1.txt", 1, 1)
        # Assert
        self.assertTrue(len(plc.green_line_wayside1_token_list) > 0)

    def test_plc_file_tokenized(self):
        # Arrange
        plc = PLC()
        # Act
        tokenized = plc.tokenizer("Track_Resources/PLC_Programs/Green Line/ws1.txt")
        # Assert
        self.assertTrue(len(tokenized) > 0)
    
    # ----- Signal tests -----
    # signals from ctc
    def test_wayside_receives_authority(self):
        # Arrange
        route = Route()
        route.stops = [1]
        route.stop_time = ['12:00:00']
        route.dwell_time = ['2:00']
        train = Train(route, 1)
        # Assert
        self.assertTrue(train.current_authority == 0)

    def test_wayside_receives_suggested_speed(self):
        # Arrange
        route = Route()
        route.stops = [1]
        route.stop_time = ['12:00:00']
        route.dwell_time = ['2:00']
        train = Train(route, 1)
        # Assert
        self.assertTrue(train.current_suggested_speed == 0)

    def test_wayside_receives_maintenance(self):
        # Arrange
        track = Track()
        # Assert
        self.assertTrue(track.lines[0].blocks[0].maintenance_status == False)
    
    # signals from track model
    def test_wayside_receives_block_occupancy(self):
        # Arrange
        track = Track()
        # Assert
        self.assertTrue(track.lines[0].blocks[0].block_occupancy == False)

    def test_wayside_receives_track_fault(self):
        # Arrange
        track = Track()
        # Assert
        self.assertTrue(track.lines[0].blocks[0].track_fault_status == False)

    # ---- PLC logic tests -----
    def test_wayside_changes_traffic_light(self):
        # Arrange
        plc = PLC()
        track = Track()
        # Act
        track.lines[1].blocks[75].block_occupancy = True
        # Assert
        self.assertTrue(track.lines[1].blocks[76].traffic_light_color == True)
    
    def test_wayside_changes_switch_direction(self):
        # Arrange
        plc = PLC()
        track = Track()
        # Act
        track.lines[1].blocks[75].block_occupancy = True
        # Assert
        self.assertTrue(track.lines[1].blocks[76].switch_direction == True)

    def test_wayside_changes_crossing_active(self):
        # Arrange
        plc = PLC()
        track = Track()
        # Act
        track.lines[1].blocks[20].block_occupancy = True
        # Assert
        self.assertTrue(track.lines[1].blocks[19].crossing_status == True)

    def test_wayside_changes_authority(self):
        # Arrange
        plc = PLC()
        track = Track()
        route = Route()
        route.stops = [1]
        route.stop_time = ['12:00:00']
        route.dwell_time = ['2:00']
        train = Train(route, 1)
        train.current_authority = 10
        # Act
        plc.route_verification()
        # Assert
        self.assertTrue(train.current_authority == 0)

if __name__ == '__main__':
    unittest.main()