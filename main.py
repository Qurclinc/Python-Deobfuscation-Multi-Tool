import sys
import screeninfo

from PyQt5.QtWidgets import QApplication
from Windows.MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()