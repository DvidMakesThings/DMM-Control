# main.py
import sys
import time
import json
from PyQt6 import QtWidgets
from main_window_ui import Ui_Widget
from measurement import Measurement
import pyvisa


class MainWindow(QtWidgets.QWidget, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resource_manager = pyvisa.ResourceManager('@py')
        self.usb_device = None
        self.measurement = None

        # Load device configuration from devices.json
        with open('devices/devices.json', 'r') as file:
            self.devices = json.load(file)

        # Populate device menu
        self.DeviceMenu.addItems(self.devices.keys())

        # Populate measurement type menu
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
            self.AvgEdit.clear()
            self.IntervalEdit.clear()

    def connect_device(self):
        device_name = self.DeviceMenu.currentText()
        if device_name:
            device_info = self.devices[device_name]
            self.usb_device = self.resource_manager.open_resource(device_info["resource"], timeout=device_info["timeout"])
            identification = self.usb_device.query("*IDN?")
            self.fill_device_info(identification)
            self.measurement = Measurement(self.usb_device)
        else:
            self.clear_device_info()

    def fill_device_info(self, identification):
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
        self.DeviceIdText.clear()
        self.DeviceText.clear()
        self.SNText.clear()
        self.SoftwareText.clear()
        self.HardwareText.clear()

    def perform_measurement(self):
        if not self.usb_device:
            self.statusView.clear()
            self.statusView.append("Error: No device selected or connected.")
            self.clear_device_info()
            return

        if self.measurement:
            # Clear the status view
            self.statusView.clear()
            self.statusView.append("Starting measurement...")

            if self.AvgBox.isChecked():
                self.AvgEdit.setEnabled(True)
                self.IntervalEdit.setEnabled(True)
                num_measurements = int(self.AvgEdit.text()) if self.AvgEdit.text() else 10
                interval_seconds = float(self.IntervalEdit.text()) / 1000 if self.IntervalEdit.text() else 0.5
            else:
                self.AvgEdit.setEnabled(False)
                self.IntervalEdit.setEnabled(False)
                num_measurements = 1
                interval_seconds = 0.5

            self.statusView.append(f"Number of measurements: {num_measurements}")
            self.statusView.append(f"Interval: {interval_seconds * 1000} ms")

            measurement_type = self.MeastypeMenu.currentText()
            try:
                if measurement_type == "Voltage":
                    self.measurement.measure_voltage(num_measurements, interval_seconds)
                elif measurement_type == "Resistance":
                    self.measurement.measure_resistance(num_measurements, interval_seconds)
                elif measurement_type == "Diode":
                    self.measurement.measure_diode(num_measurements, interval_seconds)
                else:
                    self.statusView.append("Error: Unknown measurement type.")
                    return

                self.measurement.print_average()
                self.usb_device.close()
                self.statusView.append("Measurement completed.")
            except Exception as e:
                self.statusView.append(f"Error: {str(e)}")
                self.clear_device_info()

    def copy_measurement(self):
        # Implement copy functionality
        pass

    def save_measurement(self):
        # Implement save functionality
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()