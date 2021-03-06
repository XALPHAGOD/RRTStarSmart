from map import Map
from objects import *
from RRTStarSmart import RRTStarSmart


def main():
    map = Map(length=960, height=540, caption="RRT* Smart")
    # Course 1
    # map.add_obstacle(RectangleObstacle(top=540, bottom=290, left=450, right=510))
    # map.add_obstacle(RectangleObstacle(top=250, bottom=0, left=450, right=510))
    # map.add_obstacle(RectangleObstacle(top=405, bottom=135, left=350, right=410))
    # map.add_obstacle(RectangleObstacle(top=405, bottom=135, left=550, right=610))
    # start = Point(pos=(100, 100), color=(20, 252, 3), pointSize=7)
    # end = Point(pos=(860, 440), color=(252, 3, 3), pointSize=7)
    # map.add_obstacle(CircleObstacle(x=20, y=40, radius=20))
    # Course 2
    map.add_obstacle(RectangleObstacle(top=500, bottom=100, left=600, right=700))
    map.add_obstacle(RectangleObstacle(top=350, bottom=300, left=350, right=600))
    map.add_obstacle(RectangleObstacle(top=240, bottom=200, left=700, right=800))
    start = Point(pos=(380, 270), color=(20, 252, 3), pointSize=7)
    end = Point(pos=(720, 460), color=(252, 3, 3), pointSize=7)
    # Course 3
    # map.add_obstacle(RectangleObstacle(top=500, bottom=430, left=465, right=800))
    # map.add_obstacle(RectangleObstacle(top=380, bottom=310, left=160, right=495))
    # map.add_obstacle(RectangleObstacle(top=260, bottom=190, left=465, right=800))
    # map.add_obstacle(RectangleObstacle(top=140, bottom=70, left=160, right=495))
    # start = Point(pos=(480, 520), color=(20, 252, 3), pointSize=7)
    # end = Point(pos=(480, 50), color=(252, 3, 3), pointSize=7)
    # Course 4
    # map.add_obstacle(RectangleObstacle(top=340, bottom=310, left=410, right=580))
    # map.add_obstacle(RectangleObstacle(top=340, bottom=240, left=550, right=580))
    # map.add_obstacle(RectangleObstacle(top=240, bottom=210, left=360, right=580))
    # map.add_obstacle(RectangleObstacle(top=390, bottom=210, left=330, right=360))
    # map.add_obstacle(RectangleObstacle(top=420, bottom=390, left=330, right=630))
    # map.add_obstacle(RectangleObstacle(top=420, bottom=160, left=630, right=660))
    # map.add_obstacle(RectangleObstacle(top=160, bottom=130, left=280, right=660))
    # map.add_obstacle(RectangleObstacle(top=470, bottom=130, left=250, right=280))
    # map.add_obstacle(RectangleObstacle(top=500, bottom=470, left=250, right=700))
    # start = Point(pos=(480, 270), color=(20, 252, 3), pointSize=7)
    # end = Point(pos=(650, 520), color=(252, 3, 3), pointSize=7)
    # Course 5
    # map.add_obstacle(RectangleObstacle(top=540, bottom=280, left=100, right=860))
    # map.add_obstacle(RectangleObstacle(top=260, bottom=0, left=100, right=860))
    # start = Point(pos=(50, 50), color=(20, 252, 3), pointSize=7)
    # end = Point(pos=(910, 490), color=(252, 3, 3), pointSize=7)
    # Course 6
    # map.add_obstacle(RectangleObstacle(top=290, bottom=0, left=100, right=150))
    # map.add_obstacle(RectangleObstacle(top=540, bottom=250, left=200, right=250))
    # map.add_obstacle(RectangleObstacle(top=290, bottom=0, left=300, right=350))
    # map.add_obstacle(RectangleObstacle(top=540, bottom=250, left=400, right=450))
    # map.add_obstacle(RectangleObstacle(top=290, bottom=0, left=500, right=550))
    # map.add_obstacle(RectangleObstacle(top=540, bottom=250, left=600, right=650))
    # map.add_obstacle(RectangleObstacle(top=290, bottom=0, left=700, right=750))
    # map.add_obstacle(RectangleObstacle(top=540, bottom=250, left=800, right=850))
    # start = Point(pos=(50, 50), color=(20, 252, 3), pointSize=7)
    # end = Point(pos=(910, 490), color=(252, 3, 3), pointSize=7)

    rrtstarsmart = RRTStarSmart(map=map, start=start, end=end, iterations=1e4)
    while map.window_open:
        rrtstarsmart.plan()
        finalPath = rrtstarsmart.finalPath
        final = []
        for i in range(len(finalPath) - 1):
            final.append(
                Line(
                    start=finalPath[i],
                    end=finalPath[i + 1],
                    color=(0, 220, 0),
                    lineWidth=3,
                )
            )
        lines = []
        for node in rrtstarsmart.nodes:
            if node.parent is not None:
                lines.append(Line(start=node.parent.point.pos, end=node.point.pos))
        map.add_geometry(
            nodes=rrtstarsmart.nodes,
            lines=lines,
            final=final,
        )
        map.render()


if __name__ == "__main__":
    main()
