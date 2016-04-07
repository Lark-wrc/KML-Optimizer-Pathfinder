from GeometricDataStructures.Mercator import MercatorPoint

class Clipper():

    def __init__(self):
        pass

    def verticalCheck(self, aLine, bLine):
        if aLine.start.x == aLine.end.x:
            aLine.slope = (aLine.end.y - aLine.start.y) / (aLine.end.x - aLine.start.x)
            aLine.cept = aLine.start.y - (aLine.slope * aLine.start.x)
            y = (aLine.slope * bLine.start.x) + aLine.cept
            return MercatorPoint(bLine.start.x, y)
        else: return None


def my_line_intersection(PointA, PointB, PointC, PointD):

    if((if_intersect(PointA, PointB, PointC, PointD) == False)):
        return None

    xdiff = (PointA[0] - PointB[0], PointC[0] - PointD[0])
    ydiff = (PointA[1] - PointB[1], PointC[1] - PointD[1])

    def deterMinent(a, b):
        return (a[0] * b[1] - a[1] * b[0])

    div = deterMinent(xdiff, ydiff)
    if(div == 0):
        raise Exception("No POI")


    d = (deterMinent(PointA, PointB), deterMinent(PointC, PointD))
    resultx = deterMinent(d, xdiff) / div
    resulty = deterMinent(d, ydiff) / div
    return resultx, resulty

def my_gradient(PointA, PointB):
    m = None
    if(PointA[0] != PointB[0]):
        m = (1./(PointA[0] - PointB[0]) * (PointA[1] - PointB[1]))
        return m

def if_intersect(As, Ae, Bs, Be):

    def findOrientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]);
        if (val == 0.0):
            return 0        # Orientation.COLLINEAR
        if(val > 0):
            return -1       #Orientation.RIGHT
        return 1            #Orientation.LEFT

    o1 = findOrientation(As, Ae, Bs);
    o2 = findOrientation(As, Ae, Be);
    o3 = findOrientation(Bs, Be, As);
    o4 = findOrientation(Bs, Be, Ae);

    if (o1 != o2 and o3 != o4):
       return True
    return False

A = (1.0, 1.0)
B = (1.0, 0.0)
C = (1.5, 0.5)
D = (-3.0, 0.5)

print my_line_intersection(A, B, C, D)