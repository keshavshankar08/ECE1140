import sys
sys.path.append(".")
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import *

class ADMIN(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("Admin_UI.ui", self)
                self.track_instance_copy = Track()
                self.active_trains_instance_copy = ActiveTrains()
                self.ticket_sales_instance_copy = 0
                signals.update_admin.connect(self.update_admin)
                self.block_occupancy_occupied_button.clicked.connect(self.block_occupied_clicked)
                self.block_occupancy_unoccupied_button.clicked.connect(self.block_unoccupied_clicked)
                self.track_fault_detected_button.clicked.connect(self.track_fault_detected_clicked)
                self.track_fault_undetected_button.clicked.connect(self.track_fault_undetected_clicked)
                self.maintenance_active_button.clicked.connect(self.maintenance_active_clicked)
                self.maintenance_inactive_button.clicked.connect(self.maintenance_inactive_clicked)
                self.ticket_sales_input.textChanged.connect(self.update_ticket_sales_changed)
                self.adminPower.valueChanged.connect(self.admin_force_power)

                self.last_line_state = ""
                self.last_wayside_state = ""

        # Handles all admin updates
        def update_admin(self, track_instance, active_trains_instance):
                # update local instance of track
                self.update_copy_track(track_instance)
                self.update_copy_active_trains(active_trains_instance)

                # update the ui information
                self.update_display()

                # send updated signals to wayside backend
                self.send_admin_update()

        def send_admin_update(self):
                signals.admin_update.emit(self.track_instance_copy, self.active_trains_instance_copy, self.ticket_sales_instance_copy)

        # Updates all UI display information
        def update_display(self):
                self.update_line_dropdown()
                self.update_wayside_dropdown()
                self.update_block_dropdown()

        # Updates local instance of track
        def update_copy_track(self, updated_track):
                self.track_instance_copy = updated_track

        # Updates active trains instance
        def update_copy_active_trains(self, updated_active_trains):
                self.active_trains_instance_copy = updated_active_trains

        def update_copy_ticket_sales(self, updated_ticket_sales):
                self.ticket_sales_instance_copy = updated_ticket_sales

        # Updates Ticket Sales as Changed
        def update_ticket_sales_changed(self):
            if(self.ticket_sales_input.text() == ''):
                self.ticket_sales_instance_copy = 0
            else:
                self.ticket_sales_instance_copy = int(self.ticket_sales_input.text())

        # Updates elements shown once line chosen
        def update_line_dropdown(self):
                if(self.line_selection_dropdown.currentText() == "Select Line..."):
                        self.wayside_box.setEnabled(False)
                elif(self.line_selection_dropdown.currentText() == "Green Line"):
                        self.wayside_box.setEnabled(True)
                elif(self.line_selection_dropdown.currentText() == "Red Line"):
                        self.wayside_box.setEnabled(True)

        # Updates elements shown once wayside chosen
        def update_wayside_dropdown(self):
                if(self.wayside_selection_dropdown.currentText() == "Select Wayside..."):
                        self.block_box.setEnabled(False)
                elif((self.wayside_selection_dropdown.currentText() == "Wayside 1") and (self.last_wayside_state != "Wayside 1" or self.last_line_state != self.line_selection_dropdown.currentText())):
                        self.last_wayside_state = "Wayside 1"
                        self.last_line_state = self.line_selection_dropdown.currentText()
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
                        self.block_occupancy_occupied_button.setEnabled(False)
                        self.block_occupancy_unoccupied_button.setEnabled(False)
                        self.block_occupancy_value.setEnabled(False)
                        self.track_fault_detected_button.setEnabled(False)
                        self.track_fault_undetected_button.setEnabled(False)
                        self.track_fault_value.setEnabled(False)
                        self.maintenance_active_button.setEnabled(False)
                        self.maintenance_inactive_button.setEnabled(False)
                        self.maintenance_value.setEnabled(False)

                else:
                        self.block_occupancy_occupied_button.setEnabled(True)
                        self.block_occupancy_unoccupied_button.setEnabled(True)
                        self.block_occupancy_value.setEnabled(True)
                        self.track_fault_detected_button.setEnabled(True)
                        self.track_fault_undetected_button.setEnabled(True)
                        self.track_fault_value.setEnabled(True)
                        self.maintenance_active_button.setEnabled(True)
                        self.maintenance_inactive_button.setEnabled(True)
                        self.maintenance_value.setEnabled(True)
                        curr_line_int = self.get_current_line_displayed_int()
                        curr_block_int = self.get_current_block_displayed_int()
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
                self.block_occupancy_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_block_occupancy_string())
                self.track_fault_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_track_fault_status_string())
                self.maintenance_value.setText(self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].get_maintenance_status_string())

        def block_occupied_clicked(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].block_occupancy = True

        def block_unoccupied_clicked(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].block_occupancy = False

        def track_fault_detected_clicked(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].track_fault_status = True

        def track_fault_undetected_clicked(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].track_fault_status = False

        def maintenance_active_clicked(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].maintenance_status = True
        
        def maintenance_inactive_clicked(self):
                curr_line_int = self.get_current_line_displayed_int()
                curr_block_int = self.get_current_block_displayed_int()
                self.track_instance_copy.lines[curr_line_int].blocks[curr_block_int].maintenance_status = False
                
        def admin_force_power(self, value):
                signals.train_controller_send_power_command.emit(value)