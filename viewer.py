from objects import *

try:
    import pyglet
except ImportError as err:
    raise ImportError(
        """
    Unable to import pyglet.
    Please install pyglet via 'pip install pyglet'
    """
    )

try:
    from pyglet.gl import *
except ImportError as err:
    raise ImportError(
        """
    Unable to import gl from pyglet.
    Please install OpenGL.
    """
    )


class Viewer:
    def __init__(self, length=1280, height=720, caption="XYZ"):
        self.length = length
        self.height = height
        self.caption = caption
        self.window = pyglet.window.Window(
            width=int(self.length),
            height=int(self.height),
            caption=self.caption,
        )
        self.window_open = True
        self.window.on_close = self.close_viewer
        self.window.on_draw = self.draw

    def close_viewer(self):
        self.window_open = False

    def render(self):
        glClearColor(1, 1, 1, 1)
        self.window.clear()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.window.flip()

    def draw(self):
        print("Override in Map class")
        # Testing
        # self.draw_point(Point(pos=(400, 300), color=(100, 0, 0), pointSize=3))
        # self.draw_line(Line(start=(150, 250), end=(350, 450), color=(0, 0, 100)))
        # self.draw_circle(Circle(pos=(300, 300), radius=20, filled=False))
        # self.draw_polygon(
        #     Polygon(
        #         points=((200, 50), (200, 250), (300, 400), (400, 250), (400, 50)),
        #         filled=False,
        #         lineWidth=3,
        #         color=(0, 0, 100),
        #     )
        # )

    def draw_point(self, pointObj):
        pointObj.render()

    def draw_line(self, lineObj):
        lineObj.render()

    def draw_circle(self, circleObj):
        circleObj.render()

    def draw_polygon(self, polygonObj):
        polygonObj.render()
