from PyQt5.QtWidgets import QApplication, QStyle, QMessageBox


class SuccessWindow(QMessageBox):
    def __init__(self, title, text):
        super(SuccessWindow, self).__init__()
        style = QApplication.style()
        icon = style.standardIcon(QStyle.SP_DialogApplyButton)
        self.setIconPixmap(icon.pixmap(32, 32))
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)