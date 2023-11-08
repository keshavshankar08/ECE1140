from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import cv2
sys.path.append(".")
import Track_Resources.Track as track
from Main_Backend import *
from signals import *

class SWWaysideFrontend(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("Modules/SW_Wayside/Frontend/SW_Wayside_UI.ui", self)
                self.track_instance_copy = Track()

                # Receives updates from backend
                signals.sw_wayside_update_frontend.connect(self.update_frontend)

                # If any change in manual mode, need to override system with their inputs
                self.switch_direction_dropdown.currentTextChanged.connect(self.manual_switch_toggled)
                self.traffic_light_color_dropdown.currentTextChanged.connect(self.manual_light_toggled)
                self.crossing_status_dropdown.currentTextChanged.connect(self.manual_crossing_toggled)

                # If PLC upload button clicked
                self.upload_plc_program_button.clicked.connect(self.uploadPLCClicked)

                # If view track map button clicked
                self.track_map_view_button.clicked.connect(self.view_track_map_clicked)

                self.show()
        
        # Handles all frontend updates
        def update_frontend(self, track_instance):
                # update local instance of track
                self.track_instance_copy = track_instance

                # update the ui information
                self.update_display()

                # send any updates back to backend
                self.frontend_update()

        # Sends updates to backend
        def frontend_update(self):
                signals.sw_wayside_frontend_update.emit(self.track_instance_copy)

        # Calls all UI information
        def update_display(self):
                self.update_opeartion_dropdown()
                self.update_line_dropdown()
                self.update_wayside_dropdown()
                self.update_block_dropdown()
                self.update_block_information()

        # Updates copy track instance
        def update_copy_track(self, updatedTrack):
                self.trackInstanceCopy = updatedTrack
        
        # Updates elements shown once mode chosen
        def update_opeartion_dropdown(self):
                if(self.mode_selection_dropdown.currentText() == "Select Mode..."):
                        self.mode_selection_dropdown.setEnabled(False)
                        self.line_box.setEnabled(False)
                        self.switch_direction_dropdown.setEnabled(False)
                        self.traffic_light_color_dropdown.setEnabled(False)
                        self.crossing_status_dropdown.setEnabled(False)
                elif(self.mode_selection_dropdown.currentText() == "Manual"):
                        self.mode_selection_dropdown.setEnabled(False)
                        self.line_box.setEnabled(True)
                        self.switch_direction_dropdown.setEnabled(True)
                        self.traffic_light_color_dropdown.setEnabled(True)
                        self.crossing_status_dropdown.setEnabled(True)
                elif(self.mode_selection_dropdown.currentText() == "Automatic"):
                        self.mode_selection_dropdown.setEnabled(False)
                        self.line_box.setEnabled(True)
                        self.switch_direction_dropdown.setEnabled(False)
                        self.traffic_light_color_dropdown.setEnabled(False)
                        self.crossing_status_dropdown.setEnabled(False)

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
                elif(self.wayside_selection_dropdown.currentText() == "Wayside 1"):
                        self.upload_plc_program_button.setEnabled(True)
                        self.block_box.setEnabled(True)
                        self.block_selection_dropdown.clear()
                        self.block_selection_dropdown.addItem("Select Block...")
                        if(self.line_selection_dropdown.currentText() == "Green Line"):
                                for i in range(69):
                                        self.block_selection_dropdown.addItem("Block " + str(self.track_instance_copy.lines[1].blocks[i].blockNumber))
                        elif(self.line_selection_dropdown.currentText() == "Red Line"):
                                for i in range(24):
                                        self.block_selection_dropdown.addItem("Block " + str(self.track_instance_copy.lines[0].blocks[i].blockNumber))
                elif(self.wayside_selection_dropdown.currentText() == "Wayside 2"):
                        self.upload_plc_program_button.setEnabled(True)
                        self.block_box.setEnabled(True)
                        self.block_selection_dropdown.clear()
                        self.block_selection_dropdown.addItem("Select Block...")
                        if(self.line_selection_dropdown.currentText() == "Green Line"):
                                for i in range(69, 151):
                                        self.block_selection_dropdown.addItem("Block " + str(self.track_instance_copy.lines[1].blocks[i].blockNumber))
                        elif(self.line_selection_dropdown.currentText() == "Red Line"):
                                for i in range(24, 77):
                                        self.block_selection_dropdown.addItem("Block " + str(self.track_instance_copy.lines[0].blocks[i].blockNumber))

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
                        if(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].blockType == "Junction"):
                                self.junction_box.setEnabled(True)
                                self.station_box.setEnabled(False)
                                self.crossing_box.setEnabled(False)
                                self.switch_direction_dropdown.clear()
                                self.switch_direction_dropdown.addItems(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_switch_direction_string_list(curr_line_int))
                                self.traffic_light_color_dropdown.clear()
                                self.traffic_light_color_dropdown.addItems(["Red", "Green"])
                        elif(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].blockType == "Station"):
                                self.junction_box.setEnabled(False)
                                self.station_box.setEnabled(True)
                                self.crossing_box.setEnabled(False)
                        elif(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].blockType == "Crossing"):
                                self.junction_box.setEnabled(False)
                                self.station_box.setEnabled(False)
                                self.crossing_box.setEnabled(True)
                                self.crossing_status_dropdown.clear()
                                self.crossing_status_dropdown.addItems(["Active","Inactive"])
                        else:
                                self.crossing

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
                self.block_type_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].block_type)
                self.block_occupancy_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].block_occupancy)
                self.track_fault_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].track_fault_status)
                self.maintenance_active_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].maintenance_status)
                self.switch_direction_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].switch_direction)
                self.traffic_light_color_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].traffic_light_color)
                self.station_name_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].station_name)
                self.crossing_status_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].crossing_status)

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
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].switch_direction = self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_switch_direction_bool(self.switch_direction_dropdown.currentText(), curr_line_int)
        
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

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = SWWaysideFrontend()
        app.exec()
