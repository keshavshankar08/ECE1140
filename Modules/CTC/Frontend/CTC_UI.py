#Frontend Implementation for CTC Office

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import os
sys.path.append(".")
from signals import *
from Track_Resources.Track import *
from Modules.CTC.Backend.CTC_Backend import *

##main module setup
class CTCFrontend(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules\CTC\Frontend\CTC_UI.ui", self)

        #CONFIGURATION
        #Create objects
        self.track_instance_copy = Track()
        self.active_trains_copy = ActiveTrains()
        self.queue_trains_copy = QueueTrains()
        self.route_queue_copy = RouteQueue()

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

        #SIGNALS
        #Update Entire Frontend
        signals.ctc_office_frontend_update.connect(self.update_frontend)

        #Top Bar Signals
        self.open_schedule_builder_button.clicked.connect(self.schedule_builder_clicked)
        self.line_value_box.currentTextChanged.connect(self.line_value_box_changed)

        #Manual Scheduling Signals
        self.manual_add_stop_button.clicked.connect(self.add_stop_button_clicked)
        self.manual_delete_stop_button.clicked.connect(self.delete_stop_button_clicked)
        self.manual_clear_all_stops_button.clicked.connect(self.manual_clear_all_stops_button_clicked)
        self.manual_dispatch_button.clicked.connect(self.manual_dispatch_button_clicked)

        #Automatic Scheduling Signals
        self.upload_schedule_button.clicked.connect(self.upload_schedule_button_clicked)

        #Maintenance Mode Signals
        
        #Test Bench Signals
        #self.TestBenchActivateButton.clicked.connect(self.test_bench_activate_button_clicked)
        #self.TestBenchDeactivateButton.clicked.connect(self.test_bench_deactivate_button_clicked)
        #self.TestUpdateButton.clicked.connect(self.test_bench_update_button_clicked)

        #Deactivate Test Bench On Startup
        #self.test_bench_deactivate_button_clicked()

        #end with showing main window
        self.show()

    #Update Frontend Functions
    def update_frontend(self, track_instance):
        #update local instance of track
        self.update_copy_track(track_instance)

        #update the ui information
        self.update_display()

        #send update signals to ctc backend
        self.send_backend_update()

    def send_backend_update(self):
        signals.ctc_office_frontend_update.emit(self.track_instance_copy)

    def update_display(self):
        #update functions
        pass

    def update_copy_track(self, updated_track):
        self.track_instance_copy = updated_track

    #Menu Bar Functions
    def schedule_builder_clicked(self):
        os.system("start EXCEL.EXE")
    
    def line_value_box_changed(self):
        #reset scheduling
        self.manual_table.setRowCount(0)
        
        #update line status
        if (str(self.line_value_box.currentText()) == 'Red Line'):
            self.set_block_maintenance_value.clear()
            self.set_block_maintenance_value.addItems([str(x) for x in list(self.track_instance_copy.red_line.graph.keys())])
        if (str(self.line_value_box.currentText()) == 'Green Line'):
            self.set_block_maintenance_value.clear()
            self.set_block_maintenance_value.addItems([str(x) for x in list(self.track_instance_copy.green_line.graph.keys())])

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

            #save data to route object
            new_route.stops.append(self.manual_table.cellWidget(row, 0).currentText())
            new_route.stop_time.append(str(self.manual_table.item(row, 1).text()))
            new_route.dwell_time.append(str(self.manual_table.item(row, 2).text()))
        
        #add new route to the route queue
        self.route_queue_copy.add_route(new_route)

        testTrain = Train(new_route)
        #print(testTrain)

        #make a train in the train queue
        #self.queue_trains_copy.add_train(Train(new_route))

        self.manual_table.setRowCount(0)

    #Queue Tab Functions
    def queue_table_selection_changed(self):
        pass

    def remove_selected_train_button_clicked(self):
        pass

    #Active Trains Tab Functions
    def dispatch_trains_table_selection_changed(self):
        pass

    #Maintenance Mode Functions
    def toggle_maintenance_button_clicked(self):
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
