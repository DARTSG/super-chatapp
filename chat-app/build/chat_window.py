import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QMessageBox, QDialog, QLabel, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from update_service import check_for_updates
from send_message_service import send_message

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(50)
        layout.addWidget(self.message_input)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.handle_send_message)
        layout.addWidget(send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.check_for_updates()

    def handle_send_message(self):
        message = self.message_input.toPlainText().strip()
        if message:
            send_message(message, self.chat_display)
            self.message_input.clear()

    def check_for_updates(self):
        self.update_dialog = UpdateDialog(self)
        self.update_dialog.show()
        self.update_dialog.center()
        QTimer.singleShot(100, self._check_for_updates)

    def _check_for_updates(self):
        local_file_path = check_for_updates(self.update_dialog.update_status)
        if local_file_path:
            self.execute_update(local_file_path)
        else:
            self.update_dialog.close()

    def execute_update(self, file_path):
        try:
            os.startfile(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Update Error", f"Failed to execute update: {e}")

    def center(self):
        frame_geom = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        frame_geom.moveCenter(center_point)
        self.move(frame_geom.topLeft())

class UpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Checking for Updates")
        self.setGeometry(150, 150, 300, 100)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.layout = QVBoxLayout()

        self.label = QLabel("Checking for updates...")
        self.layout.addWidget(self.label)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        self.layout.addWidget(self.progress)

        self.setLayout(self.layout)
        self.center()

    def update_status(self, message):
        self.label.setText(message)
        if "successfully" in message or "Failed" in message:
            self.progress.setRange(0, 1)
            QTimer.singleShot(3000, self.close)

    def center(self):
        frame_geom = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        frame_geom.moveCenter(center_point)
        self.move(frame_geom.topLeft())
