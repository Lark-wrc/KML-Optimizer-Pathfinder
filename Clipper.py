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
        if not self.doLinesIntersect(pointA, pointB, pointC, pointD): return None

        xdiff = pointA[0] - pointB[0], pointC[0] - pointD[0]
        ydiff = pointA[1] - pointB[1], pointC[1] - pointD[1]

        div = self.determinent(xdiff, ydiff)
        if(div == 0): raise Exception("No POI")

        d = self.determinent(pointA, pointB), self.determinent(pointC, pointD)
        resultx = self.determinent(d, xdiff) / div
        resulty = self.determinent(d, ydiff) / div
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

        o1 = self.findOrientation(pointA, pointB, pointC);
        o2 = self.findOrientation(pointA, pointB, pointD);
        o3 = self.findOrientation(pointC, pointD, pointA);
        o4 = self.findOrientation(pointC, pointD, pointB);

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

    def getClosestPoint(self, target, pointA, pointB):
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

    def getClipped(self, P, Q, Ie):
        """
        'Author': Bob S. and Nick L.

        This method returns the result of the clipping algorithm as a collection of coordinate pairs

        :return: result, the collection of tuples representing the points of the new polygon
        """
        # P = [(2.0, 2.25), (1.4, 3.0), (1.0, 3.5), (0.557142857142857, 3.0), (-1.0, 1.241935483870968), (-2.1, 0.0), (0.0, -3.0), (2.0, -1.0), (2.0, -1.0), (3.0, 0.0), (3.0, 1.0)]
        # Q = [(2.0, 3.0), (1.4, 3.0), (0.557142857142857, 3.0), (-1.0, 3.0), (-1.0, 1.241935483870968), (-1.0, -1.0), (2.0,-1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, 2.25)]
        # Ie = Stack()
        # Ie.items = [(2.0, -1.0), (2.0, -1.0), (-1.0, 1.241935483870968), (0.557142857142857, 3.0), (1.4, 3.0), (2.0, 2.25)]
        # result should be: [(2.0, 2.25), (1.4, 3.0), (0.557142857142857, 3.0), (-1.0, 1.241935483870968), (-1.0,
        # -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0)]


        result = Stack()
        result.items = []
        reserve = Ie.peek()
        location = reserve
        flag = True
        while(flag):
            Ie.pop()
            end = Ie.peek()
            index = P.index(location)
            while( not location == end):
                result.push(location)
                index += 1
                index = index % len(P)
                location = P[index]
            Ie.pop()
            try:
                end = Ie.peek()
            except Exception:
                end = reserve
                flag = False
            finally:
                index = Q.index(location)
                while ( not location == end):
                    result.push(location)
                    index += 1
                    index = index % len(Q)
                    location = Q[index]
        return result

    def getP(self, subjectlines, viewportlines):

        P = []
        Ie = Stack()
        Ie.items = []
        for subjectline in reversed(subjectlines):
            P.append(subjectline[1])
            crossCount = 0
            for viewportline in viewportlines:
                poi = None
                if (self.doLinesIntersect(subjectline[0], subjectline[1], viewportline[0], viewportline[1])):
                    poi = self.getLineIntersection(subjectline[0], subjectline[1], viewportline[0], viewportline[1])
                    P.append(poi)
                    Ie.push(poi)
                    crossCount += 1
                if (crossCount > 1):
                    if(Ie.peek() == self.getClosestPoint(P[len(P) - 3], P[len(P) - 2], P[len(P) - 1])):
                        # perform swap
                        a, b = len(P) - 2, len(P) - 1
                        Ie[b], Ie[a] = Ie[a], Ie[b]
        return P, Ie

    def getQ(self, viewportlines, Ie):

        Q = []
        corner = viewportlines[0][0]
        storage = []
        Q.append(corner)
        for point in Ie:
            if (corner[1] == point[1]):
                storage.append(point)
        storage.sort(key=lambda tup: tup[0], reverse = True)
        Q.extend(storage)

        corner = viewportlines[1][0]
        storage = []
        Q.append(corner)
        for point in Ie:
            if (corner[0] == point[0]):
                storage.append(point)
        storage.sort(key=lambda tup: tup[1], reverse = True)
        Q.extend(storage)

        corner = viewportlines[2][0]
        storage = []
        Q.append(corner)
        for point in Ie:
            if (corner[1] == point[1]):
                storage.append(point)
        storage.sort(key=lambda tup: tup[0])
        Q.extend(storage)

        corner = viewportlines[3][0]
        storage = []
        Q.append(corner)
        for point in Ie:
            if (corner[0] == point[0]):
                storage.append(point)
        storage.sort(key=lambda tup: tup[1])
        Q.extend(storage)

        return Q

class Stack():

     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         if(len(self.items)-1 < 0):
             raise Exception
         return self.items.pop()

     def peek(self):
         if(self.isEmpty()):
             raise Exception
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

if __name__ == '__main__':

    clipper = Clipper()
    P = [(2.0, 2.25), (1.4, 3.0), (1.0, 3.5), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0), (0.0, -3.0), (0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5), (3.0, 1.0)]
    Q = [(2.0, 3.0), (1.4, 3.0), (0.8571428571428571, 3.0), (-1.0, 3.0), (-1.0, -1.0), (0.0, -1.0), (0.6666666666666666, -1.0), (2.0, -1.0), (2.0, 0.5), (2.0, 2.25)]
    Ie = Stack()
    Ie.items = [(2.0, 0.5), (0.6666666666666666, -1.0), (0.0, -1.0), (0.8571428571428571, 3.0), (1.4, 3.0), (2.0, 2.25)]
    # Result should be: [(2.0, 2.25), (1.4, 3.0), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0),
    # (0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5)]

    result = clipper.getClipped(P, Q, Ie).items
    print result
    test = [(2.0, 2.25), (1.4, 3.0), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0),(0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5)]

    subjectlines = [((3.0, 1.0), (1.0, 3.5)) , ((1.0, 3.5), (0.0, 0.0)), ((0.0, 0.0), (0.0, -3.0)), ((0.0, -3.0), (1.0, 0.0)), ((1.0, 0.0), (3.0, 1.0))]
    viewportlines = [((2.0, 3.0), (-1.0, 3.0)),  ((-1.0, 3.0), (-1.0, -1.0)),  ((-1.0, -1.0), (2.0, -1.0)),  ((2.0, -1.0), (2.0, 3.0))]

    testP = [(2.0, 2.25), (1.4, 3.0), (1.0, 3.5), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0), (0.0, -3.0), (0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5), (3.0, 1.0)]
    testP.reverse()
    testIe = [(2.0, 0.5), (0.6666666666666666, -1.0), (0.0, -1.0), (0.8571428571428571, 3.0), (1.4, 3.0), (2.0, 2.25)]
    resultP, resultIe = clipper.getP(subjectlines, viewportlines)
    print (testP == resultP, testIe == resultIe)
    print (testIe)
    print (resultIe.items)

    testQ = [(2.0, 3.0), (1.4, 3.0), (0.8571428571428571, 3.0), (-1.0, 3.0), (-1.0, -1.0), (0.0, -1.0), (0.6666666666666666, -1.0), (2.0, -1.0), (2.0, 0.5), (2.0, 2.25)]
    resultQ = clipper.getQ(viewportlines, testIe)
    print (testQ == resultQ)
    print (testQ)
    print (resultQ)

    print test == result
    print test
    print clipper.getClipped(resultP, resultQ, resultIe).items
    print "success"
