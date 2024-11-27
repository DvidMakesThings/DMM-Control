# main.py
import time
import json
from measurement import Measurement
import pyvisa


def main():
    # Load device configuration from devices.json
    with open('devices/devices.json', 'r') as file:
        devices = json.load(file)

    # Connect to the BK Precision 5493C device
    device_info = devices["BK_Precision_5493C"]
    resource_manager = pyvisa.ResourceManager()
    usb_device = resource_manager.open_resource(device_info["resource_string"],
                                                timeout=device_info["timeout"])  # Set timeout to 10 seconds

    # Query and print the instrument identification
    identification = usb_device.query("*IDN?")
    print(f"Instrument Identification: {identification}")

    # User-selectable parameters
    # num_measurements = int(input("Enter the number of measurements: "))
    # interval_seconds = float(input("Enter the interval between measurements (seconds): "))

    time.sleep(5)

    # Create Measurement object
    measurement = Measurement(usb_device)

    # Perform voltage measurements and calculate average
    # measurement.measure_voltage(num_measurements, interval_seconds)
    measurement.measure_voltage(20, 0.5)

    # Perform resistance measurements and calculate average
    # measurement.measure_resistance(20, 0.5)

    # Print average for both measurements
    measurement.print_average()

    # Close the connection
    usb_device.close()


if __name__ == "__main__":
    main()