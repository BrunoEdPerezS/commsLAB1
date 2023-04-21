
#include <Wire.h>

const int Trigger = 2;   //Pin digital 2 para el Trigger del sensor
const int Echo = 3;   //Pin digital 3 para el Echo del sensor

void setup() {
  Wire.begin(8);                // join I2C bus with address #8
  Wire.onRequest(requestEvent); // register event
  pinMode(Trigger, OUTPUT); //pin como salida
  pinMode(Echo, INPUT);  //pin como entrada
  digitalWrite(Trigger, LOW);//Inicializamos el pin con 0
}

void loop() {
  delay(100);
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()
void requestEvent() {

  long t; //timepo que demora en llegar el eco
  int d; //distancia en centimetros
  
  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);
  
  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = int(t/59);             //escalamos el tiempo a una distancia en cm
  
  //Serial.print("Distancia: ");
  //Serial.print(d);      //Enviamos serialmente el valor de la distancia
  //Serial.print("cm");
  //Serial.println();          //Hacemos una pausa de 100ms
  Wire.write((byte)(d >> 8)); // Enviar el primer byte del dato
  Wire.write((byte)d); // Enviar el segundo byte del dato
  // as expected by master
}
