# measurement.py
import time


class Measurement:
    def __init__(self, usb_device):
        self.usb_device = usb_device
        self.measured_values = []

    def measure_voltage(self, num_measurements, interval_seconds):
        for measurement_number in range(1, num_measurements + 1):
            self.usb_device.write(":MEASure:VOLTage:DC?")
            self._trigger_measurement(interval_seconds)
            measured_voltage = float(self.usb_device.query(":FETCh?"))
            self._process_measurement(measured_voltage, measurement_number, "V")

    def measure_resistance(self, num_measurements, interval_seconds):
        for measurement_number in range(1, num_measurements + 1):
            self.usb_device.write(":MEASure:RESistance? AUTO")
            self._trigger_measurement(interval_seconds)
            measured_resistance = float(self.usb_device.query(":FETCh?"))
            self._process_measurement(measured_resistance, measurement_number, "Ohms")

    def measure_diode(self, num_measurements, interval_seconds):
        for measurement_number in range(1, num_measurements + 1):
            self.usb_device.write(":MEASure:DIODe?")
            self._trigger_measurement(interval_seconds)
            measured_diode_voltage = float(self.usb_device.query(":FETCh?"))
            self._process_measurement(measured_diode_voltage, measurement_number, "V (Diode)")

    def _trigger_measurement(self, interval_seconds):
        self.usb_device.write(":TRIGger:SINGle")
        time.sleep(interval_seconds)

    def _process_measurement(self, measured_value, measurement_number, unit):
        self.measured_values.append(measured_value)
        print(f"Measurement {measurement_number}:\t {measured_value:.5f} {unit}")

    def print_average(self):
        average_value = round(sum(self.measured_values) / len(self.measured_values), 5)
        print(f"Average Value: {average_value}")
        print("Measurement complete.")
