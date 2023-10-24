import sys
import os
from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QFileDialog
import openpyxl

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
        block_width = 20
        block_height = 20
        x = 10
        y = 10
    
        previous_block = None
    
        if line_name == 'Red Line':
            # place the yard block and go from there
            yard = QtWidgets.QGraphicsRectItem(800,0,20,20)
            yard.setBrush(QtGui.QColor(128,128,128)) # gray color for yard block 
            self.graphicsView.scene().addItem(yard)
            
            # add label to yard 
            text = QtWidgets.QGraphicsTextItem('Yard')
            text.setPos(792,25)
            self.graphicsView.scene().addItem(text)
            
            # add next blocks
            block9 = QtWidgets.QGraphicsRectItem(800,-70,40,40)
            block9.setBrush(QtGui.QColor(0,128,0)) # green color by default for block
            self.graphicsView.scene().addItem(block9)
            
            block8 = QtWidgets.QGraphicsRectItem(775,-100,20,20)
            block8.setBrush(QtGui.QColor(0,128,0)) # green color by default for block
            self.graphicsView.scene().addItem(block8)
            
            # connect blocks
            line1 = QtWidgets.QGraphicsLineItem(810,-50,810,0)
            line1.setPen(QtGui.QColor(255,255,255)) # white color for lines
            self.graphicsView.scene().addItem(line1)
            
            
        elif line_name == 'Green Line':
            data = self.green_line_data
        
        yard.mousePressEvent = self.showBlockInfo



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrackModelModule()
    window.show()
    sys.exit(app.exec())
