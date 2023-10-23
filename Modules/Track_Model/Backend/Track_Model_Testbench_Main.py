import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class TrackModelModule(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Track_Model_Testbench.ui", self)
        self.TrackCircuitFailureToggleButton.clicked.connect(self.slot1)
        self.PowerFailureToggleButton.clicked.connect(self.slot2)
        self.BrokenRailToggleButton.clicked.connect(self.slot3)

    def slot1(self, clicked1: bool):
        if clicked1 or self.PowerFailureToggleButton.isChecked() or self.BrokenRailToggleButton.isChecked(): 
            self.TrackFaultOutput.setText("Yes")
        else: 
            self.TrackFaultOutput.setText("No")

    def slot2(self, clicked2: bool):
        if clicked2 or self.TrackCircuitFailureToggleButton.isChecked() or self.BrokenRailToggleButton.isChecked(): 
            self.TrackFaultOutput.setText("Yes")
        else: 
            self.TrackFaultOutput.setText("No")

    def slot3(self, clicked3: bool):
        if clicked3 or self.TrackCircuitFailureToggleButton.isChecked() or self.PowerFailureToggleButton.isChecked(): 
            self.TrackFaultOutput.setText("Yes")
        else: 
            self.TrackFaultOutput.setText("No")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrackModelModule()
    window.show()
    sys.exit(app.exec())
