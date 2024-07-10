import csv
import serial
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
import pandas as pd

class DataAQ:
    def __init__(self, filename='fsr', serial_port='/dev/tty.usbserial-0001', baud_rate=115200):
        self.filename = filename
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.file = f'{self.filename}.csv'

        # Check if the file already exists and plot its contents if it does
        if os.path.exists(self.file):
            print(f"File '{self.file}' already exists.")
            self.plot_existing_data()
        else:
            self.record_and_save_data()

    def plot_existing_data(self):
        df = pd.read_csv(self.file)
        plt.figure(figsize=(15, 3))  # Adjust figure size as needed
        df.plot(ax=plt.gca())  # Adjust x_column and y_column
        plt.xlabel('Samples')  # Replace with actual labels
        plt.ylabel('Amplitude')  # Replace with actual labels
        plt.title(self.file)  # Replace with actual title
        plt.show()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def record_data(self, duration, label_name, label_num):
        # Open serial port
        ser = serial.Serial(self.serial_port, baudrate=self.baud_rate)

        # Initialize list to store data
        data_rows = []

        # Record data for the specified duration
        start_time = time.time()
        with tqdm(total=duration, desc=f'Recording for label {label_name}') as pbar:
            while time.time() - start_time < duration:
                # Read data from serial port
                line = ser.readline().decode().strip()
                data = line.split(',')  # Assuming data is comma-separated

                # Filter out and record only the integer or float values
                filtered_data = [x for x in data if self.is_number(x)]

                # Append filtered data to list
                data_rows.append([label_num, label_name] + filtered_data)
                pbar.update(1)

        # Close serial port
        ser.close()

        # Calculate sampling frequency
        num_samples = len(data_rows)
        sampling_freq = num_samples / duration

        # Print sampling frequency and number of samples recorded
        print(f"Sampling frequency for label {label_name}: {sampling_freq} Hz")
        print(f"Number of samples recorded for label {label_name}: {num_samples}")

        return data_rows, sampling_freq

    def record_and_save_data(self):
        # Get duration for data recording
        duration = int(input("Enter the duration for data recording (in seconds): "))

        # Initialize label number
        label_num = 0

        # Initialize dictionary to store label data and list to store sampling frequencies
        label_data_dict = {}
        sampling_freqs = []

        while True:
            # Get label name from user input
            label_name = input("Enter the label name: ")

            # Record data for the label
            label_data, sampling_freq = self.record_data(duration, label_name, label_num)

            # Add label data and sampling frequency to dictionary and list
            label_data_dict[label_name] = (label_num, label_data)
            sampling_freqs.append(sampling_freq)

            # Ask if the data is recorded correctly
            correct = input("Is the data recorded correctly? (y/n): ")
            if correct.lower() != 'y':
                del label_data_dict[label_name]
                sampling_freqs.pop()
                continue

            # Increment label number
            label_num += 1

            # Ask if the user wants to record another label
            another_label = input("Do you want to record another label? (y/n): ")
            if another_label.lower() != 'y':
                break

        # Calculate the average sampling frequency
        average_sampling_freq = sum(sampling_freqs) / len(sampling_freqs)

        # Print recorded labels and their respective label names
        print("Recorded labels:")
        for label_name, (label_num, _) in label_data_dict.items():
            print(f"Label {label_num}: {label_name}")

        # Save all data to CSV file
        file_name = f"{self.filename}_{average_sampling_freq:.2f}.csv"
        with open(file_name, 'w', newline='') as csvfile:
            # Initialize CSV writer
            writer = csv.writer(csvfile)

            # Write header
            header = [f'channel_{i+1}' for i in range(len(label_data_dict[next(iter(label_data_dict))][1][0])-2)]  # Exclude label and label_name columns
            writer.writerow(['label', 'label_name'] + header)

            # Write data rows
            for label_name, (_, label_data) in label_data_dict.items():
                for data_row in label_data:
                    writer.writerow(data_row)

        print(f"Average sampling frequency of the recorded file: {average_sampling_freq:.2f} Hz")
        print("")
        print(f"All data recorded successfully and saved as '{file_name}'")

