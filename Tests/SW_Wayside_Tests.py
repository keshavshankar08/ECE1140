import unittest
import sys
sys.path.append(".")
from Modules.SW_Wayside.Backend.SW_Wayside_Backend import *
from Main_Backend import *
from Track_Resources.PLC import *

class automatic_mode_tests(unittest.TestCase):
    # ----- PLC load tests -----
    def test_plc_file_uploaded_updates_tokens(self):
        # Arrange
        plc = PLC()
        
        # Act
        plc.update_plc_program("Track_Resources/PLC_Programs/Green Line/ws1.txt", 1, 1)

        # Assert
        self.assertTrue(len(plc.green_line_wayside1_token_list) > 0)

    def test_plc_file_interpreted(self):
        # Arrange
        plc = PLC()
    
    # ----- Signal tests -----
    # signals from ctc
    def test_wayside_receives_authority(self):
        pass

    def test_wayside_receives_suggested_speed(self):
        pass

    def test_wayside_receives_maintenance(self):
        pass
    
    # signals from track model
    def test_wayside_receives_track_occupancy(self):
        pass

    def test_wayside_receives_track_fault(self):
        pass

    # ---- PLC logic tests -----
    def test_wayside_changes_traffic_light(self):
        pass
    
    def test_wayside_changes_switch_direction(self):
        pass

    def test_wayside_changes_crossing_active(self):
        pass

    def test_wayside_changes_authority(self):
        pass

class manual_mode_tests(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()