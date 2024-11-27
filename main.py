# main.py
import time
from measurement import Measurement
import pyvisa


def main():
    # Connect to the BK Precision 5493C device
    resource_manager = pyvisa.ResourceManager()
    usb_device = resource_manager.open_resource("USB0::0x3121::0x5001::W111228111::INSTR",
                                                timeout=10000)  # Set timeout to 10 seconds

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
