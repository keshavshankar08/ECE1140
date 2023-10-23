import sys
import os
from PyQt6 import QtWidgets, QtGui, uic
from PyQt6.QtCore import Qt
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

        uic.loadUi("Track_Model_UI.ui", self)
        
        # load track model button
        self.LoadTrackModelButton.clicked.connect(self.track_layout)

        # set up scene for graphics view and set scene size to widget size 
        self.graphicsView.setScene(QtWidgets.QGraphicsScene())
        self.graphicsView.setSceneRect(0,0,1221,521)
        
        # build track in graphics view
        self.TrackLineColorValue.currentTextChanged.connect(self.build_track_map)
        
        # create rectangle item
        '''
        rect = QtWidgets.QGraphicsRectItem(0, 0, 100, 100) 
        rect.setBrush(QtGui.QColor(0, 255, 255))  # Use QColor to specify blue (RGB: 0, 0, 255)
        rect.setPen(QtGui.QColor(0, 0, 0))     # Use QColor to specify black (RGB: 0, 0, 0)
        self.graphicsView.scene().addItem(rect)
        
        
        # move rectangle to new coordinates
        rect.setPos(100,200)
        
        
        # open popup when clicked 
        rect.mousePressEvent = self.showBlockInfo
        '''
        
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
        sheet1 = layout_data['Blue Line'] 
        sheet2 = layout_data['Red Line']
        sheet3 = layout_data['Green Line']
        
        # declare list to store line data
        self.blue_line_data = []
        self.red_line_data = []
        self.green_line_data = []
        
        # iterate through to extract data
        for row in sheet1.iter_rows(min_row=2, max_row=16, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, elevation, cumulative_elevation = row[:9]
            
            # Append the data to the list in the desired format
            self.blue_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, elevation, cumulative_elevation))
            
        
        # do same for red and green lines
        for row in sheet2.iter_rows(min_row=2, max_row=77, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation = row[:10]
            
            self.red_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation))
            
        
        for row in sheet3.iter_rows(min_row=2,max_row=151, values_only=True):
            line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time = row[:11]
            
            self.green_line_data.append((line, section, block_number, block_length, block_grade, speed_limit, infrastructure, station_side, elevation, cumulative_elevation, traversal_time))
        
            
        
    def build_track_map(self):
        line_name = self.TrackLineColorValue.currentText()
        block_width = 20
        block_height = 20
        x = 50
        y = 50
    
        previous_block = None
    
        if line_name == 'Blue Line':
            data = self.blue_line_data
        elif line_name == 'Red Line':
            data = self.red_line_data
        elif line_name == 'Green Line':
            data = self.green_line_data
    
        for row in data:
            section, block_number, block_length, infrastructure = row[1], row[2], row[3], row[6]
        
            # create rectangle for block
            block = QtWidgets.QGraphicsRectItem(x, y, block_width, block_height)
            block.setBrush(QtGui.QColor(0, 128, 0))  # Green
            self.graphicsView.scene().addItem(block)
        
            # add block number label
            text = QtWidgets.QGraphicsTextItem(f'Block {block_number}')
            text.setPos(x, y - 25)
            self.graphicsView.scene().addItem(text)

            # connect blocks with lines
            if previous_block is not None:
                line = QtWidgets.QGraphicsLineItem(previous_block.x() + block_width, y + block_height / 2, block.x(), y + block_height / 2)
                line.setPen(QtGui.QColor(255, 255, 255))  # White
                self.graphicsView.scene().addItem(line)
        
            previous_block = block
        
            x += block_width + 50  # Spacing between blocks
        
        block.mousePressEvent = self.showBlockInfo



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TrackModelModule()
    window.show()
    sys.exit(app.exec())
