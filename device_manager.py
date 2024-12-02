# device_manager.py
import pyvisa

class DeviceManager:
    """
    DeviceManager class handles the connection to the measurement devices.
    """
    def __init__(self):
        self.resource_manager = pyvisa.ResourceManager('@py')

    def connect_device(self, device_info):
        """
        Connect to the device using the provided device information.
        """
        return self.resource_manager.open_resource(device_info["resource"], timeout=device_info["timeout"])