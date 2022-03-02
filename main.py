###Karasu Main Program###
#Description: This program calculates the necessary angles to reach a desired position with Karasu.
#The program publish the calculated values in JSON to a MQTT topic in a MQTT network.
#The program can perform linear and angular interpolations for the robot's motion.
#Creator: Juan Antonio Robledo Lara
#Last Modofication: March 02 2022
#Github Repository: 

#libraries
import math
import time
import json
import paho.mqtt.client as mqtt

#globals
global link1_len
global link2_len
global link3_len

#MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Succesful connection! rc = ", str(rc))
    else:
        print("Unable to connect, rc = ", str(rc))
        quit_program()
def on_disconnect(client, userdata, rc):
    print("Connection lost, rc = ", str(rc))

#functions
def quit_program():
     print("Quitting program...")
     client.loop_stop()
     time.sleep(4)
     exit()
    
def inversekin(x_coor, y_coor, alfa_val, sing_flag):
    link2_x = x_coor - link3_len * math.cos(alfa_val)
    link2_y = y_coor - link3_len * math.sin(alfa_val)
    costh2 = (pow(link2_x, 2) + pow(link2_y, 2) - pow(link1_len, 2) - pow(link2_len, 2) ) / (2 * link1_len * link2_len)
    try:
        if sing_flag == True:
            sinth2 = -1* math.sqrt(1 - pow(costh2, 2))
        elif sing_flag == False:
            sinth2 = math.sqrt(1 - pow(costh2, 2))
    except:
        print("Unreachable location: calculation of sinth2 has imaginary solutions.\n Try modifying Alfa...")
        quit_program()
    den_x = (pow(link1_len + link2_len * costh2, 2) + pow(link2_len, 2) * pow(sinth2, 2))
    costh1 = (link2_x * (link1_len + link2_len * costh2) + (link2_y * link2_len * sinth2)) / den_x
    sinth1 = (link2_y * (link1_len + link2_len * costh2) - (link2_x * link2_len * sinth2)) / den_x
    th1 = math.atan2(sinth1, costh1)
    th2 = math.atan2(sinth2, costh2)
    th3 = alfa_val - th1 - th2
    joint_pos = dict()
    joint_pos['theta1'] = math.degrees(th1)
    joint_pos['theta2'] = math.degrees(th2)
    joint_pos['theta3'] = math.degrees(th3)
    return(joint_pos)
def inversekin_singcheck(x_coor, y_coor, alfa_val):
    ang_val = inversekin(x_coor, y_coor, alfa_val, False)
    count_val = 0 
    while True:
        if ang_val['theta3'] > 180 or  ang_val['theta3'] < -180:
            ang_val = inversekin(x_coor, y_coor, alfa_val, True)
            print("Negative Sinth2 was used")
            count_val = count_val + 1
        if count_val == 0:
            break
        elif count_val > 1:
            print("theta 3 exceeds the permissible values, Theta3: ", ang_val['theta3'])
            print("Try angular interpolation instead if using linear")
            quit_program()      
    return(ang_val)
def lin_ang_interpol(init_val, fin_val, step_par):
    val = init_val + step_par * (fin_val - init_val)
    return(val)

#Welcome
print("Welcome to the Karasu Control Software!")
time.sleep(2)

#MQTT client/broker parameters
client_id = "karasu_control"
broker_ad = "" #Write your broker IP address or Host name here
topic_id = "karasu/control"
client = mqtt.Client(client_id)

#MQTT Callbacks declaration
client.on_connect = on_connect
client.on_disconnect = on_disconnect

#MQTT broker connection
print("Attempting to connect to ", broker_ad, "as", client_id)
time.sleep(1)
try:
    client.connect(broker_ad, port=1883, keepalive=60)
    client.loop_start()
    time.sleep(1)
    print("Starting Karasu Control Software...")
except:
    print("Connection failed, check broker status or port")
    quit_program()

#karasu parameters (Change it to your robot parameters)
link1_len = 6.997
link2_len = 6.7
link3_len = 5.195
inter_steps = 30
conn_sleeptime = 0.050 #sleep time between publishing data to topic

#initial positioning (Change it to your robot parameters)
xinit_coor = 0
yinit_coor = 18.892
init_alfa = math.radians(90)

#user input
while True:
    print("Input the new location and positioning of the robot...")
    xfin_coor = float(input("X: "))
    yfin_coor = float(input("Y: "))
    fin_alfa = math.radians(float(input("Alfa: ")))

#Choose interpolation type
    interpo_type = None
    time.sleep(2)
    while True:
        interpo_type = input("Type the intepolation method you want to use (linear / angular): ")
        if interpo_type == 'angular':
            print("You have selected ANGULAR interpolation...")
            init_ang_val = inversekin_singcheck(xinit_coor, yinit_coor, init_alfa)
            final_ang_val = inversekin_singcheck(xfin_coor, yfin_coor, fin_alfa)
            time.sleep(2)
            set_values = dict()
            break
        elif interpo_type == 'linear':
            print("You have selected LINEAR interpolation...")
            time.sleep(2)
            break

#Positioning calculation (interpolations)
    print("----------------\nKarasu is in movement...")
    for step in range (0, inter_steps + 1):
        if interpo_type == 'angular':
            set_values["theta1"] = lin_ang_interpol(init_ang_val['theta1'],final_ang_val['theta1'], step/inter_steps)
            set_values["theta2"] = lin_ang_interpol(init_ang_val['theta2'],final_ang_val['theta2'], step/inter_steps)
            set_values["theta3"] = lin_ang_interpol(init_ang_val['theta3'],final_ang_val['theta3'], step/inter_steps)
            for i in range(1, 4):
                if set_values["theta" + str(i)] > 180 or set_values["theta" + str(i)] < -180:
                    print("Theta ", str(i), "Exceeds permissible values, th: ", set_values["theta" + str(i)])
                    quit_program()
            json_angles = json.dumps(set_values, indent=4)
            client.publish(topic_id, payload=json_angles)
            time.sleep(conn_sleeptime)
        elif interpo_type == 'linear':
            current_x = lin_ang_interpol(xinit_coor, xfin_coor, step/inter_steps)
            current_y = lin_ang_interpol(yinit_coor, yfin_coor, step/inter_steps)
            current_alfa = lin_ang_interpol(init_alfa, fin_alfa, step/inter_steps)
            #print("Coordinates: ",current_x, current_y)
            curr_ang_val = inversekin_singcheck(current_x, current_y, current_alfa)
            json_angles = json.dumps(curr_ang_val, indent=4)
            client.publish(topic_id, payload=json_angles)
            time.sleep(conn_sleeptime)

#quit program question
    time.sleep(1)
    print("Desired position has been reached!!!\n----------------")
    time.sleep(1)
    quit_val = input("Do you want to input a new position? (yes/no): ")
    while True:
        if quit_val == "no":
            set_values = dict()
            set_values["theta1"] = 90
            set_values["theta2"] = 0
            set_values["theta3"] = 0
            json_angles = json.dumps(set_values, indent=4)
            client.publish(topic_id, payload=json_angles)
            quit_program()
        elif quit_val == "yes":
            break

#set new init values
    xinit_coor = xfin_coor
    yinit_coor = yfin_coor
    init_alfa = fin_alfa
    

 


