import serial
import time

SERIALCOMM = serial.Serial('COM3', 9600)
SERIALCOMM.timeout = 1

# test boolean variables
TDEFA = 1
TJUNC = 1
TCROS = 1
TSTAT = 1

TransferData = str(TDEFA) + str(TJUNC) + str(TCROS) + str(TSTAT)

for iter in range(1,7):
    SERIALCOMM.write(TransferData.encode())
    time.sleep(0.5)
    print(SERIALCOMM.readline().decode('ascii').rstrip('\n'))
SERIALCOMM.close()