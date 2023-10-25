from PyQt6.QtCore import QThread, QCoreApplication
from signals import signals
from SystemTime import SystemTime
import sys

# run this function to see how the clock works

def dummyFunction(current_time):
        print("Current Time:", current_time)
        if current_time.second() == 3:
                signals.stop_timer.emit()
                sys.exit(1)


if __name__ == '__main__':
        app = QCoreApplication([])
        signals.current_system_time.connect(dummyFunction)
        thread = QThread() 
        system_time = SystemTime()
        system_time.moveToThread(thread) 
        thread.start()
        sys.exit(app.exec())