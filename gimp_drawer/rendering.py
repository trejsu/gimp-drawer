import pyglet

from gimp_drawer.decorators.timed import timed


class SimpleImageViewer(object):
    def __init__(self, display=None):
        self.window = None
        self.is_open = False
        self.display = display
        self.width = None
        self.height = None

    @timed
    def img_show(self, arr):
        if self.window is None:
            height, width, channels = arr.shape
            self.window = pyglet.window.Window(
                width=width,
                height=height,
                display=self.display
            )
            self.width = width
            self.height = height
            self.is_open = True
        assert arr.shape == (self.height, self.width, 3), \
            "You passed in an image with the wrong number shape"
        image = pyglet.image.ImageData(self.width, self.height, 'RGB',
                                       arr.tobytes(), pitch=self.width * -3)
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        image.blit(0, 0)
        self.window.flip()

    @timed
    def close(self):
        if self.is_open:
            self.window.close()
            self.is_open = False

    @timed
    def __del__(self):
        self.close()
