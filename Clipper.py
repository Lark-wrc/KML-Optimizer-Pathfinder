from GeometricDataStructures.Mercator import MercatorPoint
import math

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
         """
        `Author`: Bob Seedorf

        Returns the point, as a tuple, at which the line segments composed composed of points A, B and poinst C, D intersect
        If the lines do not intersect, return None.

        'pointA': start point of first line
        'pointB': end point of first line
        'pointC': start point of second line
        'pointD': end point of second line
        """

        if not doLinesIntersect(pointA, pointB, pointC, pointD): return None

        xdiff = pointA[0] - pointB[0], pointC[0] - pointD[0]
        ydiff = pointA[1] - pointB[1], pointC[1] - pointD[1]

        div = determinent(xdiff, ydiff)
        if(div == 0): raise Exception("No POI")

        d = determinent(pointA, pointB), determinent(pointC, pointD)
        resultx = determinent(d, xdiff) / div
        resulty = determinent(d, ydiff) / div
        return resultx, resulty

    def determinent(self, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the algebraic determinent of the parameterized points using linear combinations of thier coordinate pairs.

        'pointA': start point of line
        'pointB': end point of line
        """
        return (pointA[0] * pointB[1] - pointA[1] * pointB[0])

    def gradient(self, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the 'slope' of the line composed of the two points

        'pointA': start point of line
        'pointB': end point of line
        """
        m = None
        if(pointA[0] != pointB[0]):
            m = (1./(pointA[0] - pointB[0]) * (pointA[1] - pointB[1]))
            return m

    def doLinesIntersect(self, pointA, pointB, pointC, pointD):
        """
        `Author`: Bob Seedorf

        Returns True if the line segments composed of points A, B and points C, D have an intersection point

        'pointA': start point of first line
        'pointB': end point of first line
        'pointC': start point of second line
        'pointD': end point of second line
        """

        o1 = findOrientation(pointA, pointB, pointC);
        o2 = findOrientation(pointA, pointB, pointD);
        o3 = findOrientation(pointC, pointD, pointA);
        o4 = findOrientation(pointC, pointD, pointB);

        if (o1 != o2 and o3 != o4):
           return True
        return False

    def findOrientation(self, pointA, pointB, pointC):
        """
        `Author`: Bob Seedorf

        Returns orientation of three given points in coordinate space

        'pointA': first point being passed
        'pointB': second point being passed
        'pointC': third point being passed
        """
        val = (pointB[1] - pointA[1]) * (pointC[0] - pointB[0]) - (pointB[0] - pointA[0]) * (pointC[1] - pointB[1]);
        if (val == 0.0): return 0   # Orientation.COLLINEAR
        elif (val > 0): return -1   # Orientation.RIGHT
        else: return 1              # Orientation.LEFT

    def getClosestPoint(slef, target, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the point, of only pointA or pointB, that is dimensionally closest to the point target

        'target': control point form whom the distances of the other two will be checked
        'pointA': first point to be checked, has return precedence over pointB
        'pointB': second point to be checked
        """
        distToA = math.sqrt(((target[0] - pointA[0]) ** 2) + (target[1] - pointA[1]) ** 2)
        distToB = math.sqrt(((target[0] - pointB[0]) ** 2) + (target[1] - pointB[1]) ** 2)
        return pointA if distToA <= distToB else pointB
