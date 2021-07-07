import numpy as np


class DataPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_point_with_greatest_y_value(list_of_data_points):
    list_y_values = []
    for point in list_of_data_points:
        list_y_values.append(point.y)
    arr_y_values = np.array(list_y_values)
    index_of_max = np.argmax(arr_y_values)
    point_with_greatest_y_value = list_of_data_points[index_of_max]

    return point_with_greatest_y_value


def get_point_with_smallest_y_value(list_of_data_points):
    list_y_values = []
    for point in list_of_data_points:
        list_y_values.append(point.y)
    arr_y_values = np.array(list_y_values)
    index_of_min = np.argmin(arr_y_values)
    point_with_smallest_y_value = list_of_data_points[index_of_min]

    return point_with_smallest_y_value
