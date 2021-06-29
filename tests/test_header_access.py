import unittest
from espapy.utils.data_file import header_access


class MyTestCase(unittest.TestCase):
    def test_something(self):
        header_info = header_access.get_header_info('/Users/peepeepoopoo/Desktop/espapy/tests/1834099in.s')
        self.assertEqual(header_info["title"], 'FS CMa  ')
        self.assertEqual(header_info["num_additional_columns"], 2)
        self.assertEqual(header_info["num_data_rows"], 213722)


if __name__ == '__main__':
    unittest.main()
