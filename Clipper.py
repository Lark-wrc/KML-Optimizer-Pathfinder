from GeometricDataStructures.Mercator import MercatorPoint

class Clipper():

    def __init__(self):
        pass

    # def verticalCheck(self, aLine, bLine):
    #     if aLine.start.x == aLine.end.x:
    #         aLine.slope = (aLine.end.y - aLine.start.y) / (aLine.end.x - aLine.start.x)
    #         aLine.cept = aLine.start.y - (aLine.slope * aLine.start.x)
    #         y = (aLine.slope * bLine.start.x) + aLine.cept
    #         return MercatorPoint(bLine.start.x, y)
    #     else: return None

    def getLineIntersection(self, pointA, pointB, pointC, pointD):

        if not if_intersect(pointA, pointB, pointC, pointD): return None

        xdiff = pointA[0] - pointB[0], pointC[0] - pointD[0]
        ydiff = pointA[1] - pointB[1], pointC[1] - pointD[1]

        div = determinent(xdiff, ydiff)
        if(div == 0): raise Exception("No POI")

        d = determinent(pointA, pointB), determinent(pointC, pointD)
        resultx = determinent(d, xdiff) / div
        resulty = determinent(d, ydiff) / div
        return resultx, resulty

    def determinent(self, pointA, pointB):
        return (pointA[0] * pointB[1] - pointA[1] * pointB[0])

    def my_gradient(self, pointA, pointB):
        m = None
        if(pointA[0] != pointB[0]):
            m = (1./(pointA[0] - pointB[0]) * (pointA[1] - pointB[1]))
            return m

    def doLinesIntersect(self, pointA, pointB, pointC, pointD):

        o1 = findOrientation(pointA, pointB, pointC);
        o2 = findOrientation(pointA, pointB, pointD);
        o3 = findOrientation(pointC, pointD, pointA);
        o4 = findOrientation(pointC, pointD, pointB);

        if (o1 != o2 and o3 != o4):
           return True
        return False

    def findOrientation(self, pointA, pointB, pointC):
        val = (pointB[1] - pointA[1]) * (pointC[0] - pointB[0]) - (pointB[0] - pointA[0]) * (pointC[1] - pointB[1]);
        if (val == 0.0): return 0  # Orientation.COLLINEAR
        elif (val > 0): return -1  # Orientation.RIGHT
        else: return 1  # Orientation.LEFT
