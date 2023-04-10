import serial, time
arduino = serial.Serial('COM3', 9600)
time.sleep(2)
while(1):
 rawString = arduino.readline()
 print(rawString)
 time.sleep(1)
arduino.close()