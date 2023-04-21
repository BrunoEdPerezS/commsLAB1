
#include <MPU9250_asukiaaa.h>
#include <Adafruit_BMP280.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>


//Declaraciones--------------------------------------------------
Adafruit_BMP280 bmp; // I2C
MPU9250_asukiaaa mySensor;
float aX, aY, aZ,aMAG, gX, gY, gZ, mX, mY, mZ, mDIR, temp, bar;
LiquidCrystal_I2C lcd(0x27,20,4);;  
bool flag = false;
//-----------------------------------------------------------------



void setup() {
  
  Serial.begin(9600);
  //while (!Serial);

  //SETUP DEL GY91------------------------------------------------
  Wire.begin();
  Wire.setClock(400000);
  mySensor.setWire(&Wire);
  mySensor.beginAccel();
  mySensor.beginGyro();
  mySensor.beginMag();
  if (!bmp.begin(0x76)) {
    //Serial.println("No se pudo encontrar un sensor BMP280 válido, verifica las conexiones!");
    while (1);
  }  


  //SETUP DEL LCD-------------------------------------------------
  lcd.init();
  lcd.backlight();

  
}

void loop() {


String TOKEN = Serial.readString();
if (TOKEN == "A")
{ 
  flag = true;
}

while(flag){

//SLAVE RECIEVE---------------------------------------------------
  int dato = 1; // Variable donde se almacenará el dato recibido
  Wire.beginTransmission(8); // Definir el esclavo (dirección 8)
  Wire.requestFrom(8, 2); // Solicitar dos bytes al esclavo
  
  if (Wire.available() >= 2) { // Si se recibieron los dos bytes correctamente
    dato = Wire.read() << 8 | Wire.read(); // Combinar los bytes en un número de tipo int
  }
  String dato_ST = String(dato);

  
//Actualizacion de acelerometro-----------------------------------
  if (mySensor.accelUpdate() == 0) {
    aX = mySensor.accelX();
    aY = mySensor.accelY();
    aZ = mySensor.accelZ();
    aMAG = mySensor.accelSqrt();
  }
//Actualizacion de gyro-----------------------------------------
  if (mySensor.gyroUpdate() == 0) {
    gX = mySensor.gyroX();
    gY = mySensor.gyroY();
    gZ = mySensor.gyroZ();
  }
//Actualizacion de magnetometro-----------------------------------
  if (mySensor.magUpdate() == 0) {
    mX = mySensor.magX();
    mY = mySensor.magY();
    mZ = mySensor.magZ();
    mDIR = mySensor.magHorizDirection();
  }
//Actualizacion de variables climáticas-------------------------------
    temp = bmp.readTemperature();
    bar = bmp.readPressure()/3377;



//LCD PRINT-----------------------------------
lcd.clear();
lcd.setCursor(0, 0);
lcd.print("Temp(*C): ");
lcd.print(temp);
lcd.setCursor(0, 1);
lcd.print("Press(Hg): ");
lcd.print(bar);



//UART SEND---------------------------------------------

//Datos acelerometro
    String accST =String(aX)+","+String(aY)+","+String(aZ)+",";
    String accMAG_ST = String(aMAG)+",";
//Datos gyro
    String gyro_ST =String(gX)+","+String(gY)+","+String(gZ)+",";
//Datos del magnetometro
    String magST =String(mX)+","+String(mY)+","+String(mZ)+",";
    String mDIR_ST = String(mDIR)+",";
//Temperatura
    String sTe =String(temp)+",";
//Presion
    String sBa =String(bar)+",";

//Enviar cadena
Serial.flush();
Serial.println(gyro_ST+sTe+sBa+accMAG_ST+mDIR_ST+dato_ST);

   

//DELAY PARA TS
//delay(100);
  }
}
