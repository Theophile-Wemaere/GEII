#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#define ledVie D0

#ifndef STASSID
#define STASSID    "tp5&6"
#define STAPSK     "geii2021"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

LiquidCrystal_I2C lcd(0x27, 16, 2);


//////////////////////////////// setup ////////////////////////////////////////
void setup(void) 
{
  //--------------------------- GPIO LCD SERIAL ------------------------------
  pinMode(ledVie, OUTPUT);
  lcd.begin();
  lcd.backlight();
  Serial.begin(115200);
  lcd.setCursor(0,0);
  lcd.print("Try to connect");
  lcd.setCursor(0,1);
  lcd.print(STASSID);

 //----------------------- WIFI connexion ----------------------------------- 
  WiFi.mode(WIFI_STA); //station mode : la carte se connecte à un point d'accès
  WiFi.begin(ssid, password); //commence la connexion
  Serial.println("");
  int i=0;
 // Wait for connection
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
    lcd.setCursor(10,1);
   
    switch(i%3) { case 0: lcd.print("|"); break;
                  case 1: lcd.print("/"); break;
                  case 2: lcd.print("-");
              } 
     i++;         
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("bruce")) 
  {
    Serial.println("MDNS responder started");
  }
  lcd.setCursor(0,0);
  lcd.print("Nom : bruce");
  lcd.setCursor(0,1);
  lcd.print(WiFi.localIP());
}

//////////////////////////// loop ///////////////////////////////////////
void loop(void) 
{
  digitalWrite(ledVie, HIGH); 
  delay(50);
  MDNS.update();
  digitalWrite(ledVie, LOW); 
  delay(50);
}
