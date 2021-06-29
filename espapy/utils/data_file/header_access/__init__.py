
def get_header_info(file_path):
    file = open(file_path)
    line_title = file.readline()
    line_num_col_row = file.readline()
    file.close()
    header_info = {
        "title": get_segment_of_string(
            string=line_title,
            separator_symbol="\'",
            target_segment_index=1
        ),
        "num_data_rows": get_segment_of_string_as_int(
            string=line_num_col_row,
            separator_symbol=" ",
            target_segment_index=1
        ),
        "num_additional_columns": get_segment_of_string_as_int(
            string=line_num_col_row,
            separator_symbol=" ",
            target_segment_index=2
        ),
    }
    return header_info


def get_segment_of_string(string, separator_symbol, target_segment_index):
    target_segment = string.split(separator_symbol)[target_segment_index]
    return target_segment


def get_segment_of_string_as_int(string, separator_symbol, target_segment_index):
    target_segment = get_segment_of_string(string, separator_symbol, target_segment_index)
    return int(target_segment)

