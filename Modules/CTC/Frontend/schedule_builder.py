#Frontend Implementation for CTTC Schedule Builder

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import os
sys.path.append(".")
from signals import *
from Track_Resources.Track import *
from Modules.CTC.Backend.CTC_Backend import validate_time_hours, validate_time_minutes

##main module setup
class ScheduleBuilder(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules/CTC/Frontend/schedule_builder.ui", self)

        #initialize display
        self.initialize_display()

        #initialize variables
        self.track_instance_copy = Track()
        self.route_queue_copy = RouteQueue()
        self.queue_trains_copy = QueueTrains()

        #Menu Bar Signals
        self.line_value_box.currentTextChanged.connect(self.line_value_box_changed)

        #Manual Scheduling Signals
        self.route_add_stop_button.clicked.connect(self.add_stop_button_clicked)
        self.route_delete_stops_button.clicked.connect(self.delete_stop_button_clicked)
        self.route_clear_all_stops_button.clicked.connect(self.clear_all_stops_button_clicked)
        self.route_add_route_button.clicked.connect(self.add_route_button_clicked)

        #Route Queue Table Signals
        self.route_queue_table.itemSelectionChanged.connect(self.route_queue_table_selection_changed)

        #Confirm All Routes Button
        self.confirm_all_routes_button.clicked.connect(self.confirm_all_routes_button_clicked)

    # Function to even out the tables
    def initialize_display(self):
        #Table Space
        route_table_header = self.route_table.horizontalHeader()
        route_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        route_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        route_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        route_queue_header = self.route_queue_table.horizontalHeader()
        route_queue_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        route_queue_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        selected_schedule_table_header = self.selected_schedule_table.horizontalHeader()
        selected_schedule_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        selected_schedule_table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        selected_schedule_table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        #Line Selector
        self.line_value_box.addItems({"Green Line", "Red Line"})
        self.line_value_box.setCurrentIndex(-1)

    #Menu Bar Signals
    def line_value_box_changed(self):
        #reset scheduling
        self.route_table.setRowCount(0)

    #Manual Scheduling Functions
    def add_stop_button_clicked(self):
        #add a row
        rowPosition = self.route_table.rowCount()
        self.route_table.insertRow(rowPosition)

        #TEMP
        dispatch_time = QTableWidgetItem("12:00:00")
        self.route_table.setItem(rowPosition, 1, dispatch_time)

        #fill dwell time as 1:00
        dwell = QTableWidgetItem("1:00")
        self.route_table.setItem(rowPosition, 2, dwell)
        
        #add a combo box in the first row
        combo = QtWidgets.QComboBox()
        if(self.line_value_box.currentText() == "Red Line"):
            combo.addItems(self.track_instance_copy.red_line_station_names)
        if(self.line_value_box.currentText() == "Green Line"):
            combo.addItems(self.track_instance_copy.green_line_station_names_ordered)
        self.route_table.setCellWidget(rowPosition, 0, combo)

    def delete_stop_button_clicked(self):
        delIndex = self.route_table.currentRow()
        self.route_table.removeRow(delIndex)

    def clear_all_stops_button_clicked(self):
        self.route_table.setRowCount(0)

    def add_route_button_clicked(self):
        #create station and time data
        new_route = Route()

        route_order_list = []

        #loop through
        for row in range(self.route_table.rowCount()):
            #errors for station
            if self.route_table.cellWidget(row, 0).currentText() in new_route.stops:
                QMessageBox.information(self, "Alert", "Duplicate station. Try updating the routing.")
                return
            
            #error for stations out of order
            if(self.line_value_box.currentText() == 'Green Line'):
                index = np.where(np.array(self.track_instance_copy.green_line_station_names_ordered) == self.route_table.cellWidget(row, 0).currentText())
                for ord in route_order_list:
                    print(f'ord:',ord)
                    if index < ord:
                        QMessageBox.information(self, "Alert", "Station routed out of order. Follow the order in the dropdown menu.")
                        return
                route_order_list.append(index)

            #error for stations out of order
            if(self.line_value_box.currentText() == 'Red Line'):
                index = np.where(self.track_instance_copy.red_line_station_names == self.route_table.cellWidget(row, 0).currentText())
                for ord in route_order_list:
                    if index < ord:
                        QMessageBox.information(self, "Alert", "Station routed out of order. Follow the order in the dropdown menu.")
                        return
                route_order_list.append(index)
                      
            #errors for time
            if self.route_table.item(row, 1) == None:
                QMessageBox.information(self, "Alert", "A time value is missing. Fill and try again.")
                return
                
            if not validate_time_hours(str(self.route_table.item(row, 1).text())):
                QMessageBox.information(self, "Alert", "Incorrect stop time format. It must be in hh:mm:ss up to 23:59:59")
                return
                
            if not validate_time_minutes(str(self.route_table.item(row, 2).text())):
                QMessageBox.information(self, "Alert", "Incorrect dwell time format. It must be in mm:ss up to 59:59")
                return
            
            #save data to route object
            new_route.stops.append(self.route_table.cellWidget(row, 0).currentText())
            new_route.stop_time.append(str(self.route_table.item(row, 1).text()))
            new_route.dwell_time.append(str(self.route_table.item(row, 2).text()))

        #add new route to the route queue
        self.route_queue_copy.add_route(new_route)

        #make a train in the train queue
        if(str(self.line_value_box.currentText()) == 'Green Line'):
            self.queue_trains_copy.add_train(Train(new_route, 1))
        if (str(self.line_value_box.currentText()) == 'Red Line'):
            self.queue_trains_copy.add_train(Train(new_route, 0))

        #clear the tables
        self.route_table.setRowCount(0)
        self.route_queue_table.setRowCount(0)

        #update train queue list
        for train in self.queue_trains_copy.queue_trains:
            #Add train ID and Departure Time
            self.route_queue_table.insertRow(0)
            train_id = QTableWidgetItem(str(train.train_ID))
            self.route_queue_table.setItem(0, 0, train_id)
            departure_time = QTableWidgetItem(str(train.departure_time))
            self.route_queue_table.setItem(0, 1, departure_time)

        #deactivate line change ability
        if(len(self.route_queue_copy.routes) > 0):
            self.line_value_box.setEnabled(False)
    
    def route_queue_table_selection_changed(self):
        #get selection
        cur_index = self.route_queue_table.currentRow()

        #exit function if no selection
        if(cur_index == -1):
            return
        
        train_id = str(self.route_queue_table.item(cur_index, 0).text())
        
        #fill schedule, clear table first
        self.selected_schedule_table.setRowCount(0)

        #check line
        if(str(self.line_value_box.currentText()) == 'Green Line'):
            #add each stop
            for i in reversed(range(len(self.route_queue_copy.routes[int(train_id[3])].stops))):
                #Add Stop, Station, and Dwell
                self.selected_schedule_table.insertRow(0)
                station = QTableWidgetItem(str(self.track_instance_copy.green_line_block_to_station(self.route_queue_copy.routes[int(train_id[3])].stops[i])))
                self.selected_schedule_table.setItem(0, 0, station)
                arrival = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].stop_time[i]))
                self.selected_schedule_table.setItem(0, 1, arrival)
                dwell = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].dwell_time[i]))
                self.selected_schedule_table.setItem(0, 2, dwell)
        
        if(str(self.line_value_box.currentText()) == 'Red Line'):
            #add each stop
            for i in reversed(range(len(self.route_queue_copy.routes[int(train_id[3])].stops))):
                #Add Stop, Station, and Dwell
                self.selected_schedule_table.insertRow(0)
                station = QTableWidgetItem(str(self.track_instance_copy.red_line_block_to_station(self.route_queue_copy.routes[int(train_id[3])].stops[i])))
                self.selected_schedule_table.setItem(0, 0, station)
                arrival = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].stop_time[i]))
                self.selected_schedule_table.setItem(0, 1, arrival)
                dwell = QTableWidgetItem(str(self.route_queue_copy.routes[int(train_id[3])].dwell_time[i]))
                self.selected_schedule_table.setItem(0, 2, dwell)

    #function for when confirm all routes button is pressed
    def confirm_all_routes_button_clicked(self):
        #error handling for empty routes
        if(len(self.route_queue_copy.routes) == 0):
            QMessageBox.information(self, "Alert", "Add routes before confirming.")

        #get filename for schedule
        name, done1 = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter file name')

        while(len(name) < 3):
            QMessageBox.information(self, "Alert", "Filename not long enough. Must be longer than 3 characters.")
            name, done1 = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter file name')

        #create a file
        filename = "Modules/CTC/Backend/Routes/" + str(name) + ".txt"
        route_file = open(filename, "w")

        #write the line value
        route_file.write(str(self.line_value_box.currentText()) + "\n")

        #save each route with a delimiter as a string
        for route in self.route_queue_copy.routes:
            #create strings of route variables
            stop_string = ','.join(str(x) for x in route.stops) + "\n"
            dwell_string = ','.join(str(x) for x in route.dwell_time) + "\n"
            stop_time_string = ','.join(str(x) for x in route.stop_time) + "\n"

            #write to file with - as a delimiter
            route_file.writelines([stop_string, dwell_string, stop_time_string, "-\n"])

        #close file
        route_file.close()

        #reactivate the ability to change lines
        self.line_value_box.setEnabled(True)

        #clear all tables
        self.selected_schedule_table.setRowCount(0)
        self.route_table.setRowCount(0)
        self.route_queue_table.setRowCount(0)

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ScheduleBuilder()
    app.exec()