import file_loading


class MetaData:
    def __init__(self, file_path):

        file = file_loading.open_file(file_path)

        self.num_columns = 0
        self.num_data_lines = 0
