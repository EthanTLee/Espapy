from PyQt5.QtWidgets import *


class TextDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self.text_box = QPlainTextEdit(self)
        self.text_box.setReadOnly(True)
        self.text_box.ensureCursorVisible()
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.text_box)
        self.setLayout(self.main_layout)

    def add_text_line(self, text):
        self.text_box.insertPlainText(text + "\n")
        self.text_box.ensureCursorVisible()