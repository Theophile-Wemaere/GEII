#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#define ledVie D0
#define RLY D5

#ifndef STASSID
#define STASSID "tp5&6"      //your SSID
#define STAPSK  "geii2021"      //your password 
#endif

const char* ssid = STASSID;
const char* password = STAPSK;

LiquidCrystal_I2C lcd(0x3f, 16, 2);

WiFiServer server(1026);    //define the port here

//////////////////////////////// setup ////////////////////////////////////////
void setup(void) 
{
  //--------------------------- GPIO LCD SERIAL ------------------------------
  pinMode(ledVie, OUTPUT);  // Initialize the LED_BUILTIN pin as an output
  pinMode(RLY, OUTPUT);
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

  if (MDNS.begin("bruce")) {                 //XXXXXXXX.local is the MDNS name
    Serial.println("MDNS responder started");
  }
  lcd.setCursor(0,0);
  lcd.print(WiFi.localIP()); lcd.print("   ");
  lcd.setCursor(0,1);
  lcd.print("server wait");
  server.begin();
}
char recept[18]="";
int i=0;
WiFiClient client;    
char c;
bool verif=false;
unsigned long connexion_time;

//////////////////////////// loop ///////////////////////////////////////
void loop(void) 
{
  digitalWrite(ledVie, HIGH); 
  delay(50);
 
  MDNS.update();
  if (!client.connected() )//client is connected?
  {            
      client = server.available();  //test if one client is available
      if (client)
      {
	  client.write("\nEnter \"rly on\" or \"rly off\":\n"); //connexion established
	  connexion_time=millis();
      }
      
  }
  else //client is connected
  {
    if(millis() >= connexion_time + 10000)
    {
      client.stop();                            
    }
    else
    {
	   //handle client
       c = client.read(); //read char one by one
       if(c=='r') verif=true; //check if the client is writing a command
       if((c!='\n') && (c!='\r') && (i<17)) //c is not CR not LF and buffer is not overlow
       {  
          if(verif)
          {                        
            recept[i++] = c;   //put c in the string recept
          }
       }
       else 
       {
           recept[i]='\0';
           i=0;
           verif=false;
           client.stop();                                         //deconnect the client
           lcd.clear();
           lcd.setCursor(0,0);
           String cmd = (String)recept;
           lcd.print("Last command:");
           lcd.setCursor(0,1);
           lcd.print(cmd); 
           //Serial.println(cmd, HEX);
           if(cmd == "rly on") digitalWrite(RLY, HIGH);           //command equals "rly on"?
           else if (cmd == "rly off") digitalWrite(RLY, LOW);    //command equals "rly off"?
       }
     }    
  } 
  digitalWrite(ledVie, LOW); 
  delay(50); 
}
