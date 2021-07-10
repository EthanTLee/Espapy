from lib.data_point import DataPoint


def line_through_points(point1: DataPoint, point2: DataPoint):
    line = Line(
        a=(point1.y - point2.y),
        b=(point2.x - point1.x),
        c=(point1.x * point2.y - point2.x * point1.y)
    )

    return line


class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


if __name__ == '__main__':
    test_point1 = DataPoint(1,2)
    test_point2 = DataPoint(2,3)
    test_line = line_through_points(test_point1, test_point2)
    print("done")