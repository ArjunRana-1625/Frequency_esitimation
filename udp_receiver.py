import socket
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# UDP Configuration
host = "0.0.0.0"
port = 4000

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((host, port))

print(f"Listening for frequency data on port {port}...")

csv_file = "received_data.csv"
file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

# Initialize matplotlib
plt.ion()
fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
ax.set_title("Real-Time Frequency vs Arduino Timestamp", fontsize=14)
ax.set_xlabel("Arduino Timestamp (ms)", fontsize=12)
ax.set_ylabel("Frequency (Hz)", fontsize=12)
def format_func(value, tick_number):
    return f"{value:.4f}"  # 4 decimal places

ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_func))
line, = ax.plot([], [], 'b-', marker='o', markersize=4, linewidth=1.5, label="Frequency")
plt.legend(fontsize=12)
plt.grid()

# Data storage
timestamps = []
frequencies = []
TIME_WINDOW_MS = 1000  # Show last 1 seconds of data

def update_plot():
    if len(timestamps) < 2:
        return
    latest = timestamps[-1]
    start = latest - TIME_WINDOW_MS
    while timestamps and timestamps[0] < start:
        timestamps.pop(0)
        frequencies.pop(0)
    ax.set_xlim(start, latest)
    ax.set_ylim(min(frequencies) - 0.1, max(frequencies) + 0.1)
    line.set_xdata(timestamps)
    line.set_ydata(frequencies)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.1)

try:
    while True:
        data, addr = udp_socket.recvfrom(1024)
        message = data.decode().strip()
        if not message:
            continue
        print(f"Received: {message}")

        try:
            ntp_ts, arduino_ts, freq_str = message.split(", ")
            frequency = float(freq_str.replace(" Hz", ""))
            arduino_ts = int(arduino_ts.replace(" ms", ""))
        except ValueError:
            print("Warning: malformed data, skipping...")
            continue

        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["NTP Timestamp (ms)", "Arduino Timestamp (ms)", "Frequency (Hz)"])
                file_exists = True
            writer.writerow([ntp_ts, arduino_ts, f"{frequency:.4f}"])

        timestamps.append(arduino_ts)
        frequencies.append(frequency)
        update_plot()

except KeyboardInterrupt:
    print("Stopping receiver...")

plt.ioff()
plt.show()
udp_socket.close()

print("Receiver stopped.")
