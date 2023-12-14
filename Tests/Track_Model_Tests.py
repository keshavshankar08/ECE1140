import unittest
import sys
sys.path.append(".")
from Modules.Track_Model.Backend.Track_Model_Backend import *

class TestTrackModel(unittest.TestCase):
    
    def setUp(self):
        self.track_model = TrackModelModule()
        self.line_name = 'Red Line'
        
    def test_failure_modes(self):
        self.clicked_block = 1 
        self.TrackCircuitFailureToggleButton.isChecked = True
        self.assertTrue(self.track_instance_copy.lines[0].blocks[self.clicked_block].track_fault_status)
        
        self.clicked_block = 2
        self.BrokenRailToggleButton.isChecked = True
        self.assertTrue(self.track_instance_copy.lines[0].blocks[self.clicked_block].track_fault_status)
        
        self.clicked_block = 3
        self.PowerFailureToggleButton.isChecked = True
        self.assertTrue(self.track_instance_copy.lines[0].blocks[self.clicked_block].track_fault_status)
    
    def test_track_heater(self):
        self.track_heater(68)
        self.assertEqual(self.track_heater_display.text(),"Inactive")
        
        self.track_heater(32)
        self.assertEqual(self.track_heater_display.text(),"Active")
        
    def test_occupancy(self):
        self.line_name = 'Red Line'
        distance_from_yard = 2100
        
        occupied_block = self.block_occupancy(distance_from_yard)
        
        self.assertEqual(occupied_block,20)
        
        self.line_name = 'Green Line'
        distance_from_yard = 3847
        
        occupied_block = self.block_occupancy(distance_from_yard)
        
        self.assertEqual(occupied_block,25)
        
    def test_authority(self):
        self.line_name = 'Red Line'
        authority_blocks = 12
        
        authority_meters = self.send_train_info(authority_blocks)
        
        self.assertEqual(authority_meters,1175)
        
        self.line_name = 'Green Line'
        authority_blocks = 8
        
        authority_meters = self.send_train_info(authority_blocks)
        
        self.assertEqual(authority_meters,1000)
        
    def test_beacon(self):
        self.line_name = 'Green Line'
        block = 73
        
        beacon_message = self.beacon(block)
        
        self.assertEqual(beacon_message,"Dormont Right 50.0")