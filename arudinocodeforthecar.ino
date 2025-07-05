#include <WebServer.h>
#include <WiFi.h>
#include <WiFiUdp.h>
int l = 1;
//set up to connect to an existing network (e.g. mobile hotspot from laptop that will run the python code)
const char* ssid = "CGM-D";
const char* password = "cgm@d#300";
WiFiUDP Udp;
unsigned int localUdpPort = 4210;  //  port to listen on
char incomingPacket[255];  // buffer for incoming packets
int trigPin = 17;
int echoPin = 19;
int buzzer  = 18;
int led  = 27;
void setup()
{
  pinMode(26,OUTPUT);
  pinMode(4,OUTPUT);
  pinMode(32,OUTPUT);
  pinMode(33,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(15,OUTPUT);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(led, OUTPUT);
  int status = WL_IDLE_STATUS;
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to wifi");
//    pinMode(trigPin, OUTPUT);
//pinMode(echoPin, INPUT);
// pinMode(buzzer, OUTPUT);
//  pinMode(led, OUTPUT);
  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  // we recv one packet from the remote so we can know its IP and port


}

void loop()
{
//  if (l ==1){
//     pinMode(trigPin, OUTPUT);
//  pinMode(echoPin, INPUT);
// pinMode(buzzer, OUTPUT);
//  pinMode(led, OUTPUT);
//  }
    int packetSize = Udp.parsePacket();
    if (packetSize)
     {
      // receive incoming UDP packets
      Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
      int len = Udp.read(incomingPacket, 255);
      if (len > 0)
      {
        incomingPacket[len] = 0;
      }
      
      String incoming = incomingPacket;
      Serial.printf("UDP packet contents: %s\n", incomingPacket);
      if (incoming == "left"){
        left();
        
        }
    else   if (incoming == "right"){
        right();
        
        }
    else   if (incoming == "hleft"){
        H_left();
        
        }
     else  if (incoming == "hright"){
        H_right();
        
        }
       else  if (incoming == "stop"){
        sttop();
        
        }
      else if (incoming == "straight"){
        stright();
        
        }
     if (incoming == "sleep"){
      toni();
      
      
      }
     if (incoming == "leftsi"){
      leftsi();
      
      
      }
     if (incoming == "rightsi"){
      rightsi();
      
      
      }
        
     
    }
 long duration, distance;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = (duration / 2) / 29.1;
 
  if (distance <= 20)
    { 
      tone(buzzer, 1500);
        digitalWrite(led,HIGH);
    delay(200);
      digitalWrite(led,LOW);
      noTone(buzzer);     
      delay(200);    
    Serial.print(distance); 
        Serial.println(""); 
    }
  
  else if (distance <= 50)
    {
    tone(buzzer, 1000);
        digitalWrite(led,HIGH);
    delay(500);
      digitalWrite(led,LOW);
      noTone(buzzer);     
      delay(500);    
    Serial.print(distance); 
        Serial.println(""); 
    }
  
  else if (distance <= 100)
    {
    tone(buzzer, 800);
        digitalWrite(led,HIGH);
    delay(1000);
      digitalWrite(led,LOW);
      noTone(buzzer);     
      delay(1000);    
    Serial.print(distance); 
        Serial.println(""); 
    }
  
  else{
    digitalWrite(buzzer,LOW);
    Serial.print(distance);
    Serial.println("");
  }
  }
void H_left()    // hard left
{
  analogWrite(5,255);
  digitalWrite(32,HIGH);
  digitalWrite(4,LOW);

  analogWrite(26,255);
  digitalWrite(33,LOW);
  digitalWrite(12,HIGH);
}

void H_right()  // hard right
{
  analogWrite(26,255);
  digitalWrite(33,HIGH);
  digitalWrite(12,LOW);
  analogWrite(5,255);
  digitalWrite(32,LOW);
  digitalWrite(4,HIGH);
}


void left()
{
  analogWrite(5,150);
  digitalWrite(32,HIGH);
  digitalWrite(4,LOW);
  analogWrite(26,255);
  digitalWrite(33,HIGH);
  digitalWrite(12,LOW);
}

void right()
{
  analogWrite(5,255);
  digitalWrite(32,HIGH);
  digitalWrite(4,LOW);
  analogWrite(26,150);
  digitalWrite(7,HIGH);
  digitalWrite(12,LOW);
}



void stright()
{
  analogWrite(5,255);
  digitalWrite(32,HIGH);
  digitalWrite(4,LOW);
  
  analogWrite(26,255);
  digitalWrite(33,HIGH);
  digitalWrite(12,LOW);
}


void reverse()
{
  analogWrite(5,255);
  digitalWrite(32,LOW);
  digitalWrite(4,HIGH);
  analogWrite(26,255);
  digitalWrite(33,LOW);
  digitalWrite(12,HIGH); 
}

void Sttop()
{
  digitalWrite(33,HIGH);
  digitalWrite(12,HIGH);
  
  digitalWrite(32,HIGH);
  digitalWrite(4,HIGH);
}
void sttop()
{
  digitalWrite(33,HIGH);
  digitalWrite(12,HIGH);
  digitalWrite(32,HIGH);
  digitalWrite(4,HIGH);
}
void toni(){
  tone(buzzer, 400);
  delay(3000);
  noTone(buzzer);  
  }
  void leftsi(){
      digitalWrite(2,HIGH);
    }
  void rightsi(){
    digitalWrite(15,HIGH);
    }
