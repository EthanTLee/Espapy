from lib import data_file

if __name__ == '__main__':

    test_data_file = data_file.DataFile(file_path='1834099in.s', file_line_num_of_first_data=3)
    print(test_data_file.whole_data)

