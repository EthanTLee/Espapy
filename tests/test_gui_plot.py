from PyQt5.QtWidgets import *
from espapy.gui import plot


def test_gui_plot():
    app = QApplication([])
    test_plot = plot.Plot(x_data=[1,2,3,4], y_data=[1,6,2,-1])
    test_plot.show()
    test_plot.plot_data([20, 21, 22, 23], [1, 2, 3, 10])
    app.exec_()


if __name__ == '__main__':
    test_gui_plot()
