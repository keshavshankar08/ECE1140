from PyQt5 import QtWidgets, uic
import sys

class SW_Wayside_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(SW_Wayside_UI, self).__init__()
        uic.loadUi("/Users/keshavshankar/Documents/Trains/ECE1140/src/frontend/SW_Wayside/SW_Wayside_UI.ui", self)
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = SW_Wayside_UI()
    app.exec_()

if __name__ == '__main__':
    main()