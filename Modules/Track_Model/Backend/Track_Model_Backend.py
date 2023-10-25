import sys
import os
from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QFileDialog
import openpyxl, re

class BlockInfoPopup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Block Information")
        self.setGeometry(100, 100, 300, 200)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("This is a pop-up window.")
        layout.addWidget(label)
        self.setLayout(layout)
        
                
class Block():
    # member variables
    BlockNumber, PrevBlockNumber, NextBlockNumber = None, None, None # ints
    BlockType, StationName, SwitchDirection = None, None, None # strings
    BlockOccupancy, TrackFault, Maintenance, CrossingActive, IsReceiver, LightColor = None, None, None, None, None, None # bools
    
class LineStatus():
    # member variables
    LineName = None # string
    Blocks = [] # array of blocks
    # TODO declare map here 
    
        
class TrackModelModule(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('/Users/benshuttleworth/Desktop/ECE 1140/trains/ECE1140/Modules/Track_Model/Frontend/Track_Model_UI.ui',self)
        
        # disable line selector until track is loaded to avoid undefined behavior
        self.TrackLineColorValue.setEnabled(False)
        
        # line color combo box hint behavior, hide hint initially
        self.TrackLineColorValue.installEventFilter(self)
        self.LineSelectHint.setVisible(True)
        
        # load track model button
        self.LoadTrackModelButton.clicked.connect(self.track_layout)

        # set up scene for graphics view and set scene size to widget size 
        self.graphicsView.setScene(QtWidgets.QGraphicsScene())
        self.graphicsView.setSceneRect(0,0,1221,521)
        
        # build track in graphics view
        self.TrackLineColorValue.currentTextChanged.connect(self.build_track_map)
        
    # functions 
    
    def showBlockInfo(self,event):
        if event.button() == Qt.MouseButton.LeftButton:
            popup = BlockInfoPopup()
            popup.exec()
    
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
        file_name = os.path.basename(response) # extract the filename from the path
        layout_data = openpyxl.load_workbook(file_name, data_only=True) # open workbook and extract data only (take result from cells with formulas)
        
        # get assign sheets to sheet names from the file
        sheet3 = layout_data['Red Line']
        sheet4 = layout_data['Green Line']
        
        # declare list to store line data
        self.red_line_data = []
        self.green_line_data = []
        
        # iterate through to extract data
        for row in sheet3.iter_rows(min_row=2, max_row=77, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation = row[:10]
            
            self.red_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation))
            
        
        for row in sheet4.iter_rows(min_row=2,max_row=151, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time = row[:11]
            
            self.green_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time))
        
        # enable line selection after track layout is loaded 
        self.LineSelectHint.setVisible(False)
        self.TrackLineColorValue.setEnabled(True)
            
        
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
            self.add_block_to_map(800,-70,'block9','9','right',800,0)
            self.add_block_to_map(775,-120,'block8','8','right',800,-70)
            self.add_block_to_map(740,-170,'block7','7','top',775,-120)
            self.add_block_to_map(690,-170,'block6','6','top',740,-170)
            self.add_block_to_map(640,-150,'block5','5','top',690,-170)
            self.add_block_to_map(590,-130,'block4','4','top',640,-150)
            self.add_block_to_map(540,-110,'block3','3','top',590,-130)
            self.add_block_to_map(490,-90,'block2','2','top',540,-110)
            self.add_block_to_map(440,-70,'block1','1','top',490,-90)
            self.add_block_to_map(390,-50,'block16','16','top',440,-70)
            self.add_block_to_map(460,0,'block15','15','bottom',390,-50)
            
        elif line_name == 'Green Line':
            data = self.green_line_data
        
        block0.mousePressEvent = self.showBlockInfo

    def add_block_to_map(self,x,y,block_number,block_number_2,label_pos,prev_x,prev_y):
            block_number = QtWidgets.QGraphicsRectItem(x,y,40,40)
            block_number.setBrush(QtGui.QColor(0,128,0)) # gray color for yard block 
            self.graphicsView.scene().addItem(block_number)
            
            # handle different positions for the block label
            if label_pos == 'top' and y<0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x+13,y-20)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'top' and y>=0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x+15,y+20)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'right':
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x+40,y+10)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'left':
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x-40,y+10)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'bottom' and y<0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x-15,y+20)
                self.graphicsView.scene().addItem(text)
            
            if label_pos == 'bottom' and y>=0:
                text = QtWidgets.QGraphicsTextItem(block_number_2)
                text.setPos(x+11 ,y+40)
                self.graphicsView.scene().addItem(text)
            
            # draw line to connect blocks with handling for different orientations 
            # blocks in line vertically 
            if x == prev_x and y<0: 
                line = QtWidgets.QGraphicsLineItem(x+20,prev_y,prev_x+20,prev_y-30)
                line.setPen(QtGui.QColor(255,255,255)) # white color for lines
                self.graphicsView.scene().addItem(line)
            
            if x == prev_x and y>=0:
                line = QtWidgets.QGraphicsLineItem(x+20,prev_y,prev_x+20,prev_y+30)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            # blocks in line horizontally
            if y == prev_y and y<0:
                line = QtWidgets.QGraphicsLineItem(x+40,prev_y+20,prev_x,prev_y+20)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
             
            if y == prev_y and y>=0:
                line = QtWidgets.QGraphicsLineItem(x+20,prev_y+20,prev_x-20,prev_y+20)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            # diagonal cases
            elif x != prev_x and y != prev_y and x<prev_x and y<prev_y and y<0:
                line = QtWidgets.QGraphicsLineItem(x+30,y+40,prev_x+10,prev_y)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            elif x != prev_x and y != prev_y and y>=0:
                line = QtWidgets.QGraphicsLineItem(x+30,y-40,prev_x+10,prev_y)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)
            
            elif x != prev_x and y != prev_y and y>prev_y:
                line = QtWidgets.QGraphicsLineItem(prev_x,prev_y+20,x+40,y+10)
                line.setPen(QtGui.QColor(255,255,255))
                self.graphicsView.scene().addItem(line)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrackModelModule()
    window.show()
    sys.exit(app.exec())
