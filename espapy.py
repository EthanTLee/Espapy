from real_thing.espapy.espapy.utils import plot_attributes, data_file
import matplotlib.pyplot as plt

my_data = data_file.DataFile(
    file_path="/initial_testing/from_nadine_Jun23/1834099in.s",
    file_line_num_of_first_data=3
)

my_plot_range = plot_attributes.Range(0, 2)
my_plot_domain = plot_attributes.Domain(500, 600)

plt.plot(my_data.data["Wavelength"], my_data.data["Intensity"])
plt.xlim(my_plot_domain.minimum, my_plot_domain.maximum)
plt.ylim(my_plot_range.minimum, my_plot_range.maximum)

plt.show()


