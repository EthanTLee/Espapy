from PyQt5.QtWidgets import *
from espapy import gui
from lib import plot_attributes, data_file


class Espapy:
    def __init__(self):
        self.main_window = gui.MainWindow()

        self.main_window.main_gui.data_file_loader.button_plot.clicked.connect(self.on_button_plot_clicked)
        self.main_window.main_gui.data_file_loader.button_clear.clicked.connect(self.on_button_clear_clicked)
        self.main_window.show()

        self.current_data_file = None

    def on_button_plot_clicked(self):
        plot_range = plot_attributes.Range(
            self.main_window.main_gui.data_file_loader.get_intensity_min(),
            self.main_window.main_gui.data_file_loader.get_intensity_max()
        )

        plot_domain = plot_attributes.Domain(
            self.main_window.main_gui.data_file_loader.get_wavelength_min(),
            self.main_window.main_gui.data_file_loader.get_wavelength_max()
        )

        file_name = self.main_window.main_gui.data_file_loader.get_file_name()

        self.current_data_file = data_file.DataFile(file_name)

        self.main_window.main_gui.data_plot.plot_data(
            data_file=self.current_data_file,
            domain=plot_domain,
            range=plot_range,
            title=self.current_data_file.header_info["title"]
        )

    def on_button_clear_clicked(self):
        self.main_window.main_gui.data_plot.clear_plot()
        self.main_window.main_gui.data_file_loader.clear_form()


def main():
    app = QApplication([])
    espapy = Espapy()
    app.exec_()


if __name__ == '__main__':
    main()
