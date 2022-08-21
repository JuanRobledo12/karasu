/* KARASU CONTROL PROGRAM
 *  
Description: This program subscribes to an MQTT topic to receive JSON data with the
necessary angles for Karasu to reach certain position. The ESP8266 connects to the internet and 
to a MQTT network, then it controls the position of three servomotors with the obtained information.
Creator: Juan Antonio Robledo Lara
Last Modification: March 02 2022

 *
 */

//libraries
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>

//Servo objects
Servo joint1;
Servo joint2;
Servo joint3;

//callbacks
void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  
  // JSON handling;
  StaticJsonDocument<96> doc;
  DeserializationError error = deserializeJson(doc, payload);
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
      }
    double theta1 = doc["theta1"]; 
    double theta2 = doc["theta2"]; 
    double theta3 = doc["theta3"]; 
    Serial.println("----------Parsed Data----------");

    //servo control
    joint1.write(theta1);
    Serial.print("Theta1: ");
    Serial.println(joint1.read());

   //prevent th2 and th3 of reaching exceeding values.
    if (theta2 <= 90 || theta2 >= -90) 
    {
      joint2.write(90 - theta2);
      Serial.print("Theta2: ");
      Serial.println(joint2.read());
      }
       if (theta3<= 90 || theta3 >= -90) 
    {
      joint3.write(90 - theta3);
      Serial.print("Theta3: ");
      Serial.println(joint3.read());
      }
    
  }
  

//WiFi parameters
const char *ssid = ""; //Enter WiFi name
const char *password = ""; //Enter WiFi passoword

//client/broker parameters
const char *mqtt_broker = "";
const char *topic = "karasu/control";
String client_id = "karasu_esp8266";
const int mqtt_port = 1883; //Enter broker port

//creation of clients
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  //Serial comm
  Serial.begin(9600);

  //LED indicator parameters
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  //Servo pin declaration and setup 
  delay(3000);
  int init_steps = 30;
  joint1.attach(5, 500, 2400); //D1
  joint2.attach(4, 500, 2400); //D2
  joint3.attach(2, 500, 2400); //D4
  joint1.write(90);
  joint2.write(90);
  joint3.write(90);
  delay(1000);
  Serial.println(joint1.read());
  Serial.println(joint2.read());
  Serial.println(joint3.read());
  
  //WiFi networks connection
  delay(3000); //delay to wait opening of serial monitor
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
    }
  Serial.println("\nWiFi connected!!");
  Serial.print("Karasu_ESP8266 IP address: "); 
  Serial.println(WiFi.localIP());

  //broker connection
  client.setServer(mqtt_broker, mqtt_port);
  delay(2000);
  Serial.print("Preparing connection to broker: ");
  Serial.println(mqtt_broker);
  delay(1000);
  Serial.printf("The client **%s** is attempting to connect to the broker...\n", client_id);
  while(!client.connected())
  {
    if(client.connect(client_id.c_str()))
    {
      Serial.println("Succesful connection to broker!!");
      digitalWrite(13, HIGH);
      } else
      {
        Serial.print("failed with state ");
        Serial.println(client.state());
        delay(2000);
        }
  }
  
  //callbacks declaration
  client.setCallback(callback);

  //subscribe to topic
  Serial.println(topic);
  client.subscribe(topic); // receives message from topic
  Serial.println("------------------");
}

void loop() {
  client.loop();
}
