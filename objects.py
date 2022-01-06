import math

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


class Point:
    def __init__(self, pos=(100, 100), color=(0, 0, 0), pointSize=3):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.pointSize = pointSize

    def render(self):
        glColor3ub(*self.color)
        glPointSize(self.pointSize)
        glBegin(GL_POINTS)
        glVertex2d(*self.pos)
        glEnd()

    def equal(self, other):
        return self.x == other.x and self.y == other.y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def dist(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))


class Line:
    def __init__(self, start, end, color=(255, 0, 195), lineWidth=1):
        self.start = start
        self.end = end
        self.color = color
        self.lineWidth = lineWidth

    def render(self):
        glColor3ub(*self.color)
        glLineWidth(self.lineWidth)
        glBegin(GL_LINES)
        glVertex2d(*self.start)
        glVertex2d(*self.end)
        glEnd()


class Circle:
    def __init__(
        self,
        pos=(200, 200),
        radius=10,
        res=60,
        color=(0, 0, 0),
        lineWidth=2,
        filled=True,
    ):
        self.pos = pos
        self.radius = radius
        self.res = res
        self.color = color
        self.lineWidth = lineWidth
        self.filled = filled

    def render(self):
        glColor3ub(*self.color)
        glLineWidth(self.lineWidth)
        if self.filled:
            glBegin(GL_POLYGON)
        else:
            glBegin(GL_LINE_LOOP)
        for i in range(self.res):
            angle = 2 * math.pi / self.res * i
            glVertex2d(
                self.pos[0] + self.radius * math.cos(angle),
                self.pos[1] + self.radius * math.sin(angle),
            )
        glEnd()


class Polygon:
    def __init__(self, points, close=True, filled=True, lineWidth=3, color=(0, 0, 0)):
        self.points = points
        self.close = close
        self.filled = filled
        self.lineWidth = lineWidth
        self.color = color

    def render(self):
        glColor3ub(*self.color)
        glLineWidth(self.lineWidth)
        if self.filled:
            if len(self.points) > 4:
                glBegin(GL_POLYGON)
            elif len(self.points) == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_LINE_LOOP if self.close else GL_LINE_STRIP)
        for point in self.points:
            glVertex2d(*point)
        glEnd()


class RectangleObstacle:
    def __init__(self, top, bottom, left, right, color=(92, 56, 43)):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.length = self.right - self.left
        self.height = self.top - self.bottom
        self.color = color
        self.type = "rectangle"

    def dist(self, other):
        if other.x < self.left:
            if other.y > self.top:
                return other.dist(Point(pos=(self.left, self.top)))
            elif other.y < self.bottom:
                return other.dist(Point(pos=(self.left, self.bottom)))
            else:
                return math.fabs(other.x - self.left)
        elif other.x > self.right:
            if other.y > self.top:
                return other.dist(Point(pos=(self.right, self.top)))
            elif other.y < self.bottom:
                return other.dist(Point(pos=(self.right, self.bottom)))
            else:
                return math.fabs(other.x - self.right)
        else:
            if other.y > self.top:
                return math.fabs(other.y - self.top)
            elif other.y < self.bottom:
                return math.fabs(other.y - self.bottom)
            else:
                return 0

    def check_collision(self, other, avoidDist=5):
        return self.dist(other) <= avoidDist


class CircleObstacle:
    def __init__(self, x, y, radius, color=(92, 56, 43)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.type = "circle"

    def dist(self, other):
        return max(other.dist(Point(pos=(self.x, self.y))) - self.radius, 0)

    def check_collision(self, other, avoidDist=5):
        return self.dist(other) <= avoidDist
