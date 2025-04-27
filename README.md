# Frequency_esitimation
Assemble the circuit for Frequency Estimation and connect the output to PIN 2 of the Arduinio IDE
Connect the Arduino to your computer and compile and upload the "project_ee309.ino" code on the Arduino using the Arduino IDE application
Once the code is loaded run the "udp_sender.py" code on the same computer you have connected the Arduino to
Update the "udp_sender.py" code with the IP address of the reciever you want to send the code too as well as the port to which your Arduino is connected
Now after running the sender code take another device on which you want to recieve the code and run the "udp_reciever.py"
After a few seconds the graph and data will be recieved on the 2nd device
