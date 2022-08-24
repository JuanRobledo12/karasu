# karasu

Project name: Karasu Project
Description: The project consists of two software used to control a 3DOF planar robotic arm. 

The "main.py" file is a Python program that lets the user input a coordinate (x, y) and the type of trajectory (angular or linear) 
that the robot has to take to position its end-effector in the desired position. Therefore, this software handles the forward and 
inverse kinematic equations to calculate the angle values the three robot's servomotors must take to reach the final coordinates in a 
specific trajectory. In addition, an MQTT client was implemented in the program to publish the calculated angle values into an MQTT network.

The "karasu_control.ino" file is an Arduino program used in an ESP8266 board to control the robot's servomotors. 
First, an MQTT client is created to subscribe to the topic where the angle data is being published. Then the program processes the JSON file 
where the angle values are stored. Finally, the program sets the values to the servomotors.

Dependencies:

Python: math, time, json, paho.mqtt.client.
Arduino: ArduinoJson.h, ESP8266WiFi.h, PubSubClient.h, Servo.h
