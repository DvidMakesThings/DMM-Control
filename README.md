# DMM-Control

## Features
- Automates DMM measurements.
- Possibility to calculate the average of multiple measurements.
- Supports multiple measurement devices (currently supports BK Precision 5493C).
- Selectable measurement types: DC Voltage, Resistance, Diode.

## Requirements
- Python 3.x
- `pyvisa` library
- `PyQt6` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DvidMakesThings/DMM-Control.git
    cd DMM-Control
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Ensure your measurement device is connected.
2. Run the script:
    ```sh
    python main.py
    ```
3. Select the device from the `DeviceMenu`.
4. Select the measurement type from the `MeastypeMenu`.
5. (Optional) Check the `AvgBox` to enable averaging and set the number of measurements and interval.
6. Click the `Start` button to begin the measurement.
7. The status messages and measurement data will appear in the `statusView`.

## License
This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or feedback, please contact:
- Email: [s.dvid@hotmail.com](mailto:s.dvid@hotmail.com)
- GitHub: [DvidMakesThings](https://github.com/DvidMakesThings)