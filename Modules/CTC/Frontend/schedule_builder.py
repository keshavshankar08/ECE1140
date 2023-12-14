#Frontend Implementation for CTTC Schedule Builder

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
        uic.loadUi("Modules/CTC/Frontend/schedule_builder.ui", self)

        #initialize display
        self.initialize_display()

        #initialize variables
        self.track_instance_copy = Track()
        self.route_queue_copy = RouteQueue()

        #Manual Scheduling Signals
        self.route_add_stop_button.clicked.connect(self.add_stop_button_clicked)
        self.route_delete_stop_button.clicked.connect(self.delete_stop_button_clicked)
        self.route_clear_all_stops_button.clicked.connect(self.clear_all_stops_button_clicked)
        self.route_add_route.clicked.connect(self.add_route_button_clicked)

        #TODO
        #Queue Table Signals
        self.route.itemSelectionChanged.connect(self.route_table_selection_changed)

        #Dispatched Table Signals
        self.route_queue_table.itemSelectionChanged.connect(self.route_queue_table_selection_changed)

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

        #loop through 
        for row in range(self.route_table.rowCount()):
            #errors for station
            if self.route_table.cellWidget(row, 0).currentText() in new_route.stops:
                #TODO - Error of duplicate station
                continue
            
            #TODO - Error for station out of order
            '''
            #errors for time
            if self.route_table.item(row, 1) == None:
                #TODO - Error if empty time
                print("no time")
                
            if not validate_time_hours(str(self.route_table.item(row, 1).text())):
                #TODO - Error if incompatible time
                print("incorrect stop time format")
                
            if not validate_time_minutes(str(self.route_table.item(row, 2).text())):
                #TODO - Error if incompatible time
                print("incorrect dwell time format")
            '''
                
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

        #clear the table
        self.route_table.setRowCount(0)

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CTCFrontend()
    app.exec()