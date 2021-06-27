from PyQt5.QtWidgets import *
from . import file_loader
from . import plot


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.data_file_loader = file_loader.FileLoader()
        self.data_plot = plot.Plot()
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.data_plot)
        self.main_layout.addWidget(self.data_file_loader)
        self.setLayout(self.main_layout)
