import sys
sys.path.append(".")
import os, openpyxl
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
        
        # member variable to hold selected block 
        self.clicked_block = 0
        
        # member variable to hold occupied block
        self.occupied_block = 0
        self.block_grade = 0
        self.station_name = None
        
        # train model variables
        self.train_length = 0
        self.distance_from_yard = 100
        self.distance_from_block_start = 0
        
        # declare list to store line data
        self.red_line_data = []
        self.green_line_data = []
        
        # receives updates from main backend
        signals.track_model_update_backend.connect(self.backend_update_backend)

        # receive updates from train model
        signals.trainModel_send_train_length.connect(self.receive_train_length)
        signals.trainModel_send_distance_from_block_start.connect(self.receive_distance_from_block_start)
        signals.trainModel_send_distance_from_yard.connect(self.receive_distance_from_yard)
        
        # disable line selector until track is loaded to avoid undefined behavior
        self.TrackLineColorValue.setEnabled(False)
        
        # line color combo box hint behavior, hide hint initially
        self.TrackLineColorValue.installEventFilter(self)
        self.LineSelectHint.setVisible(True)
        
        # load track model button
        self.LoadTrackModelButton.clicked.connect(self.track_layout)
        
        # failure mode handler
        self.TrackCircuitFailureToggleButton.toggled.connect(self.failure_mode)
        self.BrokenRailToggleButton.toggled.connect(self.failure_mode)
        self.PowerFailureToggleButton.toggled.connect(self.failure_mode)

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
        signals.track_model_backend_update.emit(self.track_instance_copy, self.active_trains_instance_copy)
    
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
        self.occupied_block = self.block_occupancy()
        
        # signals to train model
        signals.track_model_block_grade.emit(self.block_grade)
        signals.track_model_beacon.emit(self.station_name)
        
        # send updated signals to main backend
        self.send_main_backend_update()
        
    # failure mode handler
    def failure_mode(self):
        if self.TrackCircuitFailureToggleButton.isChecked() or self.BrokenRailToggleButton.isChecked() or self.PowerFailureToggleButton.isChecked():
            self.track_instance_copy.lines[1].blocks[int(self.clicked_block)].track_fault_status = True
        else: 
            self.track_instance_copy.lines[1].blocks[int(self.clicked_block)].track_fault_status = False
    
    # train model signal slots 
    def receive_train_model_signals(self):
        self.receive_train_length(self.train_length)
        self.receive_distance_from_block_start(self.distance_from_block_start)
        self.receive_distance_from_yard(self.distance_from_yard)
        
    def receive_train_length(self, length):
        # Handle the received train length signal
        self.train_length = length

    def receive_distance_from_block_start(self, distance_block):
        # Handle the received distance from block start signal
        self.distance_from_block_start = distance_block

    def receive_distance_from_yard(self, distance_yard):
        # Handle the received distance from yard signal
        self.distance_from_yard = distance_yard

        
    # sends updates from track model backend to main backend
    def send_main_backend_update(self):
        signals.track_model_backend_update.emit(self.track_instance_copy)
    
   # Calculates block occupancy
    def block_occupancy(self):
        if len(self.green_line_data) > 0:
        # path to dormont
            path = [63,64,65,66,67,68,69,70,71,72,73]
            block_length_sum = 0
            count = 0
            obj = self.green_line_data[path[count]]
            block = obj[2]
            while count < 11:
                block_length_sum += int(self.green_line_data[block][3])
                if(self.distance_from_yard-block_length_sum <= 30):
                    # position found
                    self.set_block_color(path[count])
                    self.track_instance_copy.lines[1].blocks[path[count]].block_occupancy = True
                    for data in self.green_line_data:
                        if data[2] == block:
                            self.block_grade = data[4]
                    if count == 10: 
                        self.station_name = 'Dormont'
                    return block
                count += 1
        else:
            pass
            
    def set_block_color(self,occupied_block):
        scene = self.graphicsView.scene()
        for item in scene.items():
            if isinstance(item,QtWidgets.QGraphicsRectItem):
                # make occupied block red on map
                if str(item.toolTip()) == str(occupied_block):
                    item.setBrush(QtGui.QColor(255,0,0))
                # put prev block back to green 
                if str(item.toolTip()) == str(occupied_block-1):
                    item.setBrush(QtGui.QColor(0,128,0))
        
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
        for data in self.green_line_data:
            if data[2] == int(block_number):  
                self.block_number_display.setText(str(data[2]))
                if data[3] is not None:
                    self.block_length_display.setText("{:.2f}".format(data[3] * 3.281))
                self.block_grade_display.setText(str(data[4]))
                if data[5] is not None:
                    self.speed_limit_display.setText("{:.2f}".format(data[5] / 1.609))
                self.traffic_light_display.setText(self.track_instance_copy.lines[1].blocks[int(block_number)].get_traffic_light_color_string())
                if data[6] is not None:
                    self.infrastructure_display.setText(str(data[6][0:7]))
                    if str(data[6][0:7]) == 'STATION':
                        self.station_name_display.setText(str(data[6][9:20]))
                    if str(data[6][0:6]) == 'SWITCH' or str(data[6]) == 'UNDERGROUND':
                        self.infrastructure_display.setText(str(data[6]))
                        self.station_name_display.setText('')
                    if str(data[6][0:20]) == 'UNDERGROUND; STATION':
                        self.infrastructure_display.setText(str(data[6][0:20]))
                        self.station_name_display.setText(str(data[6][22:40]))
                    if str(data[6]) == 'RAILWAY CROSSING':
                        self.infrastructure_display.setText(str(data[6]))
                else:
                    self.infrastructure_display.setText(str(data[6]))
                    self.station_name_display.setText(str(data[6]))
                # TODO display active switch direction (if applicable): get signal from wayside
                self.switch_direction_display.setText(self.track_instance_copy.lines[1].blocks[int(block_number)].get_switch_direction_string(1))
                # TODO display crossing status (if applicable): get signal from wayside
                self.crossing_status_display.setText(self.track_instance_copy.lines[1].blocks[int(block_number)].get_crossing_status_string()) 
                if data[8] is not None and data[9] is not None:
                    self.elevation_display.setText("{:.2f}".format(data[8] * 3.281))
                    self.cum_elevation_display.setText("{:.2f}".format(data[9] * 3.281))
                # TODO display beacon data (if applicable)
                # TODO display track heater status
                # TODO display train info (only if block is occupied)
                if block_number == self.occupied_block:
                    self.train_ID_display.setText(str(self.active_trains_instance_copy.Train[0].train_ID))
                    self.direction_of_travel_display.setText('Traveling South')
                    self.authority_display.setText((self.active_trains_instance_copy.Train[0].current_authority) * (3.281 * (73-self.occupied_block)))
                    self.current_speed_display.setText(str(self.active_trains_instance_copy.Train[0].current_suggested_speed))
                # TODO display remainder of station info (tickets sold, passengers boarding and disembarking)
        
    def build_track_map(self):
        line_name = self.TrackLineColorValue.currentText()
    
        if line_name == 'Red Line':
            
            # place the yard block and go from there
            block0 = QtWidgets.QGraphicsRectItem(800,0,40,40)
            block0.setBrush(QtGui.QColor(128,128,128)) # gray color for yard block 
            self.graphicsView.scene().addItem(block0)
            
            # add label to yard 
            text = QtWidgets.QGraphicsTextItem('Yard')
            text.setPos(802,40)
            self.graphicsView.scene().addItem(text)
            
            # use function to keep building map
            self.add_block_to_map(800,-70,40,'block9','9','right',800,0)
            self.add_block_to_map(775,-120,40,'block8','8','right',800,-70)
            self.add_block_to_map(740,-170,40,'block7','7','top',775,-120)
            self.add_block_to_map(690,-170,40,'block6','6','top',740,-170)
            self.add_block_to_map(640,-150,40,'block5','5','top',690,-170)
            self.add_block_to_map(590,-130,40,'block4','4','top',640,-150)
            self.add_block_to_map(540,-110,40,'block3','3','top',590,-130)
            self.add_block_to_map(490,-90,40,'block2','2','top',540,-110)
            self.add_block_to_map(440,-70,40,'block1','1','top',490,-90)
            self.add_block_to_map(390,-30,40,'block16','16','top',440,-70)
            self.add_block_to_map(460,-10,40,'block15','15','bottom',390,-30)
            self.add_block_to_map(520,-12,40,'block14','14','bottom',460,-10)
            self.add_block_to_map(580,-14,40,'block13','13','bottom',520,-12)
            self.add_block_to_map(630,-16,40,'block12','12','bottom',580,-14)
            self.add_block_to_map(680,-20,40,'block11','11','bottom',630,-16)
            self.add_block_to_map(730,-24,40,'block10','10','bottom',680,-20)
            
            # connect blocks 9 and 10
            line = QtWidgets.QGraphicsLineItem(770,-4,800,-50)
            line.setPen(QtGui.QColor(255,255,255))
            self.graphicsView.scene().addItem(line)
            
            # add more blocks
            self.add_block_to_map(330,-30,40,'block17','17','top',390,-30)
            self.add_block_to_map(270,-30,40,'block18','18','top',330,-30)
            self.add_block_to_map(210,-30,40,'block19','19','top',270,-30)
            self.add_block_to_map(150,-30,40,'block20','20','top',210,-30)
            self.add_block_to_map(90,-20,40,'block21','21','top',150,-30)
            self.add_block_to_map(40,30,40,'block22','22','left',90,-20)
            self.add_block_to_map(30,80,40,'block23','23','left',40,30)
            self.add_block_to_map(60,130,40,'block24','24','left',30,80)
            self.add_block_to_map(105,140,40,'block25','25','top',60,130)
            self.add_block_to_map(150,150,40,'block26','26','top',105,140)
            self.add_block_to_map(195,160,40,'block27','27','top',150,150)
            self.add_block_to_map(240,170,40,'block28','28','top',195,160)
            self.add_block_to_map(285,180,40,'block29','29','top',240,170)
            self.add_block_to_map(330,190,40,'block30','30','top',285,180)
            self.add_block_to_map(375,200,40,'block31','31','top',330,190)
            self.add_block_to_map(420,210,40,'block32','32','top',375,200)
            self.add_block_to_map(465,220,40,'block33','33','top',420,210)
            self.add_block_to_map(510,220,40,'block34','34','top',465,220)
            self.add_block_to_map(555,220,40,'block35','35','top',510,220)
            self.add_block_to_map(600,220,40,'block36','36','top',555,220)
            self.add_block_to_map(645,220,40,'block37','37','top',600,220)
            self.add_block_to_map(690,220,40,'block38','38','top',645,220)
            self.add_block_to_map(735,220,40,'block39','39','top',690,220)
            self.add_block_to_map(780,220,40,'block40','40','top',735,220)
            self.add_block_to_map(825,220,40,'block41','41','top',780,220)
            self.add_block_to_map(870,265,40,'block42','42','right',825,220)
            self.add_block_to_map(915,310,40,'block43','43','right',870,265)
            
        elif line_name == 'Green Line':
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

    def add_block_to_map(self,x,y,block_size,block_number,block_number_2,label_pos,prev_x,prev_y):
            block_number = QtWidgets.QGraphicsRectItem(x,y,block_size,block_size)
            block_number.setBrush(QtGui.QColor(0,128,0)) # green color for normal block 
            block_number.setToolTip(str(block_number_2))
            self.graphicsView.scene().addItem(block_number)
            
            # handle different positions for the block label
            if label_pos == 'top' and y<0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x+5,y-(block_size))
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'top' and y>=0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x-5,y-(block_size))
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
                text.setPos(x-5,y+block_size)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'bottom' and y>=0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x-5,y+block_size)
                self.graphicsView.scene().addItem(text)
            
            # draw line to connect blocks with handling for different orientations 
            if(block_number_2 == '28'):
                return
            
            # vertically aligned (negative)
            if (abs(prev_x-x)) <= 10 and y<0: 
                line = QtWidgets.QGraphicsLineItem(prev_x+(block_size/2),prev_y,x+(block_size/2),y+block_size)
                line.setPen(QtGui.QColor(255,255,255)) # white color for lines
                self.graphicsView.scene().addItem(line)
                return
            
            # vertically aligned moving down (positive)
            if (abs(prev_x-x)) <= 10 and y>=0 and y > prev_y: 
                line = QtWidgets.QGraphicsLineItem((x+(block_size/2)),y,prev_x+(block_size/2),prev_y+block_size)
                line.setPen(QtGui.QColor(255,255,255)) # white color for lines
                self.graphicsView.scene().addItem(line)
                return 
            
            # vertically aligned moving upwards
            if (abs(prev_x-x)) <= 10 and y>=0 and prev_y > y:
                line = QtWidgets.QGraphicsLineItem(x+(block_size/2),prev_y,prev_x+(block_size/2),y+block_size)
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
            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrackModelModule()
    window.show()
    sys.exit(app.exec())
