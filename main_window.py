import json
import random
from datetime import datetime
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from main_window_ui import Ui_Widget
from measurement import Measurement
from device_manager import DeviceManager

DEBUG = True  # Set to True for debug mode

class MainWindow(QtWidgets.QWidget, Ui_Widget):
    """
    MainWindow class inherits from QWidget and Ui_Widget.
    This class handles the GUI and the interaction with the measurement device.
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.device_manager = DeviceManager()
        self.usb_device = None
        self.measurement = None

        # Load device configuration from devices.json
        with open('devices/devices.json', 'r') as file:
            self.devices = json.load(file)

        # Populate device menu with available devices
        self.DeviceMenu.addItems(self.devices.keys())

        # Populate measurement type menu with available measurement types
        self.MeastypeMenu.addItems(["DC Voltage", "Resistance", "Diode"])
        self.MeastypeMenu.setCurrentIndex(0)  # Set default selection to "Voltage"

        # Connect signals to slots
        self.DeviceMenu.currentIndexChanged.connect(self.connect_device)
        self.StartButton.clicked.connect(self.perform_measurement)
        self.CopyButton.clicked.connect(self.copy_measurement)
        self.SaveButton.clicked.connect(self.save_measurement)

        # Set default values and connect AvgBox toggled signal
        self.AvgBox.toggled.connect(self.update_avgbox_state)
        self.update_avgbox_state()

    def update_avgbox_state(self):
        """
        Update the state of the average and interval input fields based on the AvgBox checkbox.
        """
        if self.AvgBox.isChecked():
            self.AvgEdit.setEnabled(True)
            self.IntervalEdit.setEnabled(True)
            if not self.AvgEdit.text():
                self.AvgEdit.setText("10")
            if not self.IntervalEdit.text():
                self.IntervalEdit.setText("500")
        else:
            self.AvgEdit.setEnabled(False)
            self.IntervalEdit.setEnabled(False)
            self.AvgEdit.setText("1")
            self.IntervalEdit.clear()

    def connect_device(self):
        """
        Connect to the selected device from the device menu.
        """
        device_name = self.DeviceMenu.currentText()
        if device_name:
            device_info = self.devices[device_name]
            self.usb_device = self.device_manager.connect_device(device_info)
            identification = self.usb_device.query("*IDN?")
            self.fill_device_info(identification)
            self.measurement = Measurement(self.usb_device)
        else:
            self.clear_device_info()

    def fill_device_info(self, identification):
        """
        Fill the device information fields with the identification string.
        """
        parts = identification.split(',')
        if len(parts) >= 5:
            self.DeviceIdText.setText(parts[0])
            self.DeviceText.setText(parts[1])
            self.SNText.setText(parts[2])
            self.SoftwareText.setText(parts[3])
            self.HardwareText.setText(parts[4])
        else:
            self.clear_device_info()

    def clear_device_info(self):
        """
        Clear the device information fields.
        """
        self.DeviceIdText.clear()
        self.DeviceText.clear()
        self.SNText.clear()
        self.SoftwareText.clear()
        self.HardwareText.clear()

    def perform_measurement(self):
        """
        Perform the measurement based on the selected measurement type and settings.
        """
        if not self.usb_device and not DEBUG:
            self.statusView.clear()
            self.statusView.append("Error: No device selected or connected.")
            self.clear_device_info()
            return

        if not self.measurement:
            self.measurement = Measurement(self.usb_device)

        # Clear the measured values list
        self.measurement.measured_values.clear()

        # Get device details
        # Clear the status view
        self.statusView.clear()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.statusView.append(f"Date and Time: {current_time}\n")
        device_details = (
            f"Device ID: {self.DeviceIdText.text()}\n"
            f"Device: {self.DeviceText.text()}\n"
            f"Serial Number: {self.SNText.text()}\n"
            f"Software Version: {self.SoftwareText.text()}\n"
            f"Hardware Version: {self.HardwareText.text()}\n"
        )
        self.statusView.append(device_details)

        # Determine the number of measurements and interval based on AvgBox state
        if self.AvgBox.isChecked():
            self.AvgEdit.setEnabled(True)
            self.IntervalEdit.setEnabled(True)
            if not self.AvgEdit.text().isdigit():
                self.statusView.append("Error: Please enter a valid number for measurement count.")
                return
            num_measurements = int(self.AvgEdit.text())
            interval_seconds = float(self.IntervalEdit.text()) / 1000 if self.IntervalEdit.text() else 0.5
        else:
            self.AvgEdit.setEnabled(False)
            self.IntervalEdit.setEnabled(False)
            num_measurements = 1
            interval_seconds = 0.5

        measurement_type = self.MeastypeMenu.currentText()
        self.statusView.append(f"Selected measurement type: {measurement_type}")
        self.statusView.append(f"Number of measurements: {num_measurements}")
        self.statusView.append(f"Interval: {interval_seconds * 1000} ms\n")
        self.statusView.append("####################################################")
        self.statusView.append("Starting measurement...\n")

        progress_increment = 100 / num_measurements

        # Determine the unit based on the measurement type
        if measurement_type == "DC Voltage":
            unit = "V"
        elif measurement_type == "Resistance":
            unit = "Ohm"
        elif measurement_type == "Diode":
            unit = "V"
        else:
            self.statusView.append("Error: Unknown measurement type.")
            return

        try:
            # Perform the measurements and update the progress bar
            for i in range(num_measurements):
                if DEBUG:
                    measured_value = random.uniform(0, 10)  # Generate random voltage for debug
                    self.measurement.measured_values.append(measured_value)
                    self.statusView.append(f"Measurement {i + 1}: {measured_value:.5f} {unit}")
                else:
                    if measurement_type == "DC Voltage":
                        self.measurement.measure_voltage(1, interval_seconds)
                    elif measurement_type == "Resistance":
                        self.measurement.measure_resistance(1, interval_seconds)
                    elif measurement_type == "Diode":
                        self.measurement.measure_diode(1, interval_seconds)
                    else:
                        self.statusView.append("Error: Unknown measurement type.")
                        return

                self.progressBar.setValue(int((i + 1) * progress_increment))

            # Print the average of the measurements and close the device connection
            average_value = round(sum(self.measurement.measured_values) / len(self.measurement.measured_values), 5)
            self.statusView.append(f"\nAverage Value: {average_value} {unit}\n")
            self.lcdNumber.display(average_value)  # Display the average value on the LCD number
            if not DEBUG:
                self.usb_device.close()
            self.statusView.append("<span style='color: green;'>Measurement completed.</span>")
            self.progressBar.setValue(0)
        except Exception as e:
            self.statusView.append(f"Error: {str(e)}")
            self.clear_device_info()

    def copy_measurement(self):
        """
        Copy the measurement results to the clipboard.
        """
        # Implement copy functionality
        pass

    def save_measurement(self):
        """
        Save the measurement results to a file.
        """
        if not self.measurement or not self.measurement.measured_values:
            self.statusView.append("Error: No measurement data to save.")
            return

        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Get the measurement type
        measurement_type = self.MeastypeMenu.currentText().replace(" ", "_")
        # Create the default file name
        default_file_name = f"{measurement_type}_measurement_{current_time}.txt"

        # Open the file dialog with the default file name
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Measurement Data", default_file_name, "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as file:  # Open the file in write mode
                    # Write date and time
                    file.write(f"Measurement done at: {current_time}\n")
                    # Write device details
                    device_details = (
                        f"Device ID: {self.DeviceIdText.text()}\n"
                        f"Device: {self.DeviceText.text()}\n"
                        f"Serial Number: {self.SNText.text()}\n"
                        f"Software Version: {self.SoftwareText.text()}\n"
                        f"Hardware Version: {self.HardwareText.text()}\n\n"
                    )
                    file.write(device_details)
                    file.write(f"Measurement Type: {measurement_type.replace('_', ' ')}\n")
                    file.write(f"Number of measurements: {len(self.measurement.measured_values)}\n")
                    file.write(f"Interval: {float(self.IntervalEdit.text()) if self.IntervalEdit.text() else 500} ms\n\n")

                    # Write measurement values
                    for value in self.measurement.measured_values:
                        file.write(f"{value}\n")
                    # Calculate and write the average value
                    average_value = round(sum(self.measurement.measured_values) / len(self.measurement.measured_values), 5)
                    file.write(f"\nAverage Value: {average_value}\n")
                self.statusView.append(f"\nMeasurement data saved to {file_path}")
            except Exception as e:
                self.statusView.append(f"Error saving measurement data: {str(e)}")