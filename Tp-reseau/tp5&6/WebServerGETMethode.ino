#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#define ledVie D0
#define cmdeRelay D5

#ifndef STASSID
#define STASSID "tp5&6"
#define STAPSK  "geii2021"
#endif

const char* ssid = STASSID;
const char* password = STAPSK;
bool stateTog = false, stateRelay;
unsigned int timeTog = 0, intervall = 1000;

ESP8266WebServer server(80);
LiquidCrystal_I2C lcd(0x27, 16, 2);


/////////////////////////////// 200 OK //////////////////////////////////////////
void handleRelay() { 
  String message = "<html> <body> <center> <H1> <BR> <BR> Welcome <BR> Relay ";
  if(server.argName(0) == "relay") 
  {  //relay=[on|off|tog]
     if(server.arg(0) == "on") 
     {
       stateRelay = 1; 
       digitalWrite(cmdeRelay,stateRelay);
       lcd.setCursor(0,1);
       lcd.print("Relay ON ");      
     }
     else if (server.arg(0) == "off") 
     {
         stateRelay = 0;
         digitalWrite(cmdeRelay,stateRelay);
         lcd.setCursor(0,1);
         lcd.print("Relay OFF");
     }
     else if (server.arg(0) == "tog") 
     {
	   stateRelay = 1; 
	   digitalWrite(cmdeRelay,stateRelay);
	   lcd.setCursor(0,1);
	   lcd.print("Relay TOG");
	   stateTog = 1;
	   timeTog = millis();             
     }
  } 
  stateRelay = digitalRead(cmdeRelay);
  if(stateRelay) message += "OFF "; else message +="ON";
  message += "</H1> <BR> <BR>If you want to change <BR> Use URL: http://name.local/?relay=[on|off|tog]</center>  </body> </html>";
  server.send(200, "text/html",message);  
  }

/////////////////////////////////// Error 404 //////////////////////////////////
void error404() 
{
  String message = "<html> <body> <center> <h1> 404 : Not found </h1> </center> </body> </html>";
  server.send(404, "text/html",message);
}

//////////////////////////////// setup ////////////////////////////////////////
void setup(void) 
{
  //--------------------------- GPIO LCD SERIAL ------------------------------
  pinMode(ledVie, OUTPUT);  // Initialize the LED_BUILTIN pin as an output
  //pinMode(cmdeRelay, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin();
  lcd.backlight();
  Serial.begin(115200);
  lcd.setCursor(0,0);
  lcd.print("Try to connect");
  lcd.setCursor(0,1);
  lcd.print(STASSID);

 //----------------------- WIFI connexion ----------------------------------- 
  WiFi.mode(WIFI_AP);
  WiFi.begin(ssid, password);
  Serial.println("");

  int i=0;
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
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

  if (MDNS.begin("bruce")) {
    Serial.println("MDNS responder started");
  }
 //--------------------- server configuratiuon -------------------------------
  server.on("/", handleRelay);
  server.onNotFound(error404);
  server.begin();
  Serial.println("HTTP server started");

  //------------------- Relay init ----------------------------------------
  stateRelay = LOW;
  digitalWrite(cmdeRelay,LOW);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("bruce.local");
  lcd.setCursor(0,1);
  lcd.print("Relay OFF");
}

//////////////////////////// loop ///////////////////////////////////////
void loop(void) 
{
  //digitalWrite(ledVie, HIGH); 
  delay(50);
  server.handleClient();
  MDNS.update();
  //digitalWrite(ledVie, LOW); 
  delay(50);
  
  //------------- tog mode: just during intervall time ON ------------
  if(stateTog == 1) 
  {
    if(millis() > timeTog + intervall ) 
	  {
      stateTog = 0;
      stateRelay = 1; //0
      //digitalWrite(cmdeRelay,stateRelay);
      digitalWrite(LED_BUILTIN,stateRelay);
      lcd.setCursor(0,1);
      lcd.print("Relay OFF");
    }
  }
}
