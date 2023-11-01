from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import *
import sys
import cv2
sys.path.append(".")
import Track_Resources.Track as track
from Main_Backend import *
from signals import *

class SWWaysideFrontend(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                uic.loadUi("Modules/SW_Wayside/Frontend/SW_Wayside_UI.ui", self)
                self.trackInstanceCopy = Track()

                # Signal connections
                signals.sw_wayside_frontend_update.connect(self.update_frontend)

                self.show()
        
        # Main function to call all updates to UI
        def update_frontend(self, trackInstance):
                pass

        # Main function to send all updates to backend
        def frontend_update(self, trackInstance):
                pass
        
        # Updates display based on operation mode
        def update_opeartion_dropdown(self):
                pass

        # Updates display based on line selection
        def update_line_dropdown(self):
                pass

        # Updates display based on wayside selection
        def update_wayside_dropdown(self):
                pass

        # Updates display based on block selection
        def update_block_dropdown(self):
                pass

        # Updates display block dropdown options
        def update_dropdown_blocks(self):
                pass
        
        # Updates display block information
        def update_block_information(self):
                pass

        # Handles view track map button clicked
        def view_track_map_clicked(self):
                pass
        
        # Handles switch toggle in manual mode
        def manual_switch_toggled(self):
                pass

        # Handles light toggle in manual mode
        def manual_light_toggled(self):
                pass

        # Handles crossing toggle in manual mode
        def manual_crossing_toggled(self):
                pass

        # Handles upload plc program button clicked
        def uploadPLCClicked(self):
                fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")

        # Updates copy track instance
        def update_copy_track(self, updatedTrack):
                self.trackInstanceCopy = updatedTrack

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        window = SWWaysideFrontend()
        app.exec()
