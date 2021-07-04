
def generate_column_names(total_num_of_columns):

    def generate_generic_names():
        for column_number in range(total_num_of_columns):
            column_names.append('Col ' + str(column_number))

    def rename_first_two_names_to_wavelength_and_intensity():
        column_names[0] = 'wavelength'
        column_names[1] = 'intensity'

    column_names = []
    generate_generic_names()
    rename_first_two_names_to_wavelength_and_intensity()

    return column_names


