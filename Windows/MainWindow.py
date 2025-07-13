import screeninfo
import os
import subprocess

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from src.Ui_MainWindow import Ui_MainWindow
from Windows.CriticalWindow import CriticalWindow
from Windows.SuccessWindow import SuccessWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        size = screeninfo.get_monitors()[0]
        WIDTH, HEIGHT = 800, 600
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setGeometry(int(size.width / 2 - (WIDTH / 2)), int(size.height / 2 - (HEIGHT / 2)), WIDTH, HEIGHT)
        self.setFixedSize(WIDTH, HEIGHT)
        self.source_file = ""
        self.destination_file = ""
        self.ui.deobfuscate_btn.setText("Деобфусцировать")
        self.ui.selectFile_btn.setText("Выбрать файл")
        
        self.ui.selectFile_btn.clicked.connect(self.open_file)
        self.ui.deobfuscate_btn.clicked.connect(self.deobfuscate)

    
    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Python Files (*.py)")
        if filepath:
            self.source_file = os.path.abspath(filepath)
            with open(self.source_file, "r") as f:
                self.ui.textspace_edit.setPlainText("\n".join(line.strip() for line in f.readlines()))
                self.ui.filename_label.setText(f"Текущий файл: {os.path.basename(self.source_file)}")

    def get_destination(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Выберите файл", "Output/decoded.py", "Python Files (*.py)")
        if filepath:
            self.destination_file = os.path.abspath(f"{filepath}") 

    def deobfuscate(self):
        if (not(self.source_file)):
            CriticalWindow("Ошибка деобфускации", "Сначала выберите входной файл!").exec()
            return
        else:
            self.get_destination()
            print(self.destination_file)
        python = "python" if os.name == "nt" else "python3"
        try:
            subprocess.run(
                [python, "deobfuscator.py", "-i", self.source_file, "-o", self.destination_file]
            )
            SuccessWindow(" ", "Деобфускация прошла успешно!").exec()
            with open(self.destination_file, "r", encoding="utf-8") as f:
                self.ui.filename_label.setText(f"Текущий файл: {os.path.basename(self.destination_file)}")
                self.ui.textspace_edit.setPlainText("".join(line for line in f.readlines()))
        except Exception as ex:
            CriticalWindow("Ошибка", str(ex)).exec()
