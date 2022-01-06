from map import Map
from objects import *
from RRTStarSmart import RRTStarSmart


def main():
    map = Map(length=960, height=540, caption="RRT* Smart")
    map.add_obstacle(RectangleObstacle(top=540, bottom=285, left=450, right=510))
    # map.add_obstacle(RectangleObstacle(top=255, bottom=0, left=450, right=510))
    map.add_obstacle(RectangleObstacle(top=405, bottom=135, left=370, right=430))
    map.add_obstacle(RectangleObstacle(top=405, bottom=135, left=530, right=590))
    # map.add_obstacle(CircleObstacle(x=20, y=40, radius=10))
    # map.add_obstacle(CircleObstacle(x=200, y=240, radius=80))
    # map.add_obstacle(CircleObstacle(x=420, y=370, radius=150))
    # map.add_obstacle(CircleObstacle(x=900, y=440, radius=30))

    start = Point(pos=(100, 100), color=(20, 252, 3), pointSize=7)
    end = Point(pos=(860, 440), color=(252, 3, 3), pointSize=7)
    rrtstarsmart = RRTStarSmart(map=map, start=start, end=end)
    while map.window_open:
        rrtstarsmart.plan()
        map.add_geometry(nodes=rrtstarsmart.nodes, lines=rrtstarsmart.lines)
        map.render()


if __name__ == "__main__":
    main()
