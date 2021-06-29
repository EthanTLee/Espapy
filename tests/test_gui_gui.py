from PyQt5.QtWidgets import *
from espapy import gui


def test_gui_gui():
    app = QApplication([])
    test_gui = gui.Gui()
    test_gui.show()
    app.exec_()


if __name__ == '__main__':
    test_gui_gui()
