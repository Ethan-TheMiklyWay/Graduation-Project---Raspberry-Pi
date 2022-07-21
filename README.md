### Introduction

This is my undergraduate graduation project. There are 4 parts of my project, which are: Data acquisition and transmission in Nodemcu node and programmed by Lua. Data receiving and forwarding in Raspberry Pi. Client interface development. Design communication protocol.

### Background Information

Precision agriculture can help manage agriculture data and increase the production. In order to increase crop yield and farmers' income, information technology has been widely used in agricultural production. This project designed a set of distributed information collection system based on NodeMCU and Raspberry Pi. Here is the top architecture of the system.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/structure.png">
</div>

- NodeMCU, as a single chip computer, it connected with the sensor DHT11 directly. I designed a program that can automatically detect and connect LAN WiFi, detect and connect MQTT server, read and transmit DHT11 sensor data through Lua scripting language 
- Raspberry PI is a server to set up mosquito, which is a MQTT communications server. It will automatically detect the NodeMCU device on the LAN, and store and show the data transmitted by NodeMCU. At the same time, It opens the TCP communication protocol, parse and execute the data from the client, and transmit the data in the same time. 
- As the most upstream platform, Client software will store and show the data. When accessing the Raspberry PI LAN, the client software will automatically connects to the Raspberry PI device, obtaining data, and control the NodeMCU device.

Here is the technical route of my works:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/technique_route.png">
</div>

### NodeMCU Design

NodeMCU is an open source Internet of Things (IoT) platform based on the ESP8266 single-chip. It has WiFi module that can transfer data by wireless network. It support many network communication protocal. DHT11 is a temperature and moisture sensor, and can be linked to NodeMCU. So, I use DHT11 as data acquisition tool in this project.

Harsh environment will have a great impact on the signal transmission process. Traditional signal transmission protocol is expensive, so it is not suitable for agricultural scenes, which have large scale and poor signal environment. While message queue telemetry transmission (MQTT) protocol is more suitable, because MQTT protocol is a lightweight, simple, open and easy to implement. These characteristics make it applicable to a wide range of applications. In this project, MQTT will be used to transmit data between sensors (DHT11 link to NodeMCU) in farmland and raspberry PI.

In this part, I will design the the program running in NodeMCU. There are 4 essential functions, which are:

- WiFi status monitor: ensure WiFi is connected, and it will auto connected if WiFi disconnected.
- Acquire MQTT server ip address automatically.
- Sensor data acquisition, transmission and sensor identification
- Sensor parameter acquisition and control

#### WiFi Status Monitor

The WiFi connection module in Lua scripting language is non-blocking connection, that is, the following code will continue to execute after the WiFi connection function is called, and the execution will not wait for the WiFi connection to complete. This also makes the design of the program difficult, each operation needs to judge whether the WiFi connection is successful. Lua language development programs mostly use timer TMR to achieve robust programming. Timers are the only way to achieve multithreading in Lua. Timers can be used for non-blocking function operations and periodic function execution operations. Therefore, how to build the timer's switching operation is at the heart of NodeMCU's programming.

Here is my design:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/NodeMCU/NodeMCU_structure.png">
</div>

#### Acquire MQTT Server IP Automatically.

Mosquitto server sends UDP broadcast every a few second. Once the broadcast is received by NodeMCU, it can locate Mosquitto server location.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/NodeMCU/Broadcast.png">
</div>

#### Sensor Parameter Acquisition

In order to make the project more convenient to user, it is necessary to design a control method to adjust the parameter remotely. This project use MQTT protocol to transmit control command.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/NodeMCU/NodeMCU_control.png">
</div>

#### Demonstration

Start data acquisition:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/NodeMCU/demonstration.png">
</div>

Set parameter, and WiFi reconnected after disconnected.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/NodeMCU/NodeMCU_WiFi.png">
</div>

### Raspberry Pi Design

In this project, raspberry Pi side needs to install Mosquitto, Python, MySQL. Set raspberry PI auto start SSH function. Raspberry PI is a intermediate node. It connects NodeMCU on the down side, and connects client on the up side. Therefore, I need to conside 3 things: 

- Storage data in Raspberry Pi
- Receive data from NodeMCU
- Send data to client

#### Data Model in Rasperberry Pi

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/Pi/Pi_data_model.png">
</div>

#### Receive Data from NodeMCU

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/Pi/Pi_parameter.png">
</div>

#### Send Data to Client

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/Pi/pi_client.png">
</div>

#### Demonstration

Here is the NodeMCU user interface. This interface was programmed by Python, tkinter.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/Pi/interface.png">
</div>

This is the load test. According to the test, 7 NodeMCU could work well in the same LAN.

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/Pi/load.png">
</div>

### Client Design

In the client side, the main function is store and show data, send instruction to NodeMCU. Here is the data model:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/client/ER.png">
</div>

Client software architecture:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/client/sequence.png">
</div>

#### Demonstration

User login interface:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/client/login.png">
</div>

Main interface:

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/client/main.png">
</div>

<div align="center">
  <img src="https://github.com/Jingxiang-Zhang/Graduation-Project---Raspberry-Pi/blob/main/img/client/main2.png">
</div>
