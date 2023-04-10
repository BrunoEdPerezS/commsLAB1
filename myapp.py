import sys
from PyQt5 import QtWidgets, uic, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from threading import Thread
import serial, time
import numpy as np
import csv

#Cantidad de datos para captura
nCAPTURA = 10
escalaX = list(range(nCAPTURA))
escalaX = list(range(nCAPTURA))
grafico1 = list(range(nCAPTURA))
grafico2 = list(range(nCAPTURA))
grafico3 = list(range(nCAPTURA))
grafico4 = list(range(nCAPTURA))
grafico5 = list(range(nCAPTURA))
grafico6 = list(range(nCAPTURA))



#Clase con funcion para captura de datos
class myClassA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        index = 0
        arduino = serial.Serial('COM3', 9600)
        time.sleep(2)
        #Iniciar transferencia, para activar transferencia rapida utilizar este método
        arduino.write(bytes('A', 'utf-8')) 
        fieldnames = ["Gyro","Temp","Press","Acc","Mag","Ext"]
        while(1):
            #Para errores de sincronìa utilizar este metodo
            #arduino.write(bytes('A', 'utf-8'))
            
            
            #Recibir datos y decodificar
            rawString = arduino.readline()
            decodedString = rawString.decode('utf-8')
            print(decodedString)
            #Separar string
            lectura1, lectura2, lectura3, lectura4, lectura5, lectura6  = decodedString.split(",")
            #print(lectura2)
            # Printear, pasar a int, y guardar en array
            grafico1[index] = int(lectura1)
            grafico2[index] = int(lectura2)
            grafico3[index] = int(lectura3)
            grafico4[index] = int(lectura4)
            grafico5[index] = int(lectura5)
            grafico6[index] = int(lectura6)
            if (index >=((nCAPTURA)-1)):
                index = 0
                with open('Datos.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for i in range(len(grafico1)):
                        writer.writerow({'Gyro':grafico1[i],'Temp':grafico2[i],'Press':grafico3[i],'Acc':grafico4[i],'Mag':grafico5[i],'Ext':grafico6[i]})    
                csvfile.close()
            else:
                index = index+1
            #print(grafico1)
        arduino.write(bytes('A', 'utf-8')) 
        arduino.close()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('interfaz.ui', self)

        self.timer = QtCore.QTimer(self)

        #Set escala X e inicio del grafico
        self.graphWidget.setXRange(1, nCAPTURA)
        self.graphWidget.plot(escalaX,escalaX)
        
        #Seteo de botones para los selectores de medición
        self.gyroButton.clicked.connect(self.clickedGyro)
        self.tempButton.clicked.connect(self.clickedTemp)
        self.pressureButton.clicked.connect(self.clickedPress)
        self.accButton.clicked.connect(self.clickedAcc)
        self.magButton.clicked.connect(self.clickedMag)
        self.sensButton.clicked.connect(self.clickedSens)

    #Funcion para graficar
    def plot(self, x, y):
        self.graphWidget.plot(x, y)


#---Eventos para los botones, estos triggean las funciones de actualizacion del grafico-------------------------

    #Presentar gyro
    def clickedGyro(self):
        print("clicked! Gyro")
        self.timer.timeout.connect(self.actualizarGyro)
        self.timer.start(100)
    #Presentar temp
    def clickedTemp(self):
        print("clicked! Temp")
        self.timer.timeout.connect(self.actualizarTemp)
        self.timer.start(100)
    #Presentar pesion    
    def clickedPress(self):
        print("clicked! Pressure")
        self.timer.timeout.connect(self.actualizarPress)
        self.timer.start(100)
    #Presentar acc
    def clickedAcc(self):
        print("clicked! Aceleracion")
        self.timer.timeout.connect(self.actualizarAcc)
        self.timer.start(100)
    #Presentar mag
    def clickedMag(self):
        print("clicked! Magnetometro")
        self.timer.timeout.connect(self.actualizarMag)
        self.timer.start(100)
    #Presentar sensor externo
    def clickedSens(self):
        print("clicked! Sensor externo")
        self.timer.timeout.connect(self.actualizarSens)
        self.timer.start(100)


#---Funciones para actualizacion de los graficos----------------------------------------------------------------

    #Funcion para actualizar grafico Gyro
    def actualizarGyro(self):
        self.graphWidget.clear()
        self.graphWidget.setYRange(1, 260)
        self.plot(escalaX,grafico1)
    #Funcion para actualizar grafico temp
    def actualizarTemp(self):
        self.graphWidget.clear()
        self.graphWidget.setYRange(1, 260)
        self.plot(escalaX,grafico2)
   #Funcion para actualizar grafico presion
    def actualizarPress(self):
        self.graphWidget.clear()
        self.graphWidget.setYRange(1, 260)
        self.plot(escalaX,grafico3)
   #Funcion para actualizar grafico aceleracion
    def actualizarAcc(self):
        self.graphWidget.clear()
        self.graphWidget.setYRange(1, 260)
        self.plot(escalaX,grafico4)
   #Funcion para actualizar grafico megnetometro
    def actualizarMag(self):
        self.graphWidget.clear()
        self.graphWidget.setYRange(1, 260)
        self.plot(escalaX,grafico5)
   #Funcion para actualizar grafico Sensor
    def actualizarSens(self):
        self.graphWidget.clear()
        self.graphWidget.setYRange(1, 260)
        self.plot(escalaX,grafico6)
  

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    myClassA()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



