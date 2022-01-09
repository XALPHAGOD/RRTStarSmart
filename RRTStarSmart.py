import math
import random
import time
from typing import final
from objects import *
import helper


class Node:
    def __init__(self, point, parent=None, cost=0):
        self.point = point
        self.parent = parent
        self.cost = cost
        self.children = []

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
        iterations=2000,
        epsilon=0.2,
        stepSize=10,
        biasingRadius=40,
        biasingRatio=4,
        gamma=30.0,
    ):
        self.map = map
        self.start = start
        self.end = end
        self.iterations = iterations
        self.epsilon = epsilon
        self.stepSize = stepSize
        self.biasingRadius = biasingRadius
        self.biasingRatio = biasingRatio
        self.gamma = gamma
        self.d = math.log(self.map.length * self.map.height)
        self.nodes = []
        self.lines = []
        self.finalPath = []
        self.beacons = []
        self.n = None
        self.cost = float("inf")
        self.nodes.append(Node(point=self.start))
        self.nodes.append(Node(point=self.end))
        self.reached = False
        self.target = None
        self.strtInt = None
        self.strtIntCnt = 0

    def plan(self):
        if len(self.nodes) >= self.iterations:
            return
        if self.n is not None and (len(self.nodes) - self.n) % self.biasingRatio == 0:
            randPoint = self.intelligentPoint()
        else:
            randPoint = self.randomPoint()
        nearestNode = helper.nearestNode(self.nodes, randPoint, self.end)
        if nearestNode is None:
            return

        theta = math.atan2(
            randPoint.y - nearestNode.point.y, randPoint.x - nearestNode.point.x
        )
        (tempX, tempY) = helper.Polar2Vector(self.stepSize, theta)
        newPoint = Point(pos=(nearestNode.point.x + tempX, nearestNode.point.y + tempY))
        newNode = Node(
            point=newPoint,
            parent=nearestNode,
            cost=nearestNode.cost + newPoint.dist(nearestNode.point),
        )
        if self.map.check_map_bounds(newPoint):
            return
        if helper.checkExistingNode(self.nodes, newPoint):
            return
        if helper.checkObstacles(self.map.obstacles, newPoint):
            return
        if helper.checkLineObsCollision(
            self.map.obstacles, newPoint, nearestNode.point
        ):
            return
        radius = self.gamma * (math.log(len(self.nodes)) / len(self.nodes)) ** (
            1 / self.d
        )

        self.chooseBestParent(newNode, radius)
        self.rewire(newNode, radius)
        self.nodes.append(newNode)

        distFromTarget = newPoint.dist(self.end)
        if distFromTarget <= self.stepSize:
            if self.reached and newNode.cost + distFromTarget < self.target.cost:
                self.target = Node(
                    point=self.end, parent=newNode, cost=newNode.cost + distFromTarget
                )
            elif self.reached:
                pass
            else:
                self.reached = True
                self.n = len(self.nodes)
                print("Found:", self.n, "nodes")
                self.target = Node(
                    point=self.end, parent=newNode, cost=newNode.cost + distFromTarget
                )

        if self.reached:
            tempNode = self.target
            tempFinalPath = []
            while tempNode.parent is not None:
                tempFinalPath.append(tempNode.point.pos)
                tempNode = tempNode.parent
            tempFinalPath.append(tempNode.point.pos)
            tempFinalPath.reverse()

            optimizedPath, cost = self.pathOptimization(tempFinalPath)
            if cost < self.cost:
                self.cost = cost
                self.finalPath = optimizedPath
                self.beacons = tempFinalPath
                print("Updated:", self.cost)

        if len(self.nodes) % 1000 == 0:
            print(len(self.nodes), "iters")

        # time.sleep(0.05)

    def intelligentPoint(self):
        samples = random.sample(self.beacons[:-1], 1)
        beacon = samples[0]
        tempX, tempY = helper.Polar2Vector(
            self.biasingRadius * random.random(), random.uniform(0, 2 * math.pi)
        )
        return Point(pos=(beacon[0] + tempX, beacon[1], tempY))

    def randomPoint(self):
        if random.random() > self.epsilon or self.reached:
            return Point(
                pos=(
                    self.map.left + self.map.length * random.random(),
                    self.map.bottom + self.map.height * random.random(),
                )
            )
        return self.end

    def chooseBestParent(self, newNode, radius):
        nearNodes = [
            nearNode
            for nearNode in self.nodes
            if newNode.point.dist(nearNode.point) < radius
            and nearNode.point.pos != self.end.pos
        ]

        for nearNode in nearNodes:
            newCost = nearNode.cost + newNode.point.dist(nearNode.point)
            if helper.checkLineObsCollision(
                self.map.obstacles, newNode.point, nearNode.point
            ):
                continue
            if newCost < newNode.cost:
                newNode.cost = newCost
                newNode.parent = nearNode

        newNode.parent.children.append(newNode)

    def rewire(self, newNode, radius):
        nearNodes = [
            nearNode
            for nearNode in self.nodes
            if newNode.point.dist(nearNode.point) < radius
        ]

        for nearNode in nearNodes:
            self.updateParentCost(nearNode, newNode)

    def updateParentCost(self, nodeT, viaT):
        queue = []
        queue.append((nodeT, viaT))
        while len(queue) > 0:
            top = queue[0]
            queue.pop(0)
            node = top[0]
            via = top[1]
            newCost = via.cost + via.point.dist(node.point)
            if newCost < node.cost:
                prevParent = node.parent
                node.cost = newCost
                node.parent = via
                helper.updateChildrenCost(node)
                via.children.append(node)
                if prevParent is not None:
                    prevParent.children = helper.deleteChild(node, prevParent.children)
                    queue.append((prevParent, node))

    def pathOptimization(self, tempFinalPath):
        cost = 0
        optimizedPath = [tempFinalPath[-1]]
        iter = (len(tempFinalPath) - 1) - 1
        while iter >= 0:
            pointA = Point(pos=optimizedPath[-1])
            if iter == 0 or helper.checkLineObsCollision(
                self.map.obstacles, pointA, Point(pos=tempFinalPath[iter - 1])
            ):
                cost = cost + pointA.dist(Point(pos=tempFinalPath[iter]))
                optimizedPath.append(tempFinalPath[iter])
            iter = iter - 1
        optimizedPath.reverse()
        return optimizedPath, cost
