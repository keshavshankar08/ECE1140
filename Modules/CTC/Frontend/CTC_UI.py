#Frontend Implementation for CTC Office

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import os
sys.path.append(".")
from signals import *
from Track_Resources.Track import *

##main module setup
class CTCFrontend(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/CTC/Frontend/CTC_UI.ui", self)

        #CONFIGURATION
        #Create objects
        self.track_instance_copy = Track()
        self.active_trains_copy = ActiveTrains()
        self.queue_trains_copy = QueueTrains()
        self.route_queue_copy = RouteQueue()
        self.ticket_sales_copy = 0

        #initialize display
        self.initialize_display()

        #SIGNALS
        #Update Entire Frontend
        signals.ctc_office_update_frontend.connect(self.update_frontend)

        #Update system time
        signals.current_system_time.connect(self.update_current_time)

        #Top Bar Signals
        self.open_schedule_builder_button.clicked.connect(self.schedule_builder_clicked)
        self.line_value_box.currentTextChanged.connect(self.line_value_box_changed)
        self.maintenance_update_button.clicked.connect(self.toggle_maintenance_button_clicked)

        #Manual Scheduling Signals
        self.manual_add_stop_button.clicked.connect(self.add_stop_button_clicked)
        self.manual_delete_stop_button.clicked.connect(self.delete_stop_button_clicked)
        self.manual_clear_all_stops_button.clicked.connect(self.manual_clear_all_stops_button_clicked)
        self.manual_dispatch_button.clicked.connect(self.manual_dispatch_button_clicked)

        #Automatic Scheduling Signals
        self.upload_schedule_button.clicked.connect(self.upload_schedule_button_clicked)

        #Queue Table Signals
        self.queue_table.itemSelectionChanged.connect(self.queue_table_selection_changed)

        #Dispatched Table Signals
        self.dispatched_trains_table.itemSelectionChanged.connect(self.dispatched_trains_table_selection_changed)

        #Maintenance Mode Signals
        
        #Test Bench Signals
        #self.TestBenchActivateButton.clicked.connect(self.test_bench_activate_button_clicked)
        #self.TestBenchDeactivateButton.clicked.connect(self.test_bench_deactivate_button_clicked)
        #self.TestUpdateButton.clicked.connect(self.test_bench_update_button_clicked)

        #Deactivate Test Bench On Startup
        #self.test_bench_deactivate_button_clicked()


    #Update Current Time
    def update_current_time(self, time):
        self.current_time.setPlainText(time.toString('HH:mm:ss'))
        
    #Update Frontend Functions
    def update_frontend(self, track_instance, active_trains_instance, ticket_sales):
        #update local instances
        self.update_copy_track(track_instance)
        self.update_copy_active_trains(active_trains_instance)
        self.update_ticket_sales(ticket_sales)

        #update the ui information
        self.update_display()

        #send update signals to ctc backend
        self.send_frontend_update()

    def send_frontend_update(self):
        signals.ctc_office_frontend_update.emit(self.track_instance_copy, self.active_trains_copy, self.ticket_sales_copy, self.queue_trains_copy)

    #updates active trains instance
    def update_copy_active_trains(self, updated_active_trains):
        self.active_trains_copy = updated_active_trains

    #updates track instance
    def update_copy_track_instance(self, updated_track_instance):
        self.track_instance_copy = updated_track_instance

    #updates ticket sales
    def update_ticket_sales(self, updated_ticket_sales):
        self.ticket_sales_copy = updated_ticket_sales

    def initialize_display(self):
        #Table Space
        manual_table_header = self.manual_table.horizontalHeader()
        manual_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        manual_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        manual_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        queue_table_header = self.queue_table.horizontalHeader()
        queue_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        queue_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        queue_selected_schedule_table_header = self.queue_selected_schedule_table.horizontalHeader()
        queue_selected_schedule_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        queue_selected_schedule_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        queue_selected_schedule_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        dispatched_trains_table_header = self.dispatched_trains_table.horizontalHeader()
        dispatched_trains_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        dispatched_trains_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        dispatched_trains_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        dispatch_selected_schedule_table_header = self.dispatch_selected_schedule_table.horizontalHeader()
        dispatch_selected_schedule_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        dispatch_selected_schedule_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        dispatch_selected_schedule_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        #Line Selector
        self.line_value_box.addItems({"Green Line", "Red Line"})
        self.line_value_box.setCurrentIndex(-1)

    def update_display(self):
        #clear tables
        self.queue_table.setRowCount(0)
        self.dispatched_trains_table.setRowCount(0)

        #update queue trains
        for train in self.queue_trains_copy.queue_trains:
            #Add train ID and Departure Time
            self.queue_table.insertRow(0)
            train_id = QTableWidgetItem(str(train.train_ID))
            self.queue_table.setItem(0, 0, train_id)
            departure_time = QTableWidgetItem(str(train.departure_time))
            self.queue_table.setItem(0, 1, departure_time)

        #update active trains
        for train in self.active_trains_copy.active_trains:
            #Add train ID and Departure Time
            self.dispatched_trains_table.insertRow(0)
            train_id = QTableWidgetItem(str(train.train_ID))
            self.dispatched_trains_table.setItem(0, 0, train_id)
            suggested_speed = QTableWidgetItem(str(train.current_suggested_speed) + " mph")
            self.dispatched_trains_table.setItem(0, 1, suggested_speed)
            current_authority = QTableWidgetItem(str(train.current_authority) + " blocks")
            self.dispatched_trains_table.setItem(0, 2, current_authority)

        #update track statuses
        #check what block it is
        if(self.set_block_maintenance_value.currentText() == ''):
            status_block = 0
        else:
            status_block = int(self.set_block_maintenance_value.currentText())

        #reset all indicators
        self.block_status_indicator.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.block_occupancy_indicator.setStyleSheet("background-color: rgb(255, 255, 255)")

        #if red line
        if (str(self.line_value_box.currentText()) == 'Red Line'):
            #check block occupancy
            if(self.track_instance_copy.red_line.blocks[status_block].block_occupancy == True):
                self.block_occupancy_indicator.setStyleSheet("background-color: rgb(167, 255, 167)")
            #check block status
            if(self.track_instance_copy.red_line.blocks[status_block].track_fault_status == True):
                self.block_status_indicator.setStyleSheet("background-color: rgb(255, 167, 167)")
            #check maintenance status
            if(self.track_instance_copy.red_line.blocks[status_block].maintenance_status == True):
                self.block_status_indicator.setStyleSheet("background-color: rgb(255, 255, 167)")

            #compile list of notable blocks
            maintenance_list = ""
            fault_list = ""
            occupied_list = ""
            for block in self.track_instance_copy.red_line.blocks:
                if(block.block_occupancy == True):
                    occupied_list = occupied_list + " " + str(block.block_number)
                if(block.track_fault_status == True):
                    fault_list = fault_list + " " + str(block.block_number)
                if(block.maintenance_status == True):
                    maintenance_list = maintenance_list + " " + str(block.block_number)
            
            #display to notable blocks output TODO
            self.notable_blocks_output.setPlainText("The occupied blocks are: " + occupied_list + "\n\nThe faulty blocks are: " + fault_list + "\n\nThe maintenance blocks are: " + maintenance_list)

        #if green line
        if (str(self.line_value_box.currentText()) == 'Green Line'):
            #check block occupancy
            if(self.track_instance_copy.green_line.blocks[status_block].block_occupancy == True):
                self.block_occupancy_indicator.setStyleSheet("background-color: rgb(167, 255, 167)")
            #check block status
            if(self.track_instance_copy.green_line.blocks[status_block].track_fault_status == True):
                self.block_status_indicator.setStyleSheet("background-color: rgb(167, 255, 255)")
            #check maintenance status
            if(self.track_instance_copy.green_line.blocks[status_block].maintenance_status == True):
                self.block_status_indicator.setStyleSheet("background-color: rgb(255, 255, 167)")

            #compile list of notable blocks
            maintenance_list = ""
            fault_list = ""
            occupied_list = ""
            for block in self.track_instance_copy.green_line.blocks:
                if(block.block_occupancy == True):
                    occupied_list = occupied_list + " " + str(block.block_number)
                if(block.track_fault_status == True):
                    fault_list = fault_list + " " + str(block.block_number)
                if(block.maintenance_status == True):
                    maintenance_list = maintenance_list + " " + str(block.block_number)
            
            #display to notable blocks output TODO
            self.notable_blocks_output.setPlainText("The occupied blocks are: " + occupied_list + "\n\nThe faulty blocks are: " + fault_list + "\n\nThe maintenance blocks are: " + maintenance_list)

        #update ticket sales
        self.hourly_ticket_sales_output.setPlainText(str(self.ticket_sales_copy))

        #clear schedules if empty queues
        if(len(self.queue_trains_copy.queue_trains) == 0):
            self.queue_selected_schedule_table.setRowCount(0)
        if(len(self.active_trains_copy.active_trains) == 0):
            self.dispatch_selected_schedule_table.setRowCount(0)

    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    #Menu Bar Functions
    def schedule_builder_clicked(self):
        os.system("start EXCEL.EXE")
    
    def toggle_maintenance_button_clicked(self):
        #get block to toggle maintenance
        maintenance_block = int(self.set_block_maintenance_value.currentText())

        if (str(self.line_value_box.currentText()) == 'Red Line'):
            for block in self.track_instance_copy.red_line.blocks:
                if(block.block_number == maintenance_block):
                    block.maintenance_status = not block.maintenance_status

        if (str(self.line_value_box.currentText()) == 'Green Line'):
            for block in self.track_instance_copy.green_line.blocks:
                if(block.block_number == maintenance_block):
                    block.maintenance_status = not block.maintenance_status

    def line_value_box_changed(self):
        #reset scheduling
        self.manual_table.setRowCount(0)
        
        #update line status
        if (str(self.line_value_box.currentText()) == 'Red Line'):
            self.set_block_maintenance_value.clear()
            self.set_block_maintenance_value.addItems([str(x.block_number) for x in self.track_instance_copy.red_line.blocks])
        if (str(self.line_value_box.currentText()) == 'Green Line'):
            self.set_block_maintenance_value.clear()
            self.set_block_maintenance_value.addItems([str(x.block_number) for x in self.track_instance_copy.green_line.blocks])

    def upload_schedule_button_clicked(self):
        pass

    #Manual Scheduling Functions
    def add_stop_button_clicked(self):
        #add a row
        rowPosition = self.manual_table.rowCount()
        self.manual_table.insertRow(rowPosition)

        #fill dwell time as 1:00
        dwell = QTableWidgetItem("1:00")
        self.manual_table.setItem(rowPosition, 2, dwell)
        
        #add a combo box in the first row
        combo = QtWidgets.QComboBox()
        if(self.line_value_box.currentText() == "Red Line"):
            combo.addItems(self.track_instance_copy.red_line_station_names)
        if(self.line_value_box.currentText() == "Green Line"):
            combo.addItems(self.track_instance_copy.green_line_station_names)
        self.manual_table.setCellWidget(rowPosition, 0, combo)
      
    def delete_stop_button_clicked(self):
        delIndex = self.manual_table.currentRow()
        self.manual_table.removeRow(delIndex)

    def manual_clear_all_stops_button_clicked(self):
        self.manual_table.setRowCount(0)

    def manual_dispatch_button_clicked(self):
        #create station and time data
        new_route = Route()

        #loop through 
        for row in range(self.manual_table.rowCount()):
            #errors for station
            if self.manual_table.cellWidget(row, 0).currentText() in new_route.stops:
                #TODO - Error of duplicate station
                continue
            
            #TODO - Error for station out of order
            '''
            #errors for time
            if self.manual_table.item(row, 1) == None:
                #TODO - Error if empty time
                print("no time")
                
            if not validate_time_hours(str(self.manual_table.item(row, 1).text())):
                #TODO - Error if incompatible time
                print("incorrect stop time format")
                
            if not validate_time_minutes(str(self.manual_table.item(row, 2).text())):
                #TODO - Error if incompatible time
                print("incorrect dwell time format")
            '''
                
            #save data to route object
            new_route.stops.append(self.manual_table.cellWidget(row, 0).currentText())
            new_route.stop_time.append(str(self.manual_table.item(row, 1).text()))
            new_route.dwell_time.append(str(self.manual_table.item(row, 2).text()))
        
        #add new route to the route queue
        self.route_queue_copy.add_route(new_route)

        #make a train in the train queue
        if(str(self.line_value_box.currentText()) == 'Green Line'):
            self.queue_trains_copy.add_train(Train(new_route, "Green"))
        if (str(self.line_value_box.currentText()) == 'Red Line'):
            self.queue_trains_copy.add_train(Train(new_route, "Red"))

        #clear the table
        self.manual_table.setRowCount(0)

        #TEMP -- UPDATE UI
        self.update_display()

    #Queue Tab Functions
    def queue_table_selection_changed(self):
        #get selection
        cur_index = self.queue_table.currentRow()

        #exit function if no selection
        if(cur_index == -1):
            return
        
        train_id = str(self.queue_table.item(cur_index, 0).text())
        
        #fill schedule, clear table first
        self.queue_selected_schedule_table.setRowCount(0)

        #check line
        if(str(self.line_value_box.currentText()) == 'Green Line'):
            #add each stop
            for i in reversed(range(len(self.route_queue_copy.routes[int(train_id[3])].stops))):
                #Add Stop, Station, and Dwell
                self.queue_selected_schedule_table.insertRow(0)
                station = QTableWidgetItem(str(self.track_instance_copy.green_line_block_to_station(self.route_queue_copy.routes[int(train_id[3])].stops[i])))
                self.queue_selected_schedule_table.setItem(0, 0, station)
                arrival = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].stop_time[i]))
                self.queue_selected_schedule_table.setItem(0, 1, arrival)
                dwell = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].dwell_time[i]))
                self.queue_selected_schedule_table.setItem(0, 2, dwell)
        
        if(str(self.line_value_box.currentText()) == 'Red Line'):
            #add each stop
            for i in reversed(range(len(self.route_queue_copy.routes[int(train_id[3])].stops))):
                #Add Stop, Station, and Dwell
                self.queue_selected_schedule_table.insertRow(0)
                station = QTableWidgetItem(str(self.track_instance_copy.red_line_block_to_station(self.route_queue_copy.routes[int(train_id[3])].stops[i])))
                self.queue_selected_schedule_table.setItem(0, 0, station)
                arrival = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].stop_time[i]))
                self.queue_selected_schedule_table.setItem(0, 1, arrival)
                dwell = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].dwell_time[i]))
                self.queue_selected_schedule_table.setItem(0, 2, dwell)

    #Queue Tab Functions
    def dispatched_trains_table_selection_changed(self):
        #get selection
        cur_index = self.dispatched_trains_table.currentRow()

        #exit function if no selection
        if(cur_index == -1):
            return
        
        train_id = str(self.dispatched_trains_table.item(cur_index, 0).text())
        
        #fill schedule, clear table first
        self.dispatch_selected_schedule_table.setRowCount(0)

        #check line
        if(str(self.line_value_box.currentText()) == 'Green Line'):
            #add each stop
            for i in reversed(range(len(self.route_queue_copy.routes[int(train_id[3])].stops))):
                #Add Stop, Station, and Dwell
                self.dispatch_selected_schedule_table.insertRow(0)
                station = QTableWidgetItem(str(self.track_instance_copy.green_line_block_to_station(self.route_queue_copy.routes[int(train_id[3])].stops[i])))
                self.dispatch_selected_schedule_table.setItem(0, 0, station)
                arrival = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].stop_time[i]))
                self.dispatch_selected_schedule_table.setItem(0, 1, arrival)
                dwell = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].dwell_time[i]))
                self.dispatch_selected_schedule_table.setItem(0, 2, dwell)
        
        if(str(self.line_value_box.currentText()) == 'Red Line'):
            #add each stop
            for i in reversed(range(len(self.route_queue_copy.routes[int(train_id[3])].stops))):
                #Add Stop, Station, and Dwell
                self.dispatch_selected_schedule_table.insertRow(0)
                station = QTableWidgetItem(str(self.track_instance_copy.red_line_block_to_station(self.route_queue_copy.routes[int(train_id[3])].stops[i])))
                self.dispatch_selected_schedule_table.setItem(0, 0, station)
                arrival = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].stop_time[i]))
                self.dispatch_selected_schedule_table.setItem(0, 1, arrival)
                dwell = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].dwell_time[i]))
                self.dispatch_selected_schedule_table.setItem(0, 2, dwell)

    def remove_selected_train_button_clicked(self):
        pass

    #Active Trains Tab Functions
    def dispatch_trains_table_selection_changed(self):
        pass
    
'''
    #Test Bench Handlers
    def update_maintenance_line_status(self):
        pass
    
    def test_bench_activate_button_clicked(self):
        self.TestSetBlockOccupancyValue.setEnabled(True)
        self.TestSetBlockCrossingStatusValue.setEnabled(True)
        self.TestSetSwitchStatusValue.setEnabled(True)
        self.TestSetLineSalesInput.setEnabled(True)
        self.TestSetTrafficLightValue.setEnabled(True)
        self.TestUpdateButton.setEnabled(True)
        self.TestBenchActivateButton.setStyleSheet("background-color: rgb(199, 199, 199)")
        self.TestBenchDeactivateButton.setStyleSheet("background-color: rgb(255, 255, 255)")
    
    def test_bench_deactivate_button_clicked(self):
        self.TestSetBlockOccupancyValue.setEnabled(False)
        self.TestSetBlockCrossingStatusValue.setEnabled(False)
        self.TestSetSwitchStatusValue.setEnabled(False)
        self.TestSetLineSalesInput.setEnabled(False)
        self.TestSetTrafficLightValue.setEnabled(False)
        self.TestUpdateButton.setEnabled(False)
        self.TestBenchActivateButton.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.TestBenchDeactivateButton.setStyleSheet("background-color: rgb(199, 199, 199)")
    
    def test_bench_update_button_clicked(self):
        pass
'''

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CTCFrontend()
    app.exec()

