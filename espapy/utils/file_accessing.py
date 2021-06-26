
def get_line(file_path, line_number):
    file = open(file_path)
    for line in range(line_number-1):
        next(file)

    target_line = file.readline()
    file.close()
    return target_line
