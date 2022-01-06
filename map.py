from objects import *
from viewer import Viewer


class Map(Viewer):
    def __init__(self, length=1280, height=720, caption="ABC"):
        self.top = height
        self.bottom = 0
        self.left = 0
        self.right = length
        self.length = length
        self.height = height
        self.caption = caption
        Viewer.__init__(
            self, length=self.length, height=self.height, caption=self.caption
        )
        self.obstacles = []
        self.start = None
        self.end = None
        self.nodes = []
        self.lines = []

    def add_geometry(self, nodes=[], lines=[]):
        self.nodes = nodes
        self.lines = lines

    def add_obstacle(self, obs):
        self.obstacles.append(obs)

    def draw(self):
        for obs in self.obstacles:
            if obs.type == "circle":
                self.draw_circle(
                    Circle(pos=(obs.x, obs.y), radius=obs.radius, color=obs.color)
                )
            elif obs.type == "rectangle":
                self.draw_polygon(
                    Polygon(
                        points=(
                            (obs.left, obs.top),
                            (obs.right, obs.top),
                            (obs.right, obs.bottom),
                            (obs.left, obs.bottom),
                        ),
                        color=obs.color,
                        filled=True,
                    )
                )

        for line in self.lines:
            line.render()

        for node in self.nodes:
            node.point.render()

    def check_map_bounds(self, pos):
        return (
            pos.x < self.left
            or pos.x > self.right
            or pos.y < self.bottom
            or pos.y > self.top
        )
