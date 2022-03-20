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
bool stateRelay;


ESP8266WebServer server(80);            //web server declaration
LiquidCrystal_I2C lcd(0x27, 16, 2);

////////////////////////////// Generate HTML /////////////////////////////
String getPage()
{
  String page = "<html>";                  //<meta http-equiv='refresh' content='10'/>
  page += "<head><title>ESP8266 Post Method Q1</title>";
  page += "<style> body { background-color: #fffff; font-family: Arial, Helvetica, Sans-Serif; Color: #008800; }</style>";
  page += "</head><body><center><h1>ESP8266 Post Method</h1>";
  page += "<h3>Relay command</h3>";
  page += "<form action='/' method='POST'>";
  page += "<button type='button submit' name='RLY' value='1'>ON</button>     ";
  page += "<button type='button submit' name='RLY' value='0'>OFF</button>";
  page += "</form></center></body></html>";
  return page;
}

///////////////////////////////// handle http request ///////////////////////
void handleRoot(){ 
  String postValue;
  if ( server.hasArg("RLY") )
  {
    postValue = server.arg("RLY");
    if ( postValue == "1" ) 
    {
      stateRelay = HIGH;
      //digitalWrite(cmdeRelay, stateRelay);
      digitalWrite(LED_BUILTIN, stateRelay);
      lcd.setCursor(0,1);
      lcd.clear();
      lcd.print("Relay ON ");
      server.send ( 200, "text/html", getPage() );  
    } 
    else if ( postValue == "0") 
    {
      stateRelay = LOW;
      //digitalWrite(cmdeRelay, stateRelay);
      digitalWrite(LED_BUILTIN, stateRelay);
      lcd.setCursor(0,1);
      lcd.print("Relay OFF");
      server.send ( 200, "text/html", getPage() );  
    }       
  }
  else
  {
    String page = getPage();
   server.send ( 200, "text/html", page );  
  }
}

/////////////////////////////////// Error 404 //////////////////////////////////
void handleNotFound() {
  String message = "<html> <body> <H1> <center> <BR> <BR> Error 404, File Not Found on this server</center> </H1> </body> </html>";
  server.send(404, "text/html", message);
}

//////////////////////////////// setup ////////////////////////////////////////
void setup(void) {
  //--------------------------- GPIO LCD SERIAL ------------------------------
  //pinMode(ledVie, OUTPUT);  // Initialize the LED_BUILTIN pin as an output
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
  WiFi.mode(WIFI_STA);
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

  if (MDNS.begin("bruce")) 
  {
    Serial.println("MDNS responder started");
  }
 //--------------------- server configuratiuon -------------------------------
  server.on("/", handleRoot);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");

  //------------------- Relay init ----------------------------------------
  stateRelay = LOW;
  digitalWrite(cmdeRelay,LOW);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("ESP WEB Server");
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
}
