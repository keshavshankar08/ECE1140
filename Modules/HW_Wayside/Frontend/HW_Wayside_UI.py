import sys
sys.path.append(".")
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
from signals import *

class HWWaysideFrontend(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("Modules/HW_Wayside/Frontend/HW_Wayside_UI.ui", self)
                # set title
                self.setWindowTitle("HW Wayside")

                self.track_instance_copy = Track()
                # receives updates from wayside backend
                signals.sw_wayside_update_frontend.connect(self.update_frontend)

                # handles override signals for manual inputs
                self.switch_direction_transmit.clicked.connect(self.manual_switch_toggled)
                self.traffic_light_color_transmit.clicked.connect(self.manual_light_toggled)
                self.crossing_status_transmit.clicked.connect(self.manual_crossing_toggled)

                # handles plc button clicked
                self.upload_plc_program_button.clicked.connect(self.uploadPLCClicked)

                # handles track map button clicked
                self.track_map_view_button.clicked.connect(self.view_track_map_clicked)

                self.last_line_state = ""
                self.last_wayside_state = ""
                self.last_block_state = ""
                self.last_switch_state = ""
                self.last_light_state = ""
                self.last_crossing_state = ""
        
        # Handles all frontend updates
        def update_frontend(self, track_instance):
                # update local instance of track
                self.update_copy_track(track_instance)

                # update the ui information
                self.update_display()

                # send updated signals to wayside backend
                self.send_backend_update()

        # Sends updates from wayside frontend to wayside backend
        def send_backend_update(self):
                signals.sw_wayside_frontend_update.emit(self.track_instance_copy)

        # Updates all UI display information
        def update_display(self):
                self.update_opeartion_dropdown()
                self.update_line_dropdown()
                self.update_wayside_dropdown()
                self.update_block_dropdown()

        # Updates local instance of track
        def update_copy_track(self, updated_track):
                self.trackInstanceCopy = updated_track
        
        # Updates elements shown once mode chosen
        def update_opeartion_dropdown(self):
                if(self.mode_selection_dropdown.currentText() == "Select Mode..."):
                        self.line_selection_dropdown.setEnabled(False)
                        self.line_box.setEnabled(False)
                        self.switch_direction_dropdown.setEnabled(False)
                        self.traffic_light_color_dropdown.setEnabled(False)
                        self.crossing_status_dropdown.setEnabled(False)
                        self.switch_direction_transmit.setEnabled(False)
                        self.traffic_light_color_transmit.setEnabled(False)
                        self.crossing_status_transmit.setEnabled(False)
                elif(self.mode_selection_dropdown.currentText() == "Manual"):
                        self.line_selection_dropdown.setEnabled(True)
                        self.line_box.setEnabled(True)
                        self.switch_direction_dropdown.setEnabled(True)
                        self.traffic_light_color_dropdown.setEnabled(True)
                        self.crossing_status_dropdown.setEnabled(True)
                        self.switch_direction_transmit.setEnabled(True)
                        self.traffic_light_color_transmit.setEnabled(True)
                        self.crossing_status_transmit.setEnabled(True)
                elif(self.mode_selection_dropdown.currentText() == "Automatic"):
                        self.line_selection_dropdown.setEnabled(True)
                        self.line_box.setEnabled(True)
                        self.switch_direction_dropdown.setEnabled(False)
                        self.traffic_light_color_dropdown.setEnabled(False)
                        self.crossing_status_dropdown.setEnabled(False)
                        self.switch_direction_transmit.setEnabled(False)
                        self.traffic_light_color_transmit.setEnabled(False)
                        self.crossing_status_transmit.setEnabled(False)

        # Updates elements shown once line chosen
        def update_line_dropdown(self):
                if(self.line_selection_dropdown.currentText() == "Select Line..."):
                        self.track_map_view_button.setEnabled(False)
                        self.wayside_box.setEnabled(False)
                elif(self.line_selection_dropdown.currentText() == "Green Line"):
                        self.track_map_view_button.setEnabled(True)
                        self.wayside_box.setEnabled(True)
                elif(self.line_selection_dropdown.currentText() == "Red Line"):
                        self.track_map_view_button.setEnabled(True)
                        self.wayside_box.setEnabled(True)

        # Updates elements shown once wayside chosen
        def update_wayside_dropdown(self):
                if(self.wayside_selection_dropdown.currentText() == "Select Wayside..."):
                        self.upload_plc_program_button.setEnabled(False)
                        self.block_box.setEnabled(False)
                elif((self.wayside_selection_dropdown.currentText() == "Wayside 1") and (self.last_wayside_state != "Wayside 1" or self.last_line_state != self.line_selection_dropdown.currentText())):
                        self.last_wayside_state = "Wayside 1"
                        self.last_line_state = self.line_selection_dropdown.currentText()
                        self.upload_plc_program_button.setEnabled(True)
                        self.block_box.setEnabled(True)
                        self.block_selection_dropdown.clear()
                        self.block_selection_dropdown.addItem("Select Block...")
                        if(self.line_selection_dropdown.currentText() == "Green Line"):
                                for i in range(69):
                                        self.block_selection_dropdown.addItem("Block " + str(i))
                        elif(self.line_selection_dropdown.currentText() == "Red Line"):
                                for i in range(24):
                                        self.block_selection_dropdown.addItem("Block " + str(i))
                elif((self.wayside_selection_dropdown.currentText() == "Wayside 2") and (not(self.last_wayside_state == "Wayside 2") or not(self.last_line_state == self.line_selection_dropdown.currentText()))):
                        self.last_wayside_state = "Wayside 2"
                        self.last_line_state = self.line_selection_dropdown.currentText()
                        self.upload_plc_program_button.setEnabled(True)
                        self.block_box.setEnabled(True)
                        self.block_selection_dropdown.clear()
                        self.block_selection_dropdown.addItem("Select Block...")
                        if(self.line_selection_dropdown.currentText() == "Green Line"):
                                for i in range(69, 151):
                                        self.block_selection_dropdown.addItem("Block " + str(i))
                        elif(self.line_selection_dropdown.currentText() == "Red Line"):
                                for i in range(24, 77):
                                        self.block_selection_dropdown.addItem("Block " + str(i))

        # Updates elements shown once block chosen
        def update_block_dropdown(self):
                if(self.block_selection_dropdown.currentText() == "Select Block..."):
                        self.general_box.setEnabled(False)
                        self.maintenance_box.setEnabled(False)
                        self.junction_box.setEnabled(False)
                        self.station_box.setEnabled(False)
                        self.crossing_box.setEnabled(False)
                else:
                        self.general_box.setEnabled(True)
                        self.maintenance_box.setEnabled(True)
                        curr_line_int = self.get_current_line_displayed_int()
                        curr_block_int = self.get_current_block_displayed_int()
                        if(self.last_block_state != self.block_selection_dropdown.currentText()):
                                self.last_block_state = self.block_selection_dropdown.currentText()
                                if(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_block_type_string() == "Junction"):
                                        self.junction_box.setEnabled(True)
                                        self.station_box.setEnabled(False)
                                        self.crossing_box.setEnabled(False)
                                        self.switch_direction_dropdown.clear()
                                        self.switch_direction_dropdown.addItems(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_switch_direction_string_list(curr_line_int))
                                        self.traffic_light_color_dropdown.clear()
                                        if(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].traffic_light_color == False):
                                                self.traffic_light_color_dropdown.addItems(["Red", "Green"])
                                        else:
                                                self.traffic_light_color_dropdown.addItems(["Green", "Red"])
                                elif(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_block_type_string() == "Station"):
                                        self.junction_box.setEnabled(False)
                                        self.station_box.setEnabled(True)
                                        self.crossing_box.setEnabled(False)
                                elif(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_block_type_string() == "Crossing"):
                                        self.junction_box.setEnabled(False)
                                        self.station_box.setEnabled(False)
                                        self.crossing_box.setEnabled(True)
                                        self.crossing_status_dropdown.clear()
                                        if(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].crossing_status == False):
                                                self.crossing_status_dropdown.addItems(["Inactive","Active"])
                                        else:
                                                self.crossing_status_dropdown.addItems(["Active","Inactive"])
                                else:
                                        self.junction_box.setEnabled(False)
                                        self.station_box.setEnabled(False)
                                        self.crossing_box.setEnabled(False)
                        self.update_block_information()

        # Gets the integer representation of the current line chosen
        def get_current_line_displayed_int(self):
                curr_line = self.line_selection_dropdown.currentText()
                if(curr_line == "Green Line"):
                        return 1
                elif(curr_line == "Red Line"):
                        return 0
                
        # Gets the integer representation of the current block chosen
        def get_current_block_displayed_int(self):
                curr_block = self.block_selection_dropdown.currentText()
                return int(curr_block[6:])
                        
        # Updates display block information
        def update_block_information(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.block_type_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_block_type_string())
                self.block_occupancy_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_block_occupancy_string())
                self.track_fault_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_track_fault_status_string())
                self.maintenance_active_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_maintenance_status_string())
                self.switch_direction_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_switch_direction_string(curr_line_int))
                self.traffic_light_color_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_traffic_light_color_string())
                self.station_name_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].station_name)
                self.crossing_status_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_crossing_status_string())

        # Handles view track map button clicked
        def view_track_map_clicked(self):
                # figure out alternative to opencv to open up the map pictures
                # need to make a good map with devices to show
                pass

        # Handles upload plc program button clicked
        def uploadPLCClicked(self):
                fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
                # this will get fed into the interpreter
                # the interpreter will spit back a wayside logic object
                # this gets added to a copy of the wayside controller object, which contains the logic and info from the track for each wayside
                # most importantly, it has a wayside logic object for each controller
        
        # Handles switch toggle in manual mode
        def manual_switch_toggled(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                new_direction = self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_switch_direction_bool(self.switch_direction_dropdown.currentText(), curr_line_int)
                positions = self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_all_junction_block_indexes(curr_line_int, curr_block_int, self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_switch_direction_bool(self.switch_direction_dropdown.currentText(), curr_line_int))
                self.track_instance_copy.lines[curr_line_int].blocks[positions[0]].switch_direction = new_direction
                self.track_instance_copy.lines[curr_line_int].blocks[positions[1]].switch_direction = new_direction
                self.track_instance_copy.lines[curr_line_int].blocks[positions[2]].switch_direction = new_direction

        # Handles light toggle in manual mode
        def manual_light_toggled(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].traffic_light_color = self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_traffic_light_color_bool(self.traffic_light_color_dropdown.currentText())

        # Handles crossing toggle in manual mode
        def manual_crossing_toggled(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].crossing_status = self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_crossing_status_bool(self.crossing_status_dropdown.currentText())