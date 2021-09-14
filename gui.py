from PyQt5.QtWidgets import *
import lib
import colorsys
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Gui(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Espapy")

        self.setCentralWidget(QWidget())

        self.plot = self.Plot()
        self.file_loader = self.FileLoader()
        self.text_display = self.TextDisplay()
        self.analysis_tools = self.AnalysisTools()

        self.central_widget_layout = QGridLayout()

        self.central_widget_layout.addWidget(self.plot, 0, 0)
        self.central_widget_layout.addWidget(self.file_loader, 0, 1)
        self.central_widget_layout.addWidget(self.text_display, 1, 0)
        self.central_widget_layout.addWidget(self.analysis_tools, 1, 1)

        self.centralWidget().setLayout(self.central_widget_layout)

        self.file_loader.button_plot.clicked.connect(self.on_plot_button_clicked)
        self.file_loader.button_clear.clicked.connect(self.on_clear_button_clicked)
        self.analysis_tools.find_max_button.clicked.connect(self.on_find_local_max_button_clicked)
        self.analysis_tools.find_min_button.clicked.connect(self.on_find_local_min_button_clicked)
        self.analysis_tools.find_width_at_half_max_button.clicked.connect(
            self.on_find_full_width_half_max_button_clicked)
        self.analysis_tools.find_width_at_half_min_button.clicked.connect(
            self.on_find_full_width_half_min_button_clicked)
        self.analysis_tools.lines_halpha.clicked.connect(self.on_lines_halpha_button_clicked)
        self.analysis_tools.lines_hbeta.clicked.connect(self.on_lines_hbeta_button_clicked)
        self.analysis_tools.lines_hgamma.clicked.connect(self.on_lines_hgamma_button_clicked)
        self.analysis_tools.lines_hdelta.clicked.connect(self.on_lines_hdelta_button_clicked)
        self.current_orders_data = []

        self.text_display.add_text_line("    -- Welcome to Espapy --")

    def on_plot_button_clicked(self):
        def set_axis_labels():
            self.plot.set_ylabel("Intensity")
            self.plot.set_xlabel("Wavelength")

        def set_axis_limits(x_lim, y_lim):
            self.plot.set_xlim(x_lim)
            self.plot.set_ylim(y_lim)

        def check_axis_limit_inputs(x_lim, y_lim):
            assert x_lim[0] < x_lim[1]
            assert y_lim[0] < y_lim[1]
            assert 300 <= x_lim[0] <= 1100
            assert 300 <= x_lim[1] <= 1100
            assert 0 <= y_lim[0] <= 10
            assert 0 <= y_lim[1] <= 10

        self.plot.clear_all()
        x_lim = (float(self.file_loader.le_wavelength_min.text()), float(self.file_loader.le_wavelength_max.text()))
        y_lim = (float(self.file_loader.le_intensity_min.text()), float(self.file_loader.le_intensity_max.text()))
        try:
            check_axis_limit_inputs(x_lim, y_lim)
        except:
            self.text_display.add_text_line(
                "Unable to plot: Wavelength must be between 300 nm and 1100 nm, and intensity must be between 0 and 10" + "\n")
            return
        file_path = self.file_loader.le_file.text()
        file_header_info = lib.extract_header_info(file_path)
        orders = lib.extract_renamed_orders(file_path)
        self.current_orders_data = orders
        self.plot.plot_orders_colorized(orders)
        self.plot.set_title(file_header_info.title)
        set_axis_labels()
        set_axis_limits(x_lim, y_lim)

    def on_clear_button_clicked(self):
        self.plot.clear_all()

    def on_find_local_max_button_clicked(self):
        order_datas = self.current_orders_data
        view_domain = self.plot.get_xlim()
        max_point = lib.find_max_in_view_domain(order_datas, view_domain)
        self.plot.plot_point(max_point, color='red')
        self.text_display.add_text_line(
            "Maximum intensity of " +
            str(max_point[1]) + " " +
            "found at " +
            str(max_point[0]) + " " +
            "nm" + "\n"
        )
    def on_lines_halpha_button_clicked(self):
        self.plot.plot_vline(656.3, color='grey')

    def on_lines_hbeta_button_clicked(self):
        self.plot.plot_vline(486.1, color='grey')

    def on_lines_hgamma_button_clicked(self):
        self.plot.plot_vline(434.1, color='grey')

    def on_lines_hdelta_button_clicked(self):
        self.plot.plot_vline(410.1, color='grey')
        
        
    def on_find_local_min_button_clicked(self):
        order_datas = self.current_orders_data
        view_domain = self.plot.get_xlim()
        min_point = lib.find_min_in_view_domain(order_datas, view_domain)
        self.plot.plot_point(min_point, color='blue')
        self.text_display.add_text_line(
            "Minimum intensity of " +
            str(min_point[1]) + " " +
            "found at " +
            str(min_point[0]) + " " +
            "nm" + "\n"
        )

    def on_find_full_width_half_max_button_clicked(self):
        order_datas = self.current_orders_data
        view_domain = self.plot.get_xlim()
        left_intersection, right_intersection = lib.find_intersections_with_half_max_of_local_max(order_datas,
                                                                                                  view_domain, float(
                self.analysis_tools.baseline_input.text()))
        self.plot.plot([left_intersection[0], right_intersection[0]], [left_intersection[1], right_intersection[1]],
                       color='purple')
        self.text_display.add_text_line(
            "Width of " +
            str(right_intersection[0] - left_intersection[0]) +
            " nm" +
            " found at an intensity of " +
            str(left_intersection[1]) + "\n"
        )

    def on_find_full_width_half_min_button_clicked(self):
        order_datas = self.current_orders_data
        view_domain = self.plot.get_xlim()
        left_intersection, right_intersection = lib.find_intersections_with_half_min_of_local_min(order_datas,
                                                                                                  view_domain, float(
                self.analysis_tools.baseline_input.text()))
        self.plot.plot([left_intersection[0], right_intersection[0]], [left_intersection[1], right_intersection[1]],
                       color='purple')
        self.text_display.add_text_line(
            "Width of " +
            str(right_intersection[0] - left_intersection[0]) +
            " nm" +
            " found at an intensity of " +
            str(left_intersection[1]) + "\n"
        )

    class Plot(QWidget):
        def __init__(self, x_data=[], y_data=[]):
            super().__init__()
            self.canvas = self.MplCanvas(width=5, height=4, dpi=100)
            self.canvas.axes.plot(x_data, y_data)
            self.toolbar = NavigationToolbar(self.canvas, self)

            self.main_layout = QVBoxLayout()
            self.main_layout.addWidget(self.toolbar)
            self.main_layout.addWidget(self.canvas)
            self.setLayout(self.main_layout)

        def plot_orders_colorized(self, order_datas):
            def generate_color_list(number_of_orders):
                color_list = []
                for i in range(number_of_orders):
                    violet_hue = 0.75
                    hue = violet_hue - i * (violet_hue / number_of_orders)
                    lightness = 0.4
                    saturation = 0.8
                    color = colorsys.hls_to_rgb(hue, lightness, saturation)
                    color_list.append(color)
                return color_list

            def draw_orders(order_datas, color_list):
                for i in range(len(order_datas)):
                    self.canvas.axes.plot(order_datas[i]['wavelength'], order_datas[i]['intensity'],
                                          color=color_list[i], alpha=0.8)
                self.canvas.draw()

            color_list = generate_color_list(len(order_datas))
            draw_orders(order_datas, color_list)

        def plot(self, x_data, y_data, color):
            self.canvas.axes.plot(x_data, y_data, color)
            self.canvas.draw()

        def plot_point(self, point, color):
            self.canvas.axes.scatter(point[0], point[1], color=color)
            self.canvas.draw()

        def plot_vline(self, point, color):
            self.canvas.axes.plot([point,point],self.canvas.axes.get_ylim(), linestyle='dashed', color=color)
            self.canvas.draw()

        def multi_plot(self, line_collection):
            self.canvas.axes.add_collection(line_collection)

        def set_ylim(self, ylim: tuple):
            self.canvas.axes.set_ylim(ylim)
            self.canvas.draw()

        def set_xlim(self, xlim: tuple):
            self.canvas.axes.set_xlim(xlim)
            self.canvas.draw()

        def get_ylim(self):
            return self.canvas.axes.get_ylim()

        def get_xlim(self):
            return self.canvas.axes.get_xlim()

        def clear_all(self):
            self.canvas.axes.cla()
            self.canvas.draw()

        def set_title(self, title):
            self.canvas.axes.set_title(title)
            self.canvas.draw()

        def set_ylabel(self, ylabel):
            self.canvas.axes.set_ylabel(ylabel)
            self.canvas.draw()

        def set_xlabel(self, xlabel):
            self.canvas.axes.set_xlabel(xlabel)
            self.canvas.draw()

        def draw(self):
            self.canvas.draw()

        class MplCanvas(FigureCanvasQTAgg):
            def __init__(self, width=5, height=4, dpi=100):
                fig = Figure(figsize=(width, height), dpi=dpi)
                self.axes = fig.add_subplot(111)
                super().__init__(fig)

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

    class FileLoader(QWidget):
        def __init__(self):
            super().__init__()

            self.group_box = QGroupBox("File Loader")
            self.main_layout = QVBoxLayout()
            self.inner_layout = QGridLayout()

            self.l_file = QLabel("File:")
            self.l_wavelength_min = QLabel("Min wavelength (nm):")
            self.l_wavelength_max = QLabel("Max wavelength (nm):")
            self.l_intensity_min = QLabel("Min intensity:")
            self.l_intensity_max = QLabel("Max intensity:")

            self.le_file = QLineEdit()
            self.le_file.setPlaceholderText("e.g. data_file.s")
            self.le_wavelength_min = QLineEdit()
            self.le_wavelength_min.setPlaceholderText("e.g. 450")
            self.le_wavelength_max = QLineEdit()
            self.le_wavelength_max.setPlaceholderText("e.g. 1000")
            self.le_intensity_min = QLineEdit()
            self.le_intensity_min.setPlaceholderText("e.g. 0")
            self.le_intensity_max = QLineEdit()
            self.le_intensity_max.setPlaceholderText("e.g. 2")

            self.button_browse = QPushButton("Browse")
            self.button_plot = QPushButton("Plot")
            self.button_clear = QPushButton("Clear")

            self.inner_layout.addWidget(self.l_file, 0, 0)
            self.inner_layout.addWidget(self.le_file, 0, 1)
            self.inner_layout.addWidget(self.button_browse, 0, 2)
            self.inner_layout.addWidget(self.l_wavelength_min, 1, 0)
            self.inner_layout.addWidget(self.le_wavelength_min, 1, 1)
            self.inner_layout.addWidget(self.l_wavelength_max, 2, 0)
            self.inner_layout.addWidget(self.le_wavelength_max, 2, 1)
            self.inner_layout.addWidget(self.l_intensity_min, 3, 0)
            self.inner_layout.addWidget(self.le_intensity_min, 3, 1)
            self.inner_layout.addWidget(self.l_intensity_max, 4, 0)
            self.inner_layout.addWidget(self.le_intensity_max, 4, 1)
            self.inner_layout.addWidget(self.button_clear, 5, 0)
            self.inner_layout.addWidget(self.button_plot, 5, 1)

            self.group_box.setLayout(self.inner_layout)

            self.main_layout.addWidget(self.group_box)
            self.setLayout(self.main_layout)

            self.button_browse.clicked.connect(self.on_browse_button_clicked)

        def on_browse_button_clicked(self):
            file_path = QFileDialog.getOpenFileName(self, "choose a data file")[0]
            self.le_file.setText(file_path)

        def clear_fields(self):
            self.le_file.clear()
            self.le_intensity_max.clear()
            self.le_intensity_min.clear()
            self.le_wavelength_min.clear()
            self.le_wavelength_max.clear()

    class AnalysisTools(QWidget):
        def __init__(self):
            super().__init__()

            self.group_box = QGroupBox("Analysis Tools")

            self.inner_layout = QVBoxLayout()

            self.find_max_button = QPushButton("Find local max")
            self.find_min_button = QPushButton("Find local min")
            self.width_finder_group_box = QGroupBox("Width Finder")
            self.find_width_at_half_max_button = QPushButton("Full width at half max")
            self.find_width_at_half_min_button = QPushButton("Full width at half min")
            self.lines_halpha= QPushButton("H alpha / 656.3 nm")
            self.lines_hbeta= QPushButton("H beta  / 486.1 nm")
            self.lines_hgamma= QPushButton("H gamma  / 434.1 nm")
            self.lines_hdelta= QPushButton("H delta  / 419.1 nm")
            
            self.baseline_input = self.BaselineInput()
            self.width_finder_group_box_layout = QVBoxLayout()
            self.width_finder_group_box_layout.addWidget(self.find_width_at_half_max_button)
            self.width_finder_group_box_layout.addWidget(self.find_width_at_half_min_button)
            self.width_finder_group_box_layout.addWidget(self.baseline_input)
            self.width_finder_group_box.setLayout(self.width_finder_group_box_layout)

            self.tabs = QTabWidget()
            self.max_min_tab = QWidget()
            self.width_tab = QWidget()
            self.lines_tab= QWidget()

            self.max_min_tab_layout = QVBoxLayout()
            self.max_min_tab_layout.addWidget(self.find_max_button)
            self.max_min_tab_layout.addWidget(self.find_min_button)
            self.max_min_tab.setLayout(self.max_min_tab_layout)

            self.width_tab_layout = QVBoxLayout()
            self.width_tab_layout.addWidget(self.find_width_at_half_max_button)
            self.width_tab_layout.addWidget(self.find_width_at_half_min_button)
            self.width_tab_layout.addWidget(self.baseline_input)
            self.width_tab.setLayout(self.width_tab_layout)

            self.lines_tab_layout = QVBoxLayout()
            self.lines_tab_layout.addWidget(self.lines_halpha)
            self.lines_tab_layout.addWidget(self.lines_hbeta)
            self.lines_tab_layout.addWidget(self.lines_hgamma)
            self.lines_tab_layout.addWidget(self.lines_hdelta)
            
            self.lines_tab.setLayout(self.lines_tab_layout)
            
            self.tabs.addTab(self.max_min_tab, "Extrema")
            self.tabs.addTab(self.width_tab, "Width")
            self.tabs.addTab(self.lines_tab, "Lines")
            self.inner_layout.addWidget(self.tabs)

            self.group_box.setLayout(self.inner_layout)

            self.main_layout = QVBoxLayout()
            self.main_layout.addWidget(self.group_box)

            self.setLayout(self.main_layout)

        class BaselineInput(QWidget):
            def __init__(self):
                super().__init__()

                self.l_baseline = QLabel("Baseline: ")
                self.le_baseline = QLineEdit("1")
                self.layout = QHBoxLayout()
                self.layout.addWidget(self.l_baseline)
                self.layout.addWidget(self.le_baseline)
                self.setLayout(self.layout)

            def text(self):
                return self.le_baseline.text()
