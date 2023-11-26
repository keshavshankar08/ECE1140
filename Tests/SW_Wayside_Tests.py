import unittest
import sys
sys.path.append(".")
from Modules.SW_Wayside.Backend.SW_Wayside_Backend import *
from Main_Backend import *
from Track_Resources.PLC import *

class test_plc_file_uploaded_updates_tokens(unittest.TestCase):
    def test_junction_light_manual_toggle_updates_device(self):
        # Arrange
        plc = PLC()
        
        # Act
        plc.update_plc_program("Track_Resources/PLC_Programs/Green Line/ws1.txt", 1, 1)

        # Assert
        self.assertTrue(len(plc.green_line_wayside1_token_list) > 0)

if __name__ == '__main__':
    unittest.main()