__brush = lambda self: self.img.draw_random_brush_line()
__pencil = lambda self: self.img.draw_random_pencil_line()
__ellipse = lambda self: self.img.draw_random_ellipse(rotate=False)
__rectangle = lambda self: self.img.draw_random_rectangle(rotate=False)

__modes = {
    0: {0: __brush},
    1: {0: __pencil},
    2: {0: __brush, 1: __pencil},
    3: {0: __ellipse},
    4: {0: __ellipse, 1: __brush},
    5: {0: __ellipse, 1: __pencil},
    6: {0: __ellipse, 1: __pencil, 2: __brush},
    7: {0: __rectangle},
    8: {0: __rectangle, 1: __brush},
    9: {0: __rectangle, 1: __pencil},
    10: {0: __rectangle, 1: __pencil, 2: __brush},
    11: {0: __rectangle, 1: __ellipse},
    12: {0: __rectangle, 1: __ellipse, 2: __brush},
    13: {0: __rectangle, 1: __ellipse, 2: __pencil},
    14: {0: __rectangle, 1: __ellipse, 2: __pencil, 3: __brush}
}


def resolve_mode(mode):
    return len(__modes[mode]), __modes[mode]