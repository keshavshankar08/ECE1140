import sys
import serial
import time
sys.path.append(".")
from signals import signals
from Track_Resources.Track import *

SER = serial.Serial('COM3', 9600)
time.sleep(1)

# send PLC program serially
def send_PLC(data):
    SER.write(data.encode('ascii'))
    time.sleep(1)
    response = SER.readline().decode('ascii').strip()
    print("Arduino output: \n", response)
    
def test_PLC():
    PLC = "Program PLC Here is the PLC Program for testing"
    send_PLC(PLC)

def test_PLC2():
    PLC = "Second signal sent to PLC"
    send_PLC(PLC)

test_PLC()
time.sleep(2)
test_PLC2()
