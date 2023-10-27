#Frontend Implementation for CTC Office

from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt, QTime
from time import gmtime, strftime
from itertools import islice
import sys
import os
import time
sys.path.append(".")
from signals import *
from Track_Resources.Track import *
from Modules.CTC.Backend.CTC_Backend import *

##main module setup
class CTCModuleUI(QtWidgets.QMainWindow):
    def __init__(self):
        #setup
        super().__init__()
        uic.loadUi("Modules\CTC\Frontend\CTC_UI.ui", self)

        #CONFIGURATION
        #Create multiple objects
        self.track = Track()
        self.routeQueue = RouteQueue()

        #Table Space
        manualTableHeader = self.ManualTable.horizontalHeader()
        manualTableHeader.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        manualTableHeader.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        manualTableHeader.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        automaticTableHeader = self.AutomaticTable.horizontalHeader()
        automaticTableHeader.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        automaticTableHeader.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        automaticTableHeader.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        #Line Selector
        self.LineValueBox.addItems({"Green Line", "Red Line"})

        #SIGNALS
        #Top Bar Signals
        self.OpenScheduleBuilderButton.clicked.connect(self.schedule_builder_clicked)
        self.LineValueBox.currentTextChanged.connect(self.line_value_box_changed)

        #Manual Scheduling Signals
        self.ManualAddStopButton.clicked.connect(self.add_stop_button_clicked)
        self.ManualDeleteStopButton.clicked.connect(self.delete_stop_button_clicked)
        self.ManualClearAllStopsButton.clicked.connect(self.manual_clear_all_stops_button_clicked)
        self.ManualDispatchButton.clicked.connect(self.manual_dispatch_button_clicked)

        #Automatic Scheduling Signals
        self.AutomaticUploadScheduleButton.clicked.connect(self.upload_schedule_button_clicked)
        self.AutomaticClearAllButton.clicked.connect(self.automatic_clear_all_button_clicked)

        #Maintenance Mode Signals
        self.MaintenanceUpdateButton.clicked.connect(self.maintenance_update_button_clicked)

        #Test Bench Signals
        self.TestBenchActivateButton.clicked.connect(self.test_bench_activate_button_clicked)
        self.TestBenchDeactivateButton.clicked.connect(self.test_bench_deactivate_button_clicked)
        self.TestUpdateButton.clicked.connect(self.test_bench_update_button_clicked)

        #Deactivate Test Bench On Startup
        self.test_bench_deactivate_button_clicked()

        #end with showing main window
        self.show()

    #Menu Bar Functions
    def schedule_builder_clicked(self):
        os.system("start EXCEL.EXE")
    def line_value_box_changed(self):
        #reset all scheduling
        self.ManualTable.setRowCount(0)
        self.AutomaticTable.setRowCount(0)

    #Manual Scheduling Functions
    def add_stop_button_clicked(self):
        rowPosition = self.ManualTable.rowCount()
        self.ManualTable.insertRow(rowPosition)
        combo = QtWidgets.QComboBox()
        if(self.LineValueBox.currentText() == "Red Line"):
            combo.addItems(self.track.redLineStationNames)
        if(self.LineValueBox.currentText() == "Green Line"):
            combo.addItems(self.track.greenLineStationNames)
        self.ManualTable.setCellWidget(rowPosition, 0, combo)
        #self.ManualTable.item(rowPosition, 2).setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
    def delete_stop_button_clicked(self):
        delIndex = self.ManualTable.currentRow()
        self.ManualTable.removeRow(delIndex)
    def manual_clear_all_stops_button_clicked(self):
        self.ManualTable.setRowCount(0)
    def manual_dispatch_button_clicked(self):
        #create station and time data
        stopStationData = []
        stopTimeData = []

        #loop through 
        for row in range(self.ManualTable.rowCount()):
            #errors for station
            if self.ManualTable.cellWidget(row, 0).currentText() in stopStationData:
                #TODO - Error of duplicate station
                continue
            #TODO - Error for station out of order

            #errors for time
            if self.ManualTable.item(row, 1) == None:
                #TODO - Error if empty time
                print("no time")
                continue
            if not validateTimeInput(str(self.ManualTable.item(row, 1).text())):
                #TODO - Error if incompatible time
                print("bad time")
                continue

            #save data to route queue
            stopStationData.append(self.ManualTable.cellWidget(row, 0).currentText())
            stopTimeData.append(str(self.ManualTable.item(row, 1).text()))
        
        self.ManualTable.setRowCount(0)

    #Automatic Scheduling Functions
    def upload_schedule_button_clicked(self):
        pass
    def automatic_clear_all_button_clicked(self):
        self.AutomaticTable.setRowCount(0)
    def automatic_dispatch_button_clicked(self):
        #all temporary --> set block 1 to blue, clear cells, set output authority
        tempID = self.AutomaticTable.item(0,0).text
        print(tempID)
        self.LineStatusBlock1.setStyleSheet("background-color: rgb(69, 69, 255)")
        self.AutomaticTable.setRowCount(0)

        #set output text
        self.TestOutputsView.appendPlainText(str(tempID) + "suggested speed: 12 mph\nauthority: 400 ft")

    #Maintenance Mode Functions
    def maintenance_update_button_clicked(self):
        #create a temporary variable to hold the block under maintenance and update in backend
        maintenanceTemp = ''.join(c for c in self.SetBlockMaintenanceValue.currentText() if c.isdigit())
        if(maintenanceTemp != ''):
            self.blueLine.maintenanceStatus[int(maintenanceTemp) - 1] = not self.blueLine.maintenanceStatus[int(maintenanceTemp) - 1]
        
        #return to '-' value
        self.SetBlockMaintenanceValue.setCurrentText('-')

        self.update_maintenance_line_status()

        #update text
        self.BlocksUnderMaintenanceView.setPlainText("")
        for i in reversed(range(len(self.blueLine.maintenanceStatus))):
            if(self.blueLine.maintenanceStatus[i]):
                self.BlocksUnderMaintenanceView.appendPlainText("Block " + str(i+1) + " is under maintenance.")
    
    #Test Bench Handlers
    def update_maintenance_line_status(self):
        #update block maintenance
        #blocks 1-5
        if(self.blueLine.maintenanceStatus[0] == True):
            self.LineStatusBlock1.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock1.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[1] == True):
            self.LineStatusBlock2.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock2.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[2] == True):
            self.LineStatusBlock3.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock3.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[3] == True):
            self.LineStatusBlock4.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock4.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[4] == True):
            self.LineStatusBlock5.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock5.setStyleSheet("background-color: rgb(222, 224, 255)")
        #blocks 6-10
        if(self.blueLine.maintenanceStatus[5] == True):
            self.LineStatusBlock6.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock6.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[6] == True):
            self.LineStatusBlock7.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock7.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[7] == True):
            self.LineStatusBlock8.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock8.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[8] == True):
            self.LineStatusBlock9.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock9.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[9] == True):
            self.LineStatusBlock10.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock10.setStyleSheet("background-color: rgb(222, 224, 255)")
        #blocks 11-15
        if(self.blueLine.maintenanceStatus[10] == True):
            self.LineStatusBlock11.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock11.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[11] == True):
            self.LineStatusBlock12.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock12.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[12] == True):
            self.LineStatusBlock13.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock13.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[13] == True):
            self.LineStatusBlock14.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock14.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.maintenanceStatus[14] == True):
            self.LineStatusBlock15.setStyleSheet("background-color: rgb(255, 255, 122)")
        else:
            self.LineStatusBlock15.setStyleSheet("background-color: rgb(222, 224, 255)")
    def update_line_status(self):
        #update block occupancy
        #blocks 1-5
        if(self.blueLine.blockOccupancy[0] == True):
            self.LineStatusBlock1.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock1.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[1] == True):
            self.LineStatusBlock2.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock2.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[2] == True):
            self.LineStatusBlock3.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock3.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[3] == True):
            self.LineStatusBlock4.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock4.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[4] == True):
            self.LineStatusBlock5.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock5.setStyleSheet("background-color: rgb(222, 224, 255)")
        #blocks 6-10
        if(self.blueLine.blockOccupancy[5] == True):
            self.LineStatusBlock6.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock6.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[6] == True):
            self.LineStatusBlock7.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock7.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[7] == True):
            self.LineStatusBlock8.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock8.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[8] == True):
            self.LineStatusBlock9.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock9.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[9] == True):
            self.LineStatusBlock10.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock10.setStyleSheet("background-color: rgb(222, 224, 255)")
        #blocks 11-15
        if(self.blueLine.blockOccupancy[10] == True):
            self.LineStatusBlock11.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock11.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[11] == True):
            self.LineStatusBlock12.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock12.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[12] == True):
            self.LineStatusBlock13.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock13.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[13] == True):
            self.LineStatusBlock14.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock14.setStyleSheet("background-color: rgb(222, 224, 255)")
        if(self.blueLine.blockOccupancy[14] == True):
            self.LineStatusBlock15.setStyleSheet("background-color: rgb(69, 69, 255)")
        else:
            self.LineStatusBlock15.setStyleSheet("background-color: rgb(222, 224, 255)")

        #update switch status
        if(self.blueLine.switchStatus[4] == True):
            self.LineStatusSwitch11.setStyleSheet("color: rgb(0, 0, 0)")
            self.LineStatusSwitch6.setStyleSheet("color: rgb(216, 216, 216)")
        else:
            self.LineStatusSwitch11.setStyleSheet("color: rgb(216, 216, 216)")
            self.LineStatusSwitch6.setStyleSheet("color: rgb(0, 0, 0)")

        #update lights
        if(self.blueLine.trafficLightStatus[4] == True):
            self.LineStatusBlockLight5.setStyleSheet("background-color: rgb(197, 255, 197)")
        else:
            self.LineStatusBlockLight5.setStyleSheet("background-color: rgb(255, 197, 197)")
        if(self.blueLine.trafficLightStatus[5] == True):
            self.LineStatusBlockLight6.setStyleSheet("background-color: rgb(197, 255, 197)")
        else:
            self.LineStatusBlockLight6.setStyleSheet("background-color: rgb(255, 197, 197)")
        if(self.blueLine.trafficLightStatus[10] == True):
            self.LineStatusBlockLight11.setStyleSheet("background-color: rgb(197, 255, 197)")
        else:
            self.LineStatusBlockLight11.setStyleSheet("background-color: rgb(255, 197, 197)")
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
        #set temp values to hold selected test bench inputs, remove all other characters
        occupancyTemp = ''.join(c for c in self.TestSetBlockOccupancyValue.currentText() if c.isdigit())
        #crossingTemp = ''.join(c for c in self.TestSetBlockCrossingStatusValue.currentText() if c.isdigit())
        switchTemp = ''.join(c for c in self.TestSetSwitchStatusValue.currentText() if c.isdigit())
        trafficTemp = ''.join(c for c in self.TestSetTrafficLightValue.currentText() if c.isdigit())

        #save line sales
        if(self.TestSetLineSalesInput.text() != ''):
            if(self.blueLine.currentLineSales == 0):
                self.blueLine.currentLineSales = self.TestSetLineSalesInput.text()
            else:
                self.blueLine.pastLineSales.append(self.blueLine.currentLineSales)
                self.blueLine.currentLineSales = self.TestSetLineSalesInput.text()

        #fill arrays with updated values
        if(occupancyTemp != ''):
            self.blueLine.blockOccupancy[int(occupancyTemp) - 1] = not self.blueLine.blockOccupancy[int(occupancyTemp) - 1]
        #if(crossingTemp != ''):
            #self.blueLine.blockCrossingStatus[int(crossingTemp) - 1] = not self.blueLine.blockCrossingStatus[int(crossingTemp) - 1]
        if(switchTemp != ''):
            self.blueLine.switchStatus[int(switchTemp[0]) - 1] = not self.blueLine.switchStatus[int(switchTemp[0]) - 1]
        if(trafficTemp != ''):
            self.blueLine.trafficLightStatus[int(trafficTemp) - 1] = not self.blueLine.trafficLightStatus[int(trafficTemp) - 1]

        #temporary line sales action
        if(self.TestSetLineSalesInput.text() != ''):
            self.LineTicketSalesView.setPlainText("Current Ticket Sales: " + self.blueLine.currentLineSales)
            for i in reversed(range(len(self.blueLine.pastLineSales))):
                self.LineTicketSalesView.appendPlainText("Past Ticket Sales: " + self.blueLine.pastLineSales[i])

        #return to '-' values
        self.TestSetBlockOccupancyValue.setCurrentText('-')
        self.TestSetBlockCrossingStatusValue.setCurrentText('-')
        self.TestSetSwitchStatusValue.setCurrentText('-')
        self.TestSetTrafficLightValue.setCurrentText('-')
        self.TestSetLineSalesInput.setText('')

        #update line status
        self.update_line_status()

#Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CTCModuleUI()
    app.exec()