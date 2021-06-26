import unittest
from PyQt5.QtWidgets import *
from espapy.gui import file_loader


class MyTestCase(unittest.TestCase):
    def test_gui_file_loader(self):
        app = QApplication([])
        test_file_loader = file_loader.FileLoader()
        test_file_loader.show()
        app.exec_()


if __name__ == '__main__':
    unittest.main()
