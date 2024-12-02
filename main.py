# main.py
import sys
from PyQt6 import QtWidgets
from main_window import MainWindow

def main():
    """
    Main function to run the application.
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()