#include <SPI.h>

#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"

#define RF24_CEPIN 9			// pin ce du spi
#define RF24_CSPIN 10			// pin cs du spi

const int xpin = A0; //pin x accelerometre
const int ypin = A1; //pin y accelerometre
const int zpin = A2; //pin z accelerometre
 
RF24 radio(RF24_CEPIN, RF24_CSPIN);     //  le module nRF24l01
char payload[32+1] = {0};


const uint64_t txPipe = 0xE8E8E8E8E3LL; //fréquence de transmission
const uint64_t rxPipe = 0xF6F6F6F6F3LL; //fréquence de réception


//---------------------------------------------------------------
void setup()
{
  Serial.begin(9600);
    
  //communication
  radio.begin();
  printf_begin();
  radio.printDetails();
  
  //Default radio settings
  radio.enableDynamicPayloads();    // payload de taille variable
  radio.setDataRate(RF24_1MBPS);    // 1 Mbits/s
  radio.setPALevel(RF24_PA_MAX);    // puissance maxi
  radio.setChannel(0x2A);           // la fréquence 2,4G + n*1*M 
  
  // delay 4 ms, 15 retries
  // 0 - 250us, 15 - 4000us
  radio.setRetries(15,15);      // retrie & timeout
  
  radio.openWritingPipe(txPipe);
  radio.openReadingPipe(1,rxPipe);
  radio.setAutoAck(true);
  
  // en écoute
  radio.startListening();
}

//variables 
unsigned long millis1,previousMillis1=0;
float x,y,z;
double tang,roulis,vert;

void loop()
{
  millis1 = millis();
  
  //recupération des tensions de l'accéléromètre 
  x = analogRead(xpin)*5.0/1024; 
  delay(1); //
  y = analogRead(ypin)*5.0/1024; 
  delay(1); 
  z = analogRead(zpin)*5.0/1024;
    
  if(millis1 - previousMillis1 >= 200) //transmissions des données toutes les 200ms
  {
    previousMillis1 = millis1;
    // affichage des tensions
    Serial.print("x: " + String(x));
    Serial.print(" ");
    Serial.print("y: " + String(y));
    Serial.print(" ");
    Serial.println("z: " + String(z)); 

    //calcul de Gx, Gy, Gz et G
    float Gx = (x- 1.60)*1000;
    float Gy = (y - 1.62)*1000;
    float Gz = (z - 1.59)*1000;
    float G = sqrt(Gx*Gx+Gy*Gy+Gz*Gz);
  
    //calcul et affichage de l'angle de tangage
    tang=asin(Gx/G)*180/PI;
    Serial.println("tangage: " + String(tang));
  
    //calcul et affichage de l'angle de roulis
    roulis=asin(Gy/G)*180/PI;
    Serial.println("roulis: " + String(roulis));
  
    //calcul et affichage de la verticalité
    vert=atan(Gz/G)*180/PI;
    Serial.println("verticalité: " + String(vert));

    Serial.println(" "); //séparation

    //formation de la payload
    x=x*100; y=y*100; z=z*100; //transforamtion des floats en int pour le transfert
    sprintf(payload,"T%dR%dV%dX%dY%dZ%d",int(tang),int(roulis),int(vert),int(x),int(y),int(z));
    
    Serial.println(payload); //verification
    
    // verify if channel is free
    if (!radio.testCarrier())
    {
        // send payload
        radio.stopListening();    // en emission
        radio.write((void *)payload, strlen(payload)); //emission de la payload
        radio.startListening();
    }
  }
}
