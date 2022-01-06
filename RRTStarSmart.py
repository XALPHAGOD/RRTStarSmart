import math
import random
import time
from objects import *


class Node:
    def __init__(self, point, parent=None, cost=0):
        self.point = point
        self.parent = parent
        self.cost = cost

    def cost(self, other):
        self.cost = math.sqrt(
            math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2)
        )


class RRTStarSmart:
    def __init__(
        self,
        map,
        start,
        end,
        iterations=1e3,
        epsilon=0.2,
        stepSize=10,
        biasingRadius=10,
        biasingRatio=3,
    ):
        self.map = map
        self.start = start
        self.end = end
        self.iterations = iterations
        self.epsilon = epsilon
        self.stepSize = stepSize
        self.biasingRadius = biasingRadius
        self.biasingRatio = biasingRatio
        self.nodes = []
        self.lines = []
        self.finalPath = []
        self.cost = "inf"
        self.nodes.append(Node(point=self.start))
        # self.nodes.append(Node(point=self.end))

    def plan(self):
        # time.sleep(0.5)
        newPoint = self.randomPoint()
        if self.checkExistingNode(newPoint):
            return
        if self.checkObstacles(newPoint):
            return

        nearestNode, minCost = self.nearestNode(newPoint)
        if nearestNode is None:
            return

        self.nodes.append(Node(point=newPoint, parent=nearestNode, cost=minCost))
        self.lines.append(Line(start=nearestNode.point.pos, end=newPoint.pos))

        if len(self.nodes) % 1000 == 0:
            print(len(self.nodes))

    def randomPoint(self):
        return Point(
            pos=(
                self.map.left + self.map.length * random.random(),
                self.map.bottom + self.map.height * random.random(),
            )
        )

    def checkExistingNode(self, other):
        for node in self.nodes:
            if node.point.pos == other.pos:
                return True
        return False

    def checkObstacles(self, point):
        for obs in self.map.obstacles:
            if obs.check_collision(point):
                return True
        return False

    def nearestNode(self, point):
        nearestNode = None
        minCost = float("inf")
        for node in self.nodes:
            cost = node.point.dist(point)
            if (cost + node.cost) < minCost and self.checkLineCollision(
                node.point, point
            ) == False:
                minCost = cost + node.cost
                nearestNode = node
        return nearestNode, minCost

    def checkLineCollision(self, pointA, pointB):
        for obs in self.map.obstacles:
            if obs.type == "circle" and self.checkCircleCollision(pointA, pointB, obs):
                return True
            elif obs.type == "rectangle" and self.checkRectangleCollision(
                pointA, pointB, obs
            ):
                return True
        return False

    def checkCircleCollision(self, pointA, pointB, circleObj, avoidDist=5):
        lineLength = pointA.dist(pointB)
        perpDist = (
            abs(
                pointA.x * (pointB.y - circleObj.y)
                + pointB.x * (circleObj.y - pointA.y)
                + circleObj.x * (pointA.y - pointB.y)
            )
            / lineLength
        )
        if perpDist < circleObj.radius + avoidDist:
            return True
        return False

    def checkRectangleCollision(self, pointA, pointB, rectObj, avoidDist=5):
        x1 = pointA.x
        y1 = pointA.y
        x2 = pointB.x
        y2 = pointB.y
        sx = rectObj.left - avoidDist
        sy = rectObj.bottom - avoidDist
        sw = rectObj.length + 2 * avoidDist
        sh = rectObj.height + 2 * avoidDist

        if self.lineRect(x1, y1, x2, y2, sx, sy, sw, sh):
            return True

        return False

    def lineRect(self, x1, y1, x2, y2, rx, ry, rw, rh):

        left = self.lineLine(x1, y1, x2, y2, rx, ry, rx, ry + rh)
        right = self.lineLine(x1, y1, x2, y2, rx + rw, ry, rx + rw, ry + rh)
        top = self.lineLine(x1, y1, x2, y2, rx, ry, rx + rw, ry)
        bottom = self.lineLine(x1, y1, x2, y2, rx, ry + rh, rx + rw, ry + rh)

        if left or right or top or bottom:
            return True

        return False

    def lineLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (
            (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        )
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (
            (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        )

        if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
            return True

        return False
