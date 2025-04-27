import socket
import serial
import time
import csv
from pymongo import MongoClient

# UDP configuration
receiver_ip = "your-ip-address"  # Replace with your server's IP
port = 4000  

# Serial port configuration (Change COM5 to your correct port)
ser = serial.Serial('COM5', 115200, timeout=1)

mongo_uri = "your-mongodb-string"  
client = MongoClient(mongo_uri)
db = client["frequency_data"]
collection = db["logs"]

# Open CSV file to store data
csv_file = "frequency_log.csv"

with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["NTP Timestamp (ms)", "Arduino Timestamp (ms)", "Frequency (Hz)"])

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Streaming frequency data to {receiver_ip}:{port}...")

while True:
    try:
        line_data = ser.readline().decode(errors='ignore').strip()
        if not line_data:
            continue  # Skip empty lines

        if "Frequency" in line_data:
            # Get timestamps
            ntp_timestamp = time.strftime("%Y-%m-%d %H:%M:%S") + f".{int(time.time() * 1000) % 1000:03d}"

            # Extract Arduino timestamp and frequency
            try:
                arduino_timestamp, frequency = line_data.split(" ms, Frequency: ")
                frequency = float(frequency.replace(" Hz", "").strip())  # Convert to float
                arduino_timestamp = int(arduino_timestamp.strip())  # Convert to int
            except ValueError:
                continue  # Skip invalid lines

            # Write to CSV
            with open(csv_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([ntp_timestamp, arduino_timestamp, f"{frequency:.4f}"])
            
            collection.insert_one({
                "ntp_timestamp": ntp_timestamp,
                "arduino_timestamp_ms": arduino_timestamp,
                "frequency_hz": frequency
            })

            # Format data as a string and send over UDP
            message = f"{ntp_timestamp}, {arduino_timestamp} ms, {frequency:.4f} Hz"
            udp_socket.sendto(message.encode(), (receiver_ip, port))
            print("Sent:", message)  # Debugging

    except KeyboardInterrupt:
        print("Stopping sender...")
        break

# Close connections
ser.close()
udp_socket.close()
client.close()
print("UDP sender stopped.")