from PyQt5.QtWidgets import *
from . import file_loader
from . import plot


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Espapy")
        self._create_menu_bar()
        self.main_gui = Gui()
        self.setCentralWidget(self.main_gui)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        help_menu = menu_bar.addMenu("&Help")

        self.help_action = QAction("Get Help", self)

        help_menu.addAction(self.help_action)

        self.help_action.triggered.connect(self.open_help_window)

    def open_help_window(self):
        print("got help")


class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.data_file_loader = file_loader.FileLoader()
        self.data_plot = plot.Plot()
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.data_plot)
        self.main_layout.addWidget(self.data_file_loader)
        self.setLayout(self.main_layout)
