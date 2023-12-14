import sys
sys.path.append(".")
import os, openpyxl, random 
from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from signals import signals
from Track_Resources.Track import *
from Train_Resources.CTC_Train import * 
        
class TrackModelModule(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('Modules/Track_Model/Frontend/Track_Model_UI.ui',self)
        
        # instantiate copy of track class object 
        self.track_instance_copy = Track()
        
        # instantiate copy of active trains class object
        self.active_trains_instance_copy = ActiveTrains()
        
        # member variables to hold selected block and selected line
        self.clicked_block = 0
        self.line_name = None
        
        # member variable to hold occupied block
        self.occupied_block = 0
        self.block_grade = 0
        self.speed_limit = 0
        self.train_id = None
        self.distance_from_yard_receive = 0
        
        self.train_id
        self.new_passengers = 0
        
        # declare lists to store line data
        self.red_line_data = []
        self.green_line_data = []
        
        # tickets and passenger variables
        self.tickets_sold = 0
        self.passengers_on = 0
        self.passengers_off = 0
        self.red_sales = 0
        self.green_sales = 0
        
        # receives updates from main backend
        signals.track_model_update_backend.connect(self.backend_update_backend)

        # receive updates from train model
        signals.trainModel_send_distance_from_yard.connect(self.receive_distance_from_yard)
        
        
        # disable line selector until track is loaded to avoid undefined behavior
        self.TrackLineColorValue.setEnabled(False)
        
        # line color combo box hint behavior, show hint initially
        self.TrackLineColorValue.installEventFilter(self)
        self.LineSelectHint.setVisible(True)
        
        # load track model button
        self.LoadTrackModelButton.clicked.connect(self.track_layout)
        
        # failure mode handler
        self.TrackCircuitFailureToggleButton.toggled.connect(self.failure_mode)
        self.BrokenRailToggleButton.toggled.connect(self.failure_mode)
        self.PowerFailureToggleButton.toggled.connect(self.failure_mode)
        
        # env temp changed signal 
        self.track_heater_display.setText("Inactive")
        self.SetEnvironmentTemperatureInputBox.valueChanged.connect(self.track_heater)

        # set up scene for graphics view and set scene size to widget size 
        self.graphicsView.setScene(QtWidgets.QGraphicsScene())
        self.graphicsView.setSceneRect(0,0,1221,521)
        
        # build track in graphics view
        self.TrackLineColorValue.currentTextChanged.connect(self.build_track_map)
        
        # connect mouse event to a function 
        self.graphicsView.mousePressEvent = self.mousePressEvent
        
    # functions 
    
    # send updates from track model backend to main backend
    def send_main_backend_update(self):
        signals.track_model_backend_update.emit(self.track_instance_copy, self.active_trains_instance_copy.Train)
    
    # Update local instance of track 
    def update_copy_track(self,updated_track):
        self.track_instance_copy = updated_track
    
    # Update local instance of active trains
    def update_copy_active_trains(self,updated_active_trains):
        self.active_trains_instance_copy = updated_active_trains

    # main function to carry out all functions in a cycle
    def backend_update_backend(self,track_instance,active_trains):
        # update local instance of track
        self.update_copy_track(track_instance)
        
        # update local instance of active trains
        self.update_copy_active_trains(active_trains)
   
        # update frontend 
        self.display_block_info()
        
        # receive train model signals
        self.receive_train_model_signals()
        
        # update block occupancies
        self.block_occupancy()
        
        self.yard_occupancy()
        
        # update traffic lights
        self.set_light_color()
        
        # update crossing statuses
        self.set_crossing_light()
        
        # signals to train model
        self.send_train_info()
        
        # send updated signals to main backend
        self.send_main_backend_update()
    
    # send active trains info to train model
    def send_train_info(self):
        # loop through all active trains and send info to train model 
        for train in self.active_trains_instance_copy.active_trains:
            signals.track_model_suggested_speed.emit(int(train.train_ID),train.current_suggested_speed)
            if train.current_authority == -1:
                signals.track_model_authority.emit(int(train.train_ID), 0)
            else:
                # convert to meters then emit to train model 
                if train.current_line == 0:
                    # green line
                    start = train.current_block
                    end = start + train.current_authority
                    sum = 0
                    for block_length in self.track_instance_copy.red_line_block_lengths[start:end]:
                        sum += block_length
                    signals.track_model_authority.emit(int(train.train_ID), sum)
                    
                if train.current_line == 1:
                    # green line
                    start = train.current_block
                    end = start + train.current_authority
                    sum = 0
                    for block_length in self.track_instance_copy.green_line_block_lengths[start:end]:
                        sum += block_length
                    signals.track_model_authority.emit(int(train.train_ID), sum)
        
    # failure mode handler
    def failure_mode(self):
        if self.TrackCircuitFailureToggleButton.isChecked() or self.BrokenRailToggleButton.isChecked() or self.PowerFailureToggleButton.isChecked():
            self.track_instance_copy.lines[1].blocks[int(self.clicked_block)].track_fault_status = True
        else: 
            self.track_instance_copy.lines[1].blocks[int(self.clicked_block)].track_fault_status = False
    
    # track heater handler
    def track_heater(self,value):
        # activate track heater if 32 degrees or colder
        if value <= 32 and value is not None:
            self.track_heater_display.setText("Active")
        else:
            self.track_heater_display.setText("Inactive")
            
               
    # train model signal slots 
    def receive_train_model_signals(self):
        self.receive_distance_from_yard(self.train_id,self.distance_from_yard_receive)
        self.receive_passengers(self.train_id,self.new_passengers)

    def receive_distance_from_yard(self, train_id, distance_yard):
        for train in self.active_trains_instance_copy.active_trains:
            if int(train.train_ID) == train_id:
                # Handle the received distance from yard signal
                train.distance_from_yard = distance_yard

    def receive_passengers(self,train_id,new_passengers):
        for train in self.active_trains_instance_copy.active_trains:
            if int(train.train_ID) == train_id:
                # handle the new passengers signal
                train.passenger_count = new_passengers
    
    # sends updates from track model backend to main backend
    def send_main_backend_update(self):
        signals.track_model_backend_update.emit(self.track_instance_copy)
    
   # Calculates block occupancy
    def block_occupancy(self):
        # only attempt to calculate occupancy if track model has been loaded
        if len(self.green_line_data) > 0 and len(self.red_line_data) > 0:
            # loop through all active trains and update all occupancies
            for active_train in self.active_trains_instance_copy.active_trains:
                if self.line_name == 'Green Line':
                    # path around track (170 blocks)
                    path = [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
		                82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84,
		                83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
		                112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
                        129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145,
                        146, 147, 148, 149, 150, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15,
                        14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 13, 14, 15, 16, 17, 18, 19, 20, 21,
                        22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
                        43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
            
                    stations = [2,9,16,22,31,39,48,56,65,73,88,96,105,114,123,132,141]
                    
                    undergrounds = [36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,122,123,
                    124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143] 
                    
                    block_length_sum = 0
                    count = 0
                    obj = self.green_line_data[path[count]]
                    block = obj[2]
                    while count < len(path):
                        block_length_sum += int(self.green_line_data[block][3])
                        if(active_train.distance_from_yard-block_length_sum <= 30 and active_train.distance_from_yard != 0):
                            # position found
                            self.set_block_color(path[count],path[count-1])
                            self.track_instance_copy.lines[1].blocks[path[count]].block_occupancy = True
                            
                            # send signals for block grade and speed limit to train model
                            signals.track_model_block_grade.emit(int(active_train.train_ID),self.green_line_data[block][4])
                            signals.track_model_speed_limit.emit(int(active_train.train_ID),self.green_line_data[block][5])
                            
                            for station_block in stations:
                                if path[count] == station_block:
                                    # call function
                                    self.passenger_movement(active_train)
                                    # station block is occupied, send beacon signal and update passenger count
                                    signals.track_model_beacon.emit(int(active_train.train_ID),self.beacon(path[count]))
                            
                            for underground_block in undergrounds:
                                if path[count] == underground_block:
                                    # train is underground, send signal for lights
                                    signals.track_model_underground.emit(int(active_train.train_ID),True)
                                else:
                                    signals.track_model_underground.emit(int(active_train.train_ID),False)
                            
                            break

                        count += 1
            
                if self.line_name == 'Red Line':
                    # path around track (106 blocks)
                    path = [9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                        33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 
                        58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46, 45, 44, 67, 68, 69, 70, 71, 38, 37,
                        36, 35, 34, 33, 72, 73, 74, 75, 76, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 1, 2, 3, 4, 5, 
                        6, 7, 8, 9]
                    
                    stations = [7,17,21,25,35,45,48,60]
                    
                    undergrounds = [24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]
                    
                    block_length_sum = 0
                    count = 0
                    obj = self.red_line_data[path[count]]
                    block = obj[2]
                    
                    while count < len(path):
                        block_length_sum += int(self.red_line_data[block][3])
                        if(active_train.distance_from_yard-block_length_sum <= 30 and active_train.distance_from_yard != 0):
                            # position found
                            self.set_block_color(path[count],path[count-1])
                            self.track_instance_copy.lines[0].blocks[path[count]].block_occupancy = True
                            
                            # send signals for block grade and speed limit to train model
                            signals.track_model_block_grade.emit(int(active_train.train_ID),self.red_line_data[block][4])
                            signals.track_model_speed_limit.emit(int(active_train.train_ID),self.red_line_data[block][5])
                            
                            for station_block in stations:
                                if path[count] == station_block:
                                    # call function
                                    self.passenger_movement(active_train)
                                    # station block is occupied, send beacon signal and update passenger count
                                    signals.track_model_beacon.emit(int(active_train.train_ID),self.beacon(path[count]))
                            
                            for underground_block in undergrounds:
                                if path[count] == underground_block:
                                    # train is underground, send signal for lights
                                    signals.track_model_underground.emit(int(active_train.train_ID),True)
                                else:
                                    signals.track_model_underground.emit(int(active_train.train_ID),False)
                            
                            break
                        
                            
                        count += 1
                
        else:
            pass
    
    # beacon function
    def beacon(self,block_number):
        # beacon format: station name, station side, blocks to next station, blocks to underground 
        if self.line_name == 'Green Line':
            stations = [2,9,16,22,31,39,48,56,65,73,88,96,105,114,123,132,141]
            undergrounds = [36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,122,123,
            124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143] 
            
            # initialize blocks to next station and underground
            blocks_to_station = 100 
            blocks_to_underground = 100

            if block_number in stations:
                # block is a station, find next station
                for i in range(block_number+1, max(stations)+1):
                    if i in stations and i != block_number:
                        blocks_to_station = i - block_number
                        break
            
            if block_number in undergrounds:
                # block is underground, set blocks to itself as 0
                blocks_to_underground = 0
            else:
                # block not underground, find distance to next underground
                for i in range(block_number + 1, max(undergrounds) + 1):
                    if i in undergrounds:
                        blocks_to_underground = i - block_number
                        break
            
            # format beacon string
            if blocks_to_underground == 0:
                beacon = "{} {} {} {}".format(self.green_line_data[block_number][6][22:40],self.green_line_data[block_number][7],blocks_to_station,blocks_to_underground)
            else:
                beacon = "{} {} {} {}".format(self.green_line_data[block_number][6][9:20],self.green_line_data[block_number][7],blocks_to_station, blocks_to_underground)
            return beacon
        
        if self.line_name == 'Red Line':
            stations = [7,17,21,25,35,45,48,60]
            undergrounds = [24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]

            # initialize blocks to next station and underground
            blocks_to_station = 100
            blocks_to_underground = 100
            
            if block_number in stations:
                # block is a station, find next station
                for i in range(block_number+1, max(stations)+1):
                    if i in stations and i != block_number:
                        blocks_to_station = i-block_number
                        break
            
            if block_number in undergrounds: 
                # block is underground, set blocks to itself as 0
                blocks_to_underground = 0
            else: 
                # block is not underground, find distance to next underground
                for i in range(block_number + 1, max(undergrounds) + 1):
                    if i in undergrounds: 
                        blocks_to_underground = i - block_number
                        break
            
            blocks_to_station = blocks_to_station
            blocks_to_underground = blocks_to_underground
            
             # format beacon string
            if blocks_to_underground == 0:
                beacon = "{} {} {} {}".format(self.red_line_data[block_number][6][22:40],self.red_line_data[block_number][7],blocks_to_station,blocks_to_underground)
            else:
                beacon = "{} {} {} {}".format(self.red_line_data[block_number][6][9:20],self.red_line_data[block_number][7],blocks_to_station, blocks_to_underground)
            return beacon

    def set_block_color(self,occupied_block,prev_block):
        scene = self.graphicsView.scene()
        for item in scene.items():
            if isinstance(item,QtWidgets.QGraphicsRectItem):
                # make occupied block red on map
                if str(item.toolTip()) == str(occupied_block):
                    item.setBrush(QtGui.QColor(255,0,0))
                # put prev block back to green 
                if str(item.toolTip()) == str(prev_block):
                    item.setBrush(QtGui.QColor(0,128,0))
                    self.track_instance_copy.lines[1].blocks[prev_block].block_occupancy = False
        
    # update occupancy of yard to show if train has been dispatched             
    def yard_occupancy(self):
        if self.line_name == 'Green Line':
            if self.track_instance_copy.lines[1].blocks[0].block_occupancy == True:
                self.set_block_color(0,None)
            else:
                self.set_block_color(None,0)

        if self.line_name == 'Red Line':
            if self.track_instance_copy.lines[0].blocks[0].block_occupancy == True:
                self.set_block_color(0,None)
            else:
                self.set_block_color(None,0)
        
                        
    def set_crossing_light(self):
        scene = self.graphicsView.scene()
        for item in scene.items():
            if isinstance(item,QtWidgets.QGraphicsEllipseItem):
                if item.toolTip().startswith('crossing'):
                    block_number = int(item.toolTip().replace('crossing',''))

                    # check if the block has an active crossing status
                    if self.line_name == 'Red Line':
                        if self.track_instance_copy.lines[0].blocks[block_number].crossing_status:
                            # make crossing light orange
                            item.setBrush(QtGui.QColor(255, 165, 0))
                        else:
                            # revert back to white
                            item.setBrush(QtGui.QColor(255, 255, 255))
                    if self.line_name == 'Green Line':
                        if self.track_instance_copy.lines[1].blocks[block_number].crossing_status:
                            # make crossing block orange
                            item.setBrush(QtGui.QColor(255, 165, 0))
                        else:
                            # revert back to white
                            item.setBrush(QtGui.QColor(255, 255, 255))


    def set_light_color(self):
        scene = self.graphicsView.scene()
        for item in scene.items():
            if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                # Check if the item is a traffic light (adjust the condition as needed)
                if item.toolTip().startswith('light'):
                    block_number = int(item.toolTip().replace('light',''))
                    if self.line_name == 'Red Line':
                        light_color = self.track_instance_copy.lines[0].blocks[block_number].traffic_light_color
                        # change given light to green
                        if light_color == 1:
                            item.setBrush(QtGui.QColor(0, 128, 0))
                        # change given light to red
                        elif light_color == 0:
                            item.setBrush(QtGui.QColor(255, 0, 0))
                    
                    if self.line_name == 'Green Line':
                        light_color = self.track_instance_copy.lines[1].blocks[block_number].traffic_light_color
                        # change given light to green
                        if light_color == 1:
                            item.setBrush(QtGui.QColor(0, 128, 0))
                        # change given light to red
                        elif light_color == 0:
                            item.setBrush(QtGui.QColor(255, 0, 0))

    def tickets(self):
        # generate ticket sales for entire line 
        if self.line_name == 'Red Line':
            station_count = 8
            # set lower and upper limits for sales numbers
            lower_limit = station_count # number of stations, so minimum 1 sale per station
            upper_limit = 1000
            
            # generate random number of ticket sales for red line
            self.red_sales = random.randint(lower_limit,upper_limit)
            
            if self.red_sales is not None:
                # send ctc the ticket sales 
                signals.track_model_red_line_ticket_sales.emit(self.red_sales)
            
            # obtain ticket sales number for each station of red line
            self.tickets_sold = int(self.red_sales / station_count)
        
        if self.line_name == 'Green Line':
            station_count = 18
            # set lower and upper limits for sales numbers
            lower_limit = station_count # number of stations, so minimum 1 sale per station
            upper_limit = 1000
            
            # generate random number of ticket sales for green line
            self.green_sales = random.randint(lower_limit,upper_limit)
            
            # obtain ticket sales number for each station of green line
            self.tickets_sold = int(self.green_sales / station_count)
        
            if self.green_sales is not None: 
                # send ctc the ticket sales
                signals.track_model_green_line_ticket_sales.emit(self.green_sales)
            
    def passenger_movement(self,active_train):
        lower_limit = 0 
        upper_limit = self.tickets_sold 
                                        
        # generate passenger movement for train on red line
        passengers_on = random.randint(lower_limit,upper_limit)
        passengers_off = random.randint(lower_limit,active_train.passenger_count)
                                    
        send_passengers = active_train.passenger_count + (passengers_on - passengers_off)
        active_train.passenger_count = send_passengers
        signals.track_model_send_passengers.emit(int(active_train.train_ID),send_passengers)
                               
        # display passengers on and off in sidebar
        self.passengers_boarding_display.setText(str(passengers_on))
        self.passengers_disembarking_display.setText(str(passengers_off))

    def track_layout(self):
        file_filter = 'Excel File (*.xlsx)'
        response, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption = 'Select a Track Layout',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Execl File (*.xlsx)',
        )
        
        # parse layout file
        layout_data = openpyxl.load_workbook(response, data_only=True) # open workbook and extract data only (take result from cells with formulas)
        
        # assign sheets to sheet names from the file
        sheet3 = layout_data['Red Line']
        sheet4 = layout_data['Green Line']
        
        
        # iterate through to extract data
        for row in sheet3.iter_rows(min_row=2, max_row=78, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time = row[:11]
            
            self.red_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time))
            
        
        for row in sheet4.iter_rows(min_row=2,max_row=152, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time = row[:11]
            
            self.green_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time))
        
        # enable line selection after track layout is loaded 
        self.LineSelectHint.setVisible(False)
        self.TrackLineColorValue.setEnabled(True)
        
    
    def mousePressEvent(self,e: QtGui.QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            pos = e.pos()
            items = self.graphicsView.items(pos)
            for item in items:
                if isinstance(item,QtWidgets.QGraphicsRectItem):
                    block_number = str(item.toolTip())
                    self.clicked_block = block_number
                    self.display_block_info()
                    break
                
    def display_block_info(self):
        block_number = self.clicked_block
        if self.line_name == 'Green Line':
            for data in self.green_line_data:
                if data[2] == int(block_number):  
                    # display currently selected block number
                    self.block_number_display.setText(str(data[2]))
                    if data[3] is not None:
                        # if block is not the yard, display block length and block grade with appropriate conversions
                        self.block_length_display.setText("{:.2f}".format(data[3] * 3.281))
                        self.block_grade_display.setText(str(data[4]))
                    if data[5] is not None:
                        # display speed limit and traffic light status 
                        self.speed_limit_display.setText("{:.2f}".format(data[5] / 1.609))
                        self.traffic_light_display.setText(self.track_instance_copy.lines[1].blocks[int(block_number)].get_traffic_light_color_string())
                    if data[6] is not None:
                        # display infrastructure
                        self.infrastructure_display.setText(str(data[6][0:7]))
                        if str(data[6][0:7]) == 'STATION':
                            # if infrastructure is station, display station name and ticket sales 
                            self.station_name_display.setText(str(data[6][9:20]))
                            self.tickets_sold_display.setText(str(self.tickets_sold))
                            # TODO display remainder of station info (passengers boarding and disembarking)
                            # display beacon data (if applicable)
                            self.beacon_display.setText(self.beacon(int(block_number)))
                            #print(self.beacon_display.setText(self.beacon(int(block_number))))
                        else: 
                            # do not display ticket sales or beacon if block is not a station
                            self.tickets_sold_display.setText("None")
                            self.beacon_display.setText("None")
                        if str(data[6][0:6]) == 'SWITCH' or str(data[6]) == 'UNDERGROUND':
                            # if block is switch or underground display infrastructure, do not display a station name
                            self.infrastructure_display.setText(str(data[6]))
                            self.station_name_display.setText('')
                        if str(data[6][0:20]) == 'UNDERGROUND; STATION':
                            self.infrastructure_display.setText(str(data[6][0:20]))
                            self.station_name_display.setText(str(data[6][22:40]))
                            # display beacon data
                            self.beacon_display.setText(self.beacon(int(block_number)))
                        if str(data[6]) == 'RAILWAY CROSSING':
                            self.infrastructure_display.setText(str(data[6]))
                    else:
                        self.infrastructure_display.setText(str(data[6]))
                        self.station_name_display.setText(str(data[6]))
                        self.tickets_sold_display.setText(str(data[6]))
                        self.passengers_boarding_display.setText(str(data[6]))
                        self.passengers_disembarking_display.setText(str(data[6]))
                    self.switch_direction_display.setText(self.track_instance_copy.lines[1].blocks[int(block_number)].get_switch_direction_string(1))
                    
                    # display crossing status in sidebar 
                    self.crossing_status_display.setText(self.track_instance_copy.lines[1].blocks[int(block_number)].get_crossing_status_string()) 
                        
                    if data[8] is not None and data[9] is not None:
                        self.elevation_display.setText("{:.2f}".format(data[8] * 3.281))
                        self.cum_elevation_display.setText("{:.2f}".format(data[9] * 3.281))
                    
                    # display train info (only if block is occupied)
                    for active_train in self.active_trains_instance_copy.active_trains:
                        if active_train.current_block == int(block_number):
                            self.train_ID_display.setText(str(active_train.train_ID))
                            
                            if active_train.current_direction:
                                self.direction_of_travel_display.setText("Northbound")
                            else:
                                self.direction_of_travel_display.setText("Southbound")
                                    
                            self.authority_display.setText(str(active_train.current_authority))
                            self.current_speed_display.setText(str(active_train.current_suggested_speed))
                        
                        else: 
                            self.train_ID_display.setText("None")
                            self.direction_of_travel_display.setText("None")
                            self.authority_display.setText("None")
                            self.current_speed_display.setText("None")
                    
                    
        if self.line_name == 'Red Line':
            for data in self.red_line_data:
                if data[2] == int(block_number):  
                    self.block_number_display.setText(str(data[2]))
                    if data[3] is not None:
                        self.block_length_display.setText("{:.2f}".format(data[3] * 3.281))
                    self.block_grade_display.setText(str(data[4]))
                    if data[5] is not None:
                        self.speed_limit_display.setText("{:.2f}".format(data[5] / 1.609))
                    self.traffic_light_display.setText(self.track_instance_copy.lines[0].blocks[int(block_number)].get_traffic_light_color_string())
                    if data[6] is not None:
                        self.infrastructure_display.setText(str(data[6][0:7]))
                        if str(data[6][0:7]) == 'STATION':
                            self.station_name_display.setText(str(data[6][9:30]))
                            self.tickets_sold_display.setText(str(self.tickets_sold))
                            # TODO display remainder of station info (passengers boarding and disembarking)
                            # display beacon info for given station
                            self.beacon_display.setText(self.beacon(int(block_number)))
                        else:
                            self.tickets_sold_display.setText('')
                        if str(data[6][0:6]) == 'SWITCH' or str(data[6]) == 'UNDERGROUND':
                            self.infrastructure_display.setText(str(data[6]))
                            self.station_name_display.setText('')
                        if str(data[6][0:20]) == 'UNDERGROUND; STATION':
                            self.infrastructure_display.setText(str(data[6][0:20]))
                            self.station_name_display.setText(str(data[6][22:40]))
                            # display beacon data
                            self.beacon_display.setText(self.beacon(int(block_number)))
                        if str(data[6]) == 'RAILWAY CROSSING':
                            self.infrastructure_display.setText(str(data[6]))
                    else:
                        self.infrastructure_display.setText(str(data[6]))
                        self.station_name_display.setText(str(data[6]))
                        self.tickets_sold_display.setText(str(data[6]))
                        self.passengers_boarding_display.setText(str(data[6]))
                        self.passengers_disembarking_display.setText(str(data[6]))
                        self.beacon_display.setText(str(data[6]))
                    
                    # display active switch direction in sidebar
                    self.switch_direction_display.setText(self.track_instance_copy.lines[0].blocks[int(block_number)].get_switch_direction_string(0))
                    
                    # display crossing status in sidebar
                    self.crossing_status_display.setText(self.track_instance_copy.lines[0].blocks[int(block_number)].get_crossing_status_string()) 
                    
                    if data[8] is not None and data[9] is not None:
                        self.elevation_display.setText("{:.2f}".format(data[8] * 3.281))
                        self.cum_elevation_display.setText("{:.2f}".format(data[9] * 3.281))
                    
                    # display train info (only if block is occupied)
                    '''
                    if self.track_instance_copy.lines[0].blocks[int(block_number)].block_occupancy:
                        self.train_ID_display.setText(str(self.active_trains_instance_copy.active_trains[self.train_id].train_ID))
                        
                        if self.active_trains_instance_copy.active_trains[self.train_id].current_direction:
                            self.direction_of_travel_display.setText("Northbound")
                        else:
                            self.direction_of_travel_display.setText("Southbound")
                        self.authority_display.setText(str(self.active_trains_instance_copy.active_trains[self.train_id].current_authority))
                        self.current_speed_display.setText(str(self.active_trains_instance_copy.active_trains[self.train_id].current_suggested_speed))
                    
                    else: 
                        self.train_ID_display.setText("None")
                        self.direction_of_travel_display.setText("None")
                        self.authority_display.setText("None")
                        self.current_speed_display.setText("None")
                    '''
                    
        
    def build_track_map(self):
        self.graphicsView.scene().clear()
        self.line_name = self.TrackLineColorValue.currentText()

        # generate ticket sales
        self.tickets()
        
        if self.line_name == 'Red Line':
            
            # place the yard block and go from there
            block0 = QtWidgets.QGraphicsRectItem(850,30,20,20)
            block0.setBrush(QtGui.QColor(128,128,128)) # gray color for yard block 
            block0.setToolTip(str(0))
            self.graphicsView.scene().addItem(block0)
            
            # add label to yard 
            text = QtWidgets.QGraphicsTextItem('Yard')
            text.setPos(843,50)
            self.graphicsView.scene().addItem(text)
            
            # use function to keep building map
            self.add_block_to_map(860,-50,20,'block9','9','right',850,30)
            self.add_block_to_map(820,-30,20,'block10','10','bottom',860,-50)
            self.add_block_to_map(790,-30,20,'block11','11','bottom',820,-30)
            self.add_block_to_map(750,-30,20,'block12','12','bottom',790,-30)
            self.add_block_to_map(710,-30,20,'block13','13','bottom',750,-30)
            self.add_block_to_map(670,-30,20,'block14','14','bottom',710,-30)
            self.add_block_to_map(630,-30,20,'block15','15','bottom',670,-30)
            self.add_block_to_map(590,-30,20,'block16','16','bottom',630,-30)
            self.add_block_to_map(610,-60,20,'block1','1','top',590,-30)
            self.add_block_to_map(640,-70,20,'block2','2','top',610,-60)
            self.add_block_to_map(670,-80,20,'block3','3','top',640,-70)
            self.add_block_to_map(700,-90,20,'block4','4','top',670,-80)
            self.add_block_to_map(730,-100,20,'block5','5','top',700,-90)
            self.add_block_to_map(760,-110,20,'block6','6','top',730,-100)
            self.add_block_to_map(810,-110,20,'block7','7','top',760,-110)
            self.add_block_to_map(850,-95,20,'block8','8','right',810,-110)
            
            # connect blocks 8 and 9
            line = QtWidgets.QGraphicsLineItem(860,-75,870,-50)
            line.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line)
            
            # continue building track map 
            self.add_block_to_map(565,-30,20,'block17','17','top',590,-30)
            self.add_block_to_map(540,-30,20,'block18','18','top',565,-30)
            self.add_block_to_map(515,-30,20,'block19','19','top',540,-30)
            self.add_block_to_map(490,-30,20,'block20','20','top',515,-30)
            self.add_block_to_map(465,-30,20,'block21','21','top',490,-30)
            self.add_block_to_map(440,-10,20,'block22','22','top',465,-30)
            self.add_block_to_map(440,15,20,'block23','23','right',440,-10)
            self.add_block_to_map(440,40,20,'block24','24','right',440,15)
            self.add_block_to_map(440,65,20,'block25','25','right',440,40)
            self.add_block_to_map(440,90,20,'block26','26','right',440,65)
            self.add_block_to_map(440,115,20,'block27','27','right',440,90)
            self.add_block_to_map(440,140,20,'block28','28','right',440,115)
            self.add_block_to_map(440,165,20,'block29','29','right',440,140)
            self.add_block_to_map(440,190,20,'block30','30','right',440,165)
            self.add_block_to_map(440,215,20,'block31','31','right',440,190)
            self.add_block_to_map(440,240,20,'block32','32','right',440,215)
            self.add_block_to_map(440,265,20,'block33','33','right',440,240)
            self.add_block_to_map(440,290,20,'block34','34','right',440,265)
            self.add_block_to_map(440,315,20,'block35','35','right',440,290)
            self.add_block_to_map(440,340,20,'block36','36','right',440,315)
            self.add_block_to_map(440,365,20,'block37','37','right',440,340)
            self.add_block_to_map(440,390,20,'block38','38','right',440,365)
            self.add_block_to_map(440,415,20,'block39','39','right',440,390)
            self.add_block_to_map(440,440,20,'block40','40','right',440,415)
            self.add_block_to_map(440,465,20,'block41','41','right',440,440)
            self.add_block_to_map(440,490,20,'block42','42','right',440,465)
            self.add_block_to_map(440,515,20,'block43','43','right',440,490)
            self.add_block_to_map(440,540,20,'block44','44','right',440,515)
            self.add_block_to_map(440,565,20,'block45','45','right',440,540)
            self.add_block_to_map(430,587,20,'block46','46','right',440,565)
            self.add_block_to_map(415,610,20,'block47','47','right',430,587)
            self.add_block_to_map(395,633,20,'block48','48','right',415,610)
            self.add_block_to_map(375,655,20,'block49','49','right',395,633)
            self.add_block_to_map(345,655,20,'block50','50','bottom',375,655)
            self.add_block_to_map(315,655,20,'block51','51','bottom',345,655)
            self.add_block_to_map(285,655,20,'block52','52','bottom',315,655)
            self.add_block_to_map(255,655,20,'block53','53','bottom',285,655)
            self.add_block_to_map(225,655,20,'block54','54','bottom',255,655)
            self.add_block_to_map(185,645,20,'block55','55','bottom',225,655)
            self.add_block_to_map(155,615,20,'block56','56','left',185,645)
            self.add_block_to_map(135,590,20,'block57','57','left',155,615)
            self.add_block_to_map(135,560,20,'block58','58','left',135,590)
            self.add_block_to_map(145,530,20,'block59','59','left',135,560)
            self.add_block_to_map(155,500,20,'block60','60','top',145,530)
            self.add_block_to_map(177,520,20,'block61','61','top',155,500)
            self.add_block_to_map(199,540,20,'block62','62','top',177,520)
            self.add_block_to_map(221,560,20,'block63','63','top',199,540)
            self.add_block_to_map(243,580,20,'block64','64','top',221,560)
            self.add_block_to_map(265,600,20,'block65','65','top',243,580)
            self.add_block_to_map(287,620,20,'block66','66','top',265,600)

            # connect blocks 66 and 52
            line = QtWidgets.QGraphicsLineItem(297,640,295,655)
            line.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line)
            
            # add side pass 1 (blocks 76 through 72)
            self.add_block_to_map(410,130,20,'block76','76','top',440,115)
            self.add_block_to_map(380,145,20,'block75','75','left',410,130)
            self.add_block_to_map(380,190,20,'block74','74','left',380,145)
            self.add_block_to_map(380,235,20,'block73','73','left',380,190)
            self.add_block_to_map(410,250,20,'block72','72','bottom',380,235)
            
            # connect blocks 72 and 33
            line = QtWidgets.QGraphicsLineItem(430,260,440,275)
            line.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line)
            
            # add side pass 2 (blocks 71 through 67)
            self.add_block_to_map(410,405,20,'block71','71','top',440,390)
            self.add_block_to_map(380,420,20,'block70','70','left',410,405)
            self.add_block_to_map(380,465,20,'block69','69','left',380,420)
            self.add_block_to_map(380,510,20,'block68','68','left',380,465)
            self.add_block_to_map(410,525,20,'block67','67','bottom',380,510)
            
            # connect blocks 67 and 44
            line = QtWidgets.QGraphicsLineItem(430,535,440,550)
            line.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line)
            
            # add traffic lights
            self.add_light_to_map(850,-50,'light9')
            self.add_light_to_map(820,-40,'light10')
            self.add_light_to_map(870,40,'light0')
            
            self.add_light_to_map(640,-40,'light15')
            self.add_light_to_map(620,-70,'light1')
            self.add_light_to_map(585,-10,'light16')
            
            self.add_light_to_map(430,110,'light27')
            self.add_light_to_map(410,150,'light76')
            self.add_light_to_map(460,157,'light28')
            
            self.add_light_to_map(430,385,'light38')
            self.add_light_to_map(410,425,'light71')
            self.add_light_to_map(460,432,'light39')
            
            self.add_light_to_map(410,240,'light72')
            self.add_light_to_map(430,240,'light32')
            self.add_light_to_map(460,282,'light33')
            
            self.add_light_to_map(430,515,'light43')
            self.add_light_to_map(410,515,'light67')
            self.add_light_to_map(460,558,'light44')
            
            self.add_light_to_map(298,645,'light52')
            self.add_light_to_map(250,675,'light53')
            self.add_light_to_map(275,620,'light66')
            
            # place crossing light
            red_crossing = QtWidgets.QGraphicsEllipseItem(405,615,10,10)  # (x, y, width, height)
            red_crossing.setBrush(QtGui.QColor(255,255,255))  # white color by default for inactive crossing
            self.graphicsView.scene().addItem(red_crossing)
            red_crossing.setToolTip("crossing47")

        elif self.line_name == 'Green Line':
            # place the yard block 
            block0 = QtWidgets.QGraphicsRectItem(900,100,20,20)
            block0.setBrush(QtGui.QColor(128,128,128)) # gray color for yard block 
            block0.setToolTip(str(0))
            self.graphicsView.scene().addItem(block0)
            
            # add label to yard 
            text = QtWidgets.QGraphicsTextItem('Yard')
            text.setPos(892,80)
            self.graphicsView.scene().addItem(text)
            
            # continue building map using function 
            self.add_block_to_map(900,250,20,'block63','63','right',900,100)
            self.add_block_to_map(900,290,20,'block64','64','right',900,250)
            self.add_block_to_map(900,330,20,'block65','65','right',900,290)
            self.add_block_to_map(900,370,20,'block66','66','right',900,330)
            self.add_block_to_map(900,410,20,'block67','67','right',900,370)
            self.add_block_to_map(900,450,20,'block68','68','right',900,410)
            self.add_block_to_map(900,490,20,'block69','69','right',900,450)
            self.add_block_to_map(900,530,20,'block70','70','right',900,490)
            self.add_block_to_map(900,570,20,'block71','71','right',900,530)
            self.add_block_to_map(900,610,20,'block72','72','right',900,570)
            self.add_block_to_map(850,640,20,'block73','73','bottom',900,610)
            self.add_block_to_map(800,640,20,'block74','74','bottom',850,640)
            self.add_block_to_map(750,640,20,'block75','75','bottom',800,640)
            self.add_block_to_map(700,640,20,'block76','76','bottom',750,640)
            self.add_block_to_map(650,640,20,'block77','77','bottom',700,640)
            self.add_block_to_map(600,640,20,'block78','78','bottom',650,640)
            self.add_block_to_map(550,640,20,'block79','79','bottom',600,640)
            self.add_block_to_map(500,640,20,'block80','80','bottom',550,640)
            self.add_block_to_map(450,640,20,'block81','81','bottom',500,640)
            self.add_block_to_map(400,640,20,'block82','82','bottom',450,640)
            self.add_block_to_map(350,640,20,'block83','83','bottom',400,640)
            self.add_block_to_map(300,640,20,'block84','84','bottom',350,640)
            self.add_block_to_map(250,640,20,'block85','85','bottom',300,640)
            self.add_block_to_map(200,640,20,'block86','86','bottom',250,640)
            self.add_block_to_map(150,640,20,'block87','87','bottom',200,640)
            self.add_block_to_map(100,640,20,'block88','88','bottom',150,640)
            self.add_block_to_map(65,620,20,'block89','89','bottom',100,640)
            self.add_block_to_map(50,590,20,'block90','90','left',65,620)
            self.add_block_to_map(35,560,20,'block91','91','left',50,590)
            self.add_block_to_map(35,530,20,'block92','92','left',35,560)
            self.add_block_to_map(35,500,20,'block93','93','left',35,530)
            self.add_block_to_map(50,470,20,'block94','94','left',35,500)
            self.add_block_to_map(65,440,20,'block95','95','left',50,470)
            self.add_block_to_map(80,410,20,'block96','96','left',65,440)
            self.add_block_to_map(120,410,20,'block97','97','top',80,410)
            self.add_block_to_map(160,470,20,'block98','98','top',120,410)
            self.add_block_to_map(200,530,20,'block99','99','top',160,470)
            self.add_block_to_map(240,590,20,'block100','100','top',200,530)

            # connect blocks 85 and 100
            line = QtWidgets.QGraphicsLineItem(250,610,260,640)
            line.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line)
            
            # place more blocks 
            self.add_block_to_map(680,580,20,'block101','101','left',650,640)
            self.add_block_to_map(720,580,20,'block102','102','top',680,580)
            self.add_block_to_map(760,580,20,'block103','103','top',720,580)
            self.add_block_to_map(800,580,20,'block104','104','top',760,580)
            self.add_block_to_map(840,560,20,'block105','105','bottom',800,580)
            self.add_block_to_map(840,535,20,'block106','106','left',840,560)
            self.add_block_to_map(840,510,20,'block107','107','left',840,535)
            self.add_block_to_map(840,485,20,'block108','108','left',840,510)
            self.add_block_to_map(840,460,20,'block109','109','left',840,485)
            self.add_block_to_map(840,435,20,'block110','110','left',840,460)
            self.add_block_to_map(840,410,20,'block111','111','left',840,435)
            self.add_block_to_map(840,385,20,'block112','112','left',840,410)
            self.add_block_to_map(840,360,20,'block113','113','left',840,385)
            self.add_block_to_map(840,335,20,'block114','114','left',840,360)
            self.add_block_to_map(840,310,20,'block115','115','left',840,335)
            self.add_block_to_map(840,285,20,'block116','116','left',840,310)
            self.add_block_to_map(840,260,20,'block117','117','left',840,285)
            self.add_block_to_map(840,235,20,'block118','118','left',840,260)
            self.add_block_to_map(820,210,20,'block119','119','left',840,235)
            self.add_block_to_map(800,185,20,'block120','120','right',820,210)
            self.add_block_to_map(780,160,20,'block121','121','right',800,185)
            self.add_block_to_map(755,160,20,'block122','122','bottom',780,160)
            self.add_block_to_map(880,225,20,'block62','62','right',900,250)
            self.add_block_to_map(860,200,20,'block61','61','right',880,225)
            self.add_block_to_map(845,175,20,'block60','60','right',860,200)
            self.add_block_to_map(825,150,20,'block59','59','right',845,175)
            self.add_block_to_map(805,125,20,'block58','58','right',825,150)
            self.add_block_to_map(785,100,20,'block57','57','top',805,125)
            self.add_block_to_map(760,100,20,'block56','56','top',785,100)
            self.add_block_to_map(735,100,20,'block55','55','top',760,100)
            self.add_block_to_map(710,100,20,'block54','54','top',735,100)
            self.add_block_to_map(685,100,20,'block53','53','top',710,100)
            self.add_block_to_map(660,100,20,'block52','52','top',685,100)
            self.add_block_to_map(635,100,20,'block51','51','top',660,100)
            self.add_block_to_map(610,100,20,'block50','50','top',635,100)
            self.add_block_to_map(585,100,20,'block49','49','top',610,100)
            self.add_block_to_map(560,100,20,'block48','48','top',585,100)
            self.add_block_to_map(535,100,20,'block47','47','top',560,100)
            self.add_block_to_map(510,100,20,'block46','46','top',535,100)
            self.add_block_to_map(485,100,20,'block45','45','top',510,100)
            self.add_block_to_map(460,100,20,'block44','44','top',485,100)
            self.add_block_to_map(435,100,20,'block43','43','top',460,100)
            self.add_block_to_map(410,100,20,'block42','42','top',435,100)
            self.add_block_to_map(385,100,20,'block41','41','top',410,100)
            self.add_block_to_map(360,100,20,'block40','40','top',385,100)
            self.add_block_to_map(335,100,20,'block39','39','top',360,100)
            self.add_block_to_map(310,100,20,'block38','38','top',335,100)
            self.add_block_to_map(285,100,20,'block37','37','top',310,100)
            self.add_block_to_map(260,100,20,'block36','36','top',285,100)
            self.add_block_to_map(730,160,20,'block123','123','bottom',755,160)
            self.add_block_to_map(705,160,20,'block124','124','bottom',730,160)
            self.add_block_to_map(680,160,20,'block125','125','bottom',705,160)
            self.add_block_to_map(655,160,20,'block126','126','bottom',680,160)
            self.add_block_to_map(630,160,20,'block127','127','bottom',655,160)
            self.add_block_to_map(605,160,20,'block128','128','bottom',630,160)
            self.add_block_to_map(580,160,20,'block129','129','bottom',605,160)
            self.add_block_to_map(555,160,20,'block130','130','bottom',580,160)
            self.add_block_to_map(530,160,20,'block131','131','bottom',555,160)
            self.add_block_to_map(505,160,20,'block132','132','bottom',530,160)
            self.add_block_to_map(480,160,20,'block133','133','bottom',505,160)
            self.add_block_to_map(455,160,20,'block134','134','bottom',480,160)
            self.add_block_to_map(430,160,20,'block135','135','bottom',455,160)
            self.add_block_to_map(405,160,20,'block136','136','bottom',430,160)
            self.add_block_to_map(380,160,20,'block137','137','bottom',405,160)
            self.add_block_to_map(355,160,20,'block138','138','bottom',380,160)
            self.add_block_to_map(330,160,20,'block139','139','bottom',355,160)
            self.add_block_to_map(305,160,20,'block140','140','bottom',330,160)
            self.add_block_to_map(280,160,20,'block141','141','bottom',305,160)
            self.add_block_to_map(255,160,20,'block142','142','bottom',280,160)
            self.add_block_to_map(230,160,20,'block143','143','bottom',255,160)
            self.add_block_to_map(205,160,20,'block144','144','bottom',230,160)
            self.add_block_to_map(235,90,20,'block35','35','bottom',260,100)
            self.add_block_to_map(210,80,20,'block34','34','bottom',235,90)
            self.add_block_to_map(185,70,20,'block33','33','bottom',210,80)
            self.add_block_to_map(160,60,20,'block32','32','bottom',185,70)
            self.add_block_to_map(160,35,20,'block31','31','right',160,60)
            self.add_block_to_map(160,10,20,'block30','30','right',160,35)
            self.add_block_to_map(160,-15,20,'block29','29','right',160,10)
            self.add_block_to_map(165,140,20,'block145','145','bottom',205,160)
            self.add_block_to_map(125,120,20,'block146','146','bottom',165,140)
            self.add_block_to_map(85,100,20,'block147','147','bottom',125,120)
            self.add_block_to_map(85,60,20,'block148','148','left',85,100)
            self.add_block_to_map(85,20,20,'block149','149','left',85,60)
            self.add_block_to_map(85,-15,20,'block150','150','left',85,20)
            self.add_block_to_map(122,-35,20,'block28','28','right',85,-15)
            
            # add both lines for junction
            line = QtWidgets.QGraphicsLineItem(160,-5,132,-15)
            line.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line)
            
            line = QtWidgets.QGraphicsLineItem(105,-5,132,-15)
            line.setPen(QtGui.QColor(255,255,255))
            self.graphicsView.scene().addItem(line)
            
            # continue adding blocks
            self.add_block_to_map(122,-56,20,'block27','27','right',122,-35)
            self.add_block_to_map(122,-77,20,'block26','26','right',122,-56)
            self.add_block_to_map(122,-98,20,'block25','25','right',122,-77)
            self.add_block_to_map(122,-119,20,'block24','24','right',122,-98)
            self.add_block_to_map(122,-140,20,'block23','23','right',122,-119) 
            self.add_block_to_map(122,-161,20,'block22','22','right',122,-140)
            self.add_block_to_map(122,-182,20,'block21','21','left',122,-161)
            self.add_block_to_map(132,-203,20,'block20','20','left',122,-182)
            self.add_block_to_map(182,-203,20,'block19','19','bottom',132,-203)
            self.add_block_to_map(232,-203,20,'block18','18','bottom',182,-203)
            self.add_block_to_map(282,-203,20,'block17','17','bottom',232,-203)
            self.add_block_to_map(332,-203,20,'block16','16','bottom',282,-203)
            self.add_block_to_map(382,-203,20,'block15','15','bottom',332,-203)
            self.add_block_to_map(432,-203,20,'block14','14','bottom',382,-203)
            self.add_block_to_map(482,-203,20,'block13','13','bottom',432,-203)
            self.add_block_to_map(532,-203,20,'block12','12','bottom',482,-203)
            self.add_block_to_map(582,-203,20,'block11','11','bottom',532,-203)
            self.add_block_to_map(632,-203,20,'block10','10','bottom',582,-203)
            self.add_block_to_map(682,-193,20,'block9','9','top',632,-203)
            self.add_block_to_map(712,-173,20,'block8','8','right',682,-193)
            self.add_block_to_map(682,-153,20,'block7','7','bottom',712,-173)
            self.add_block_to_map(652,-133,20,'block6','6','bottom',682,-153)
            self.add_block_to_map(622,-133,20,'block5','5','bottom',652,-133)
            self.add_block_to_map(592,-133,20,'block4','4','bottom',622,-133)
            self.add_block_to_map(562,-143,20,'block3','3','bottom',592,-133)
            self.add_block_to_map(532,-153,20,'block2','2','bottom',562,-143)
            self.add_block_to_map(502,-163,20,'block1','1','bottom',532,-153)
            
            # connect block 1 to 13
            line = QtWidgets.QGraphicsLineItem(512,-163,492,-183)
            line.setPen(QtGui.QColor(255,255,255))
            self.graphicsView.scene().addItem(line)
            
            # connect yard to block 57
            line = QtWidgets.QGraphicsLineItem(900,110,805,110)
            line.setPen(QtGui.QColor(255,255,255))
            self.graphicsView.scene().addItem(line)
            
            # add traffic lights 
            self.add_light_to_map(515,-175,'light1')
            self.add_light_to_map(475,-185,'light13')
    
            self.add_light_to_map(110,-35,'light28')
            self.add_light_to_map(107,-5,'light150')
            
            self.add_light_to_map(888,95,'light0')
            self.add_light_to_map(785,120,'light57')
            
            self.add_light_to_map(870,235,'light62')
            
            self.add_light_to_map(710,630,'light76')
            self.add_light_to_map(645,660,'light77')
            
            self.add_light_to_map(260,630,'light85')
            self.add_light_to_map(230,600,'light100')
            
            # place crossing light
            green_crossing = QtWidgets.QGraphicsEllipseItem(170,-180,10,10)  # (x, y, width, height)
            green_crossing.setBrush(QtGui.QColor(255,255,255))  # white color by default for inactive crossing
            self.graphicsView.scene().addItem(green_crossing)
            green_crossing.setToolTip("crossing19")

    def add_block_to_map(self,x,y,block_size,block_number,block_number_2,label_pos,prev_x,prev_y):
            block_number = QtWidgets.QGraphicsRectItem(x,y,block_size,block_size)
            block_number.setBrush(QtGui.QColor(0,128,0)) # green color for normal block 
            block_number.setToolTip(str(block_number_2))
            self.graphicsView.scene().addItem(block_number)
            
            # handle different positions for the block label
            if label_pos == 'top' and y<0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x,y-(block_size))
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'top' and y>=0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x,y-(block_size))
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'right':
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x+block_size,y)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'left':
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x-(block_size*1.4),y)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'bottom' and y<0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x,y+block_size)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'bottom' and y>=0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x,y+block_size)
                self.graphicsView.scene().addItem(text)
            
            # draw line to connect blocks with handling for different orientations 
            if(block_number_2 == '28'):
                return
            
            # vertically aligned (negative)
            if (abs(prev_x-x)) <= 20 and y<0: 
                line = QtWidgets.QGraphicsLineItem(prev_x+(block_size/2),prev_y,x+(block_size/2),y+block_size)
                line.setPen(QtGui.QColor(255,255,255)) # white color for lines
                self.graphicsView.scene().addItem(line)
                return
            
            # vertically aligned moving down (positive)
            if (abs(prev_x-x)) <= 20 and y>=0 and y > prev_y: 
                line = QtWidgets.QGraphicsLineItem((x+(block_size/2)),y,prev_x+(block_size/2),prev_y+block_size)
                line.setPen(QtGui.QColor(255,255,255)) # white color for lines
                self.graphicsView.scene().addItem(line)

                return 
            
            # vertically aligned moving upwards
            if (abs(prev_x-x)) <= 10 and y>=0 and prev_y > y:
                line = QtWidgets.QGraphicsLineItem(prev_x+(block_size/2),prev_y,x+(block_size/2),y+block_size)
                line.setPen(QtGui.QColor(255,255,255)) # white color for lines
                self.graphicsView.scene().addItem(line)
                return
            
            if x == prev_x and y>=0:
                line = QtWidgets.QGraphicsLineItem(x+(block_size*(8/3)),y,prev_x+(block_size/2),prev_y+block_size)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            # blocks in line horizontally (right to left)
            if (abs(prev_y-y)) <= 10 and x < prev_x and y<0:
                line = QtWidgets.QGraphicsLineItem(prev_x,prev_y+(block_size/2),x+block_size,y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
                return
            
            # left to right negative y-axis
            if (abs(prev_y-y)) <= 10 and x > prev_x and y<0:
                line = QtWidgets.QGraphicsLineItem(prev_x+block_size,prev_y+(block_size/2),x,y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
                return
             
            if (abs(prev_y-y)) <= 20 and y>=0 and x < prev_x:
                line = QtWidgets.QGraphicsLineItem(x+block_size,y+(block_size/2),prev_x,prev_y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
                return
            
            # blocks in line horizontally going left to right 
            if (abs(prev_y-y)) <= 20 and y>=0 and x > prev_x:
                line = QtWidgets.QGraphicsLineItem(prev_x+block_size,prev_y+(block_size/2),x,y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
                return
            
            # diagonal cases
            # up to the left
            elif x != prev_x and y != prev_y and x<prev_x and y<prev_y:
                line = QtWidgets.QGraphicsLineItem(x+(block_size/2),y+block_size,prev_x,prev_y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            # down to the left
            elif x != prev_x and y != prev_y and x<prev_x and y>prev_y:
                line = QtWidgets.QGraphicsLineItem(prev_x,prev_y+(block_size/2),x+block_size,y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            # down to the right
            elif x != prev_x and y != prev_y and prev_x<x and y>prev_y:
                line = QtWidgets.QGraphicsLineItem(prev_x+block_size,prev_y+(block_size/2),x,y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            # up to the right (negative y-axis)
            elif x != prev_x and y != prev_y and x>prev_x and y<prev_y and y<0:
                line = QtWidgets.QGraphicsLineItem(prev_x+block_size,prev_y+(block_size/2),x,y+(block_size/2))
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
              
            # up to the right (positive y)    
            elif x != prev_x and y != prev_y and x>prev_x and y<prev_y and y>=0:
                line = QtWidgets.QGraphicsLineItem(prev_x+(block_size/2),prev_y,x+(block_size/2),y+block_size)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)

    # function to add traffic lights to map
    def add_light_to_map(self,x,y,light_number):
        light_number_2 = light_number
        light_number = QtWidgets.QGraphicsEllipseItem(x, y, 10, 10)  # (x, y, width, height)
        light_number.setBrush(QtGui.QColor(255,0,0))  # Set red color by default
        self.graphicsView.scene().addItem(light_number)
        light_number.setToolTip(str(light_number_2))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrackModelModule()
    window.show()
    sys.exit(app.exec())