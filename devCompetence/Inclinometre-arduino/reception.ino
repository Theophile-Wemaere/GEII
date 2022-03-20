#include <SPI.h>

#include <RF24_config.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"

#define RF24_CEPIN 9		// pin ce du spi
#define RF24_CSPIN 10		// pin cs du spi

#define LED_R 5 //pin R 
#define LED_G 3 //pin G
#define LED_B 6 //pin B

RF24 radio(RF24_CEPIN, RF24_CSPIN);     //  le module nRF24l01
char payload[32+1] = {0};


 const uint64_t rxPipe = 0xE8E8E8E8E3LL; //fréquence de réception
 const uint64_t txPipe = 0xF6F6F6F6F3LL; //fréquence de transmission


//---------------------------------------------------------------
void setup()
{
  Serial.begin(9600);
  printf_begin();
  //communication
  radio.begin();
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

  //déclaration des sorties de la RGB
  pinMode(LED_R,OUTPUT);
  pinMode(LED_G,OUTPUT);
  pinMode(LED_B,OUTPUT);
}

//variables
int T, R, V, tang, roulis, verti,X,Y,Z; 
float x,y,z;

void loop()
{
  // quelque chose est il arrivé ?
  if (radio.available())
  {
			int pls = radio.getDynamicPayloadSize();
			if (pls>=1 && pls<32)
			{
					  radio.read((void*)payload, pls);
					  payload[pls]=0;
           
					  Serial.println(payload); //affichage de la payload reçue
            
            // traitement de la payload
            String Newpayload=String(payload); //conversion char[] to String

            //index des repères dans la payload
            T = Newpayload.indexOf("T");
            R = Newpayload.indexOf("R");
            V = Newpayload.indexOf("V");
            X = Newpayload.indexOf("X");
            Y = Newpayload.indexOf("Y");
            Z = Newpayload.indexOf("Z");

            //récupération des angles en fonction des indexs 
            tang = Newpayload.substring(T+1,R).toInt(); 
            roulis = Newpayload.substring(R+1,V).toInt();
            verti = Newpayload.substring(V+1,X).toInt(); 

            //récupération des tensions et reconversion en float
            x = (Newpayload.substring(X+1,Y).toInt())/100.0; 
            y = (Newpayload.substring(Y+1,Z).toInt())/100.0;
            z = (Newpayload.substring(Z+1).toInt())/100.0;

            //affichage des données
            Serial.println("Tangage : " + String(tang) + " Roulis : " + String(roulis) + " Verticalité : " + String(verti) + " Vx: " + String(x) + " Vy: " + String(y) + " Vz : " + String(z)); 
            Serial.println(" ");
            delay(10);
		  }
	}
  RGB(tang); //gestion de la led RGB en fonction d'un angle au choix 
}

void RGB(int angle) //gestion de la led RGB en fonction d'un angle au choix
{
  if(angle >= 0 && angle <= 90)
  {
    digitalWrite(LED_R,0);
    int coeff1 = angle*255/80;
    analogWrite(LED_B, coeff1);
    analogWrite(LED_G, 255-coeff1);    
  }

  if(tang <= 0 && tang >= -90)
  {
    digitalWrite(LED_B,0);
    int coeff2 = -angle*255/80;
    analogWrite(LED_R, coeff2); 
    analogWrite(LED_G, 255-coeff2);   
  }
}
