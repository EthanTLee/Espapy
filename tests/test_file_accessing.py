import unittest
from lib.data_file import header_access


class TestFileLoading(unittest.TestCase):
    def test_open_file(self):
        test_file_path = "/real_thing/espapy/1834099in.s"
        line2 = header_access.get_line(test_file_path, 2)
        self.assertEqual(line2, ' 213722 2\n')


if __name__ == '__main__':
    unittest.main()






