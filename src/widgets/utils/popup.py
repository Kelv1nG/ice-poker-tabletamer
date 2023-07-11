from PyQt6.QtWidgets import QMessageBox


class PopupMessage(QMessageBox):
    def __init__(
        self, title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Icon.NoIcon
    ):
        super().__init__()
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(icon)
        self.exec()
