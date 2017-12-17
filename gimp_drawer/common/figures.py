class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Line(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_center(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

    def scale(self, scale):
        center = self.get_center()
        return Line(scale * (self.start - center) + center, scale * (self.end - center) + center)


class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_center(self):
        return Point((self.a.x + self.b.x + self.c.x) / 3, (self.a.y + self.b.y + self.c.y) / 3)

    def scale(self, scale):
        def transform(x):
            return scale * (x - center) + center

        center = self.get_center()
        return Triangle(transform(self.a), transform(self.b), transform(self.c))
