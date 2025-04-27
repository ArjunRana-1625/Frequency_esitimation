# Frequency_esitimation

# How to run this project 

1. Clone the Repository
   
Open your terminal and execute the following command:

git clone https://github.com/arnavb2004/Frequency_esitimation

2. Set Up the Hardware
   
Assemble the hardware as illustrated in the project report and connect the signal input to digital pin 2 of the Arduino.

3. Upload the Arduino Code

Open the Arduino IDE.

Load the file project_ee309.ino.

Verify and upload the code to your Arduino board.

4. Configure the Sender Script

Open udp_sender.py in your preferred code editor.

Update the receiver IP address and MongoDB connection string as per your setup.

5. Start the Receiver

Run the udp_reciever.py script on the receiver (server) machine.

6. Start the Sender

Run the udp_sender.py script on the sender (client) machine (the machine connected to Arduino).

7. Visualize the Data

Upon successful connection, you will be able to view the live frequency graph on the receiver (server) side.

