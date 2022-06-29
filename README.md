# Yoga_Tech2022
# About the Project
   Application of sensors in Healthcare has been rapidly increasing these days. Collection of data from sensors which can be placed on various parts of our body,         transmitting this data wirelessly to a device which we can carry along with us and then displaying the state of our body parameters has made our lives easier. We, the Biomedical Engineering department at IIT Hyderabad demonstrated how technology can be used in yoga. I had made a sensor based prototype which determines expansion and contraction of our chest and thorax. The data is collected and transmitted over the server. Having done that, It was used for analysis.
# Schematic
![Schematic_fsr](https://user-images.githubusercontent.com/108401638/176477849-1ffc0155-413c-49eb-8fa0-fc44dcd8d217.png)
# Technology Stack
Server : Python Websocket Server(Based on Asyncio Library)
Hardware: FSR(Force Sensitive Resistance) sensor, Esp module, connecting wires, resistors, potentiometer.
Libraries: ArduinoJSON for sending sensor data in JSON format, Arduino Websocket Client, WiFi.h for connecting to WiFi, Websockets and websocket-client libraries in Python
IDE: Arduino IDE, VS code
Programming languages: Embedded C, Python3
# Setup
1) I had run the python server after installing "websockets" and "websocket-client" libraries.
2) After ensuring that the server is switched, burn the code(which is present in the sensor_clients folder) for the desired sensor on connecting the sensor to ESP32 and using Arduino IDE.
3) The server currently runs to collect information posted from fsr sensor simultaneously at a speed of nearly 250 samples/second.
4) The flask server collects 8 samples of sensor data per second. 
# results
X-axis represents time for the sensor and Y-axis represents  sensor output voltage FSR.
![result_fsr](https://user-images.githubusercontent.com/108401638/176480224-73aabf72-a10e-491d-9c01-28e413be3f03.png)

PLot of data collected from the FSR sensor:
![image](https://user-images.githubusercontent.com/108401638/176480646-27b1529d-4f5a-4872-b32f-1233b8e4c834.png)

Other sensors used in this project were GSR sensor, EMG and pressure sensing unit placed on yoga mat
results were as follows:
plot of EMG data:
 ![EMG_plot](https://user-images.githubusercontent.com/108401638/176481559-659b7bfd-6d5c-47ca-9d2c-676234892941.png)
plot of data collected from the GSR sensor:
 ![GSR_data](https://user-images.githubusercontent.com/108401638/176481885-ea1ce324-2c31-4b50-9e20-87513a6848c4.png)
results  obtained from yoga mat:
![HeatMap_yogaMat](https://user-images.githubusercontent.com/108401638/176482172-3c456a35-548c-4904-8d85-824847f8d7b2.png)

# Schematic of the whole project
![Schematic_wholeProject](https://user-images.githubusercontent.com/108401638/176482495-925978e7-53dc-4f6f-a473-c8890410a710.png)

