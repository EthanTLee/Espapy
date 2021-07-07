from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from espapy import gui
from espapy import utils
from lib import set_attributes, data_file


class Espapy:
    def __init__(self):
        self.main_window = gui.MainWindow()

        self.main_window.main_gui.data_file_loader.button_plot.clicked.connect(self.on_button_plot_clicked)
        self.main_window.main_gui.data_file_loader.button_clear.clicked.connect(self.on_button_clear_clicked)
        self.main_window.main_gui.analysis_tools.find_max_button.clicked.connect(self.on_button_find_max_clicked)
        self.main_window.main_gui.analysis_tools.find_min_button.clicked.connect(self.on_button_find_min_clicked)

        self.main_window.show()

        self.main_window.main_gui.text_display.add_text_line("--- Welcome to Espapy ---")

        self.current_data_file = None

    def on_button_plot_clicked(self):
        plot_range = set_attributes.Range(
            self.main_window.main_gui.data_file_loader.get_intensity_min(),
            self.main_window.main_gui.data_file_loader.get_intensity_max()
        )

        plot_domain = set_attributes.Domain(
            self.main_window.main_gui.data_file_loader.get_wavelength_min(),
            self.main_window.main_gui.data_file_loader.get_wavelength_max()
        )

        file_path = self.main_window.main_gui.data_file_loader.get_file_name()

        self.current_data_file = data_file.DataFile(file_path)

        self.main_window.main_gui.data_plot.plot_data(
            data_file=self.current_data_file,
            domain=plot_domain,
            range=plot_range,
            title=self.current_data_file.header_info["title"]
        )

    def on_button_clear_clicked(self):
        self.main_window.main_gui.data_plot.clear_plot()
        self.main_window.main_gui.data_file_loader.clear_form()

    def on_button_find_max_clicked(self):
        current_domain = self.main_window.main_gui.data_plot.get_current_domain()
        max_intensity_point_in_domain = utils.get_max_intensity_point_in_domain(self.current_data_file, current_domain)
        self.main_window.main_gui.data_plot.plot_point(max_intensity_point_in_domain, color='red')
        self.main_window.main_gui.text_display.add_text_line(
            "Maximum intensity of " +
            str(max_intensity_point_in_domain.y) + " " +
            "found at " +
            str(max_intensity_point_in_domain.x) + " " +
            "nm"
        )

    def on_button_find_min_clicked(self):
        current_domain = self.main_window.main_gui.data_plot.get_current_domain()
        min_intensity_point_in_domain = utils.get_min_intensity_point_in_domain(self.current_data_file, current_domain)
        self.main_window.main_gui.data_plot.plot_point(min_intensity_point_in_domain, color='blue')
        self.main_window.main_gui.text_display.add_text_line(
            "Minimum intensity of " +
            str(min_intensity_point_in_domain.y) + " " +
            "found at " +
            str(min_intensity_point_in_domain.x) + " " +
            "nm"
        )


def main():
    app = QApplication([])


    icon = QIcon('./icon/espadon2.png')
    app.setWindowIcon(icon)

    espapy = Espapy()
    app.exec_()


if __name__ == '__main__':
    main()
