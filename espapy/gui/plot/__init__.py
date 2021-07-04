import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import *
from . import canvas


class Plot(QWidget):
    def __init__(self, x_data=[], y_data=[]):
        super().__init__()
        self.canvas = canvas.MplCanvas(width=5, height=4, dpi=100)
        self.canvas.axes.plot(x_data, y_data)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.canvas)
        self.setLayout(self.main_layout)

    def plot_data(self, data_file, domain, range, title):
        self.clear_plot()
        self._plot_all_spectral_orders(data_file)
        self.canvas.axes.set_xlim(domain.minimum, domain.maximum)
        self.canvas.axes.set_ylim(range.minimum, range.maximum)
        self.canvas.axes.set_xlabel("Wavelength (nm)")
        self.canvas.axes.set_ylabel("Intensity")
        self.canvas.axes.set_title("Spectrum of " + "\'" + title + "\'")
        self.canvas.draw()

    def clear_plot(self):
        self.canvas.axes.cla()
        self.canvas.draw()

    def _plot_all_spectral_orders(self, data_file):
        for order_data in data_file.split_data:
            self.canvas.axes.plot(order_data["wavelength"], order_data["intensity"])
