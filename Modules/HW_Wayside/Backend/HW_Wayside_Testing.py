import unittest
import sys
sys.path.append(".")

from Modules.HW_Wayside.Backend.Arduino_PLC import *

class Testing_HW_Wayside(unittest.TestCase):
    # test arduino connection
    def ard_connect(self):
        # ensure that connection exists (!= 0)
        SER = serial.Serial('COM3', 9600)
        self.assertNotEqual(SER, 0)
    
    # test tokenizer of PLC
    def test_plc_file_tokenized(self):
        # Arrange
        plc = Arduino_PLC()
        # Act
        tokenized = plc.tokenizer("Track_Resources/PLC_Programs/Green Line/ws1.txt")
        # Assert
        self.assertTrue(len(tokenized) > 0)
    
    # test receivnig signals from ctc
    def test_wayside_receives_authority(self):
        # Arrange
        route = Route()
        route.stops = [1]
        route.stop_time = ['12:00:00']
        route.dwell_time = ['2:00']
        train = Train(route, 1)
        # Assert
        self.assertTrue(train.current_authority == 0)

    # test receiving speed
    def test_wayside_receives_suggested_speed(self):
        # Arrange
        route = Route()
        route.stops = [1]
        route.stop_time = ['12:00:00']
        route.dwell_time = ['2:00']
        train = Train(route, 1)
        # Assert
        self.assertTrue(train.current_suggested_speed == 0)

    # test receiving track maintenance
    def test_wayside_receives_maintenance(self):
        # Arrange
        track = Track()
        # Assert
        self.assertTrue(track.lines[0].blocks[0].maintenance_status == False)
        
    # test receiving track maintenance
    def test_wayside_receives_maintenance_station(self):
        # Arrange
        track = Track()
        # Assert
        self.assertTrue(track.lines[0].blocks[7].maintenance_status == False)

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

    # test PLC
    def test_wayside_changes_traffic_light(self):
        # Arrange
        plc = Arduino_PLC()
        track = Track()
        # Act
        track.lines[1].blocks[75].block_occupancy = True
        # Assert
        self.assertTrue(track.lines[1].blocks[76].traffic_light_color == False)
    
    def test_wayside_changes_switch_direction(self):
        # Arrange
        plc = Arduino_PLC()
        track = Track()
        # Act
        track.lines[1].blocks[75].block_occupancy = True
        # Assert
        self.assertTrue(track.lines[1].blocks[76].switch_direction == False)

    def test_wayside_changes_crossing_active(self):
        # Arrange
        plc = Arduino_PLC()
        track = Track()
        # Act
        track.lines[1].blocks[20].block_occupancy = True
        # Assert
        self.assertTrue(track.lines[1].blocks[19].crossing_status == False)

    # test authority changer
    def test_wayside_changes_authority(self):
        # Arrange
        plc = Arduino_PLC()
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
        self.assertTrue(train.current_authority != 0)

        
if __name__ == '__main__':
    unittest.main()
