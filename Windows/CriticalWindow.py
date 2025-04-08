from PyQt5.QtWidgets import QApplication, QStyle, QMessageBox


class CriticalWindow(QMessageBox):
    def __init__(self, title, text):
        super(CriticalWindow, self).__init__()
        style = QApplication.style()
        icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        self.setIconPixmap(icon.pixmap(32, 32))
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)