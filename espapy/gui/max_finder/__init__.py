from PyQt5.QtWidgets import *


class MaxFinder(QWidget):
    def __init__(self):
        super().__init__()

        self.group_box = QGroupBox("Max Finder")

        self.find_max_button = QPushButton("Find Max")

        self.inner_layout = QVBoxLayout()
        self.inner_layout.addWidget(self.find_max_button)

        self.group_box.setLayout(self.inner_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.group_box)

        self.setLayout(self.main_layout)


