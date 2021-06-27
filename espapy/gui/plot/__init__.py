from PyQt5.QtWidgets import *
from . import canvas


class Plot(QWidget):
    def __init__(self, x_data=[], y_data=[]):
        super().__init__()
        self.canvas = canvas.MplCanvas(width=5, height=4, dpi=100)
        self.canvas.axes.plot(x_data, y_data)
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.canvas)
        self.setLayout(self.main_layout)

    def update_plot(self, x_data, y_data):
        self.clear_plot()
        self.canvas.axes.plot(x_data, y_data)
        self.canvas.draw()

    def clear_plot(self):
        self.canvas.axes.cla()
