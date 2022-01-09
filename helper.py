import math


def nearestNode(nodes, point, end):
    nearestNode = None
    minCost = float("inf")
    for node in nodes:
        cost = node.point.dist(point)
        if cost < minCost and node.point.pos != end.pos:
            minCost = cost
            nearestNode = node
    return nearestNode


def checkExistingNode(nodes, other):
    for node in nodes:
        if node.point.pos == other.pos:
            return True
    return False


def checkObstacles(obstacles, point):
    for obs in obstacles:
        if obs.check_collision(point):
            return True
    return False


def Polar2Vector(dist, theta):
    return (dist * math.cos(theta), dist * math.sin(theta))


def checkLineObsCollision(obstacles, pointA, pointB):
    for obs in obstacles:
        if obs.type == "circle" and checkCircleCollision(pointA, pointB, obs):
            return True
        elif obs.type == "rectangle" and checkRectangleCollision(pointA, pointB, obs):
            return True
    return False


def checkCircleCollision(pointA, pointB, circleObj, avoidDist=5):
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


def checkRectangleCollision(pointA, pointB, rectObj, avoidDist=5):
    x1 = pointA.x
    y1 = pointA.y
    x2 = pointB.x
    y2 = pointB.y
    sx = rectObj.left - avoidDist
    sy = rectObj.bottom - avoidDist
    sw = rectObj.length + 2 * avoidDist
    sh = rectObj.height + 2 * avoidDist

    if lineRect(x1, y1, x2, y2, sx, sy, sw, sh):
        return True

    return False


def lineRect(x1, y1, x2, y2, rx, ry, rw, rh):

    left = lineLine(x1, y1, x2, y2, rx, ry, rx, ry + rh)
    right = lineLine(x1, y1, x2, y2, rx + rw, ry, rx + rw, ry + rh)
    top = lineLine(x1, y1, x2, y2, rx, ry, rx + rw, ry)
    bottom = lineLine(x1, y1, x2, y2, rx, ry + rh, rx + rw, ry + rh)

    if left or right or top or bottom:
        return True

    return False


def lineLine(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = 2
    uB = 2
    if (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1) != 0:
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (
            (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        )
    if (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1) != 0:
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (
            (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        )

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        return True

    return False


def deleteChild(node, parentChildren):
    return [child for child in parentChildren if child.point.pos != node.point.pos]


def updateChildrenCost(nearNode):
    queue = []
    for child in nearNode.children:
        queue.append(child)
    while len(queue) > 0:
        top = queue[0]
        queue.pop(0)
        if (
            top.parent is not None
            and top.parent.cost + top.parent.point.dist(top.point) < top.cost
        ):
            top.cost = top.parent.cost + top.parent.point.dist(top.point)
            for child in top.children:
                queue.append(child)
