from PyQt5.QtWidgets import *


class FileLoader(QWidget):
    def __init__(self):
        super().__init__()

        self.group_box = QGroupBox("File Loader")
        self.main_layout = QVBoxLayout()
        self.inner_form_layout = QFormLayout()

        self.l_file = QLabel("File:")
        self.l_wavelength_min = QLabel("Min wavelength:")
        self.l_wavelength_max = QLabel("Max wavelength:")
        self.l_intensity_min = QLabel("Min intensity:")
        self.l_intensity_max = QLabel("Max intensity:")

        self.le_file = QLineEdit()
        self.le_wavelength_min = QLineEdit()
        self.le_wavelength_max = QLineEdit()
        self.le_intensity_min = QLineEdit()
        self.le_intensity_max = QLineEdit()

        self.b_plot = QPushButton("Plot")
        self.b_clear = QPushButton("Clear")

        self.inner_form_layout.addRow(self.l_file, self.le_file)
        self.inner_form_layout.addRow(self.l_wavelength_min, self.le_wavelength_min)
        self.inner_form_layout.addRow(self.l_wavelength_max, self.le_wavelength_max)
        self.inner_form_layout.addRow(self.l_intensity_min, self.le_intensity_min)
        self.inner_form_layout.addRow(self.l_intensity_max, self.le_intensity_max)
        self.inner_form_layout.addRow(self.b_clear, self.b_plot)
        self.group_box.setLayout(self.inner_form_layout)

        self.main_layout.addWidget(self.group_box)
        self.setLayout(self.main_layout)

    def clear_form(self):
        self.le_file.clear()
        self.le_intensity_max.clear()
        self.le_intensity_min.clear()
        self.le_wavelength_max.clear()
        self.le_wavelength_min.clear()

