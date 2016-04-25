from GeometricDataStructures.Mercator import MercatorPoint
from GeometricDataStructures.Geometrics import LatLongPoint
import math

class Clipper():

    def __init__(self):
        pass

    def getLineIntersection(self, pointA, pointB, pointC, pointD):
        """
        `Author`: Bob Seedorf, Eliakah K.

        Returns the point, as a tuple, at which the line segments composed composed of points A, B and points C, D intersect
        First the tuple of the difference in the x's an y's of points A, B and then points C, D are found.
        Next the determinent of the xdiffs and ydiffs is found and stored in div for later reference.
        Next the determinent of the the individual lines, A, B and C, D are found, this yields value d.
        Subsequently the cooresponding point of intersection's x and y values are found through the division of the determinent of d and ydiff and d and xdiff by div
        The return is the pair of values, resutltx and resulty, representing the coordinate pair that is the the point of intersection
        NOTE: Does NOT check if lines intersect, as a precondition that should be accomplished before this method is called

        `pointA`: start point of first line
        `pointB`: end point of first line
        `pointC`: start point of second line
        `pointD`: end point of second line
        """

        # if pointC.lng == pointD.lng:
        #     line1m = (pointB.lat - pointA.lat) / (pointB.lng - pointA.lng)
        #     line1b = pointA.lat - (line1m * pointA.lng)
        #     y = (line1m * pointC.lng) + line1b
        #     return LatLongPoint(y, pointC.lng)
        # if pointA.lng == pointB.lng:
        #     line2m = (pointD.lat - pointC.lat) / (pointD.lng - pointC.lng)
        #     line2b = pointC.lat - (line2m * pointC.lng)
        #     y = (line2m * pointA.lng) + line2b
        #     return LatLongPoint(y, pointA.lng)
        # line1m = (pointB.lat - pointA.lat) / (pointB.lng - pointA.lng)
        # line2m = (pointD.lat - pointC.lat) / (pointD.lng - pointC.lng)
        # line1b = pointA.lat - (line1m * pointA.lng)
        # line2b = pointC.lat - (line2m * pointC.lng)
        # x = ((-1 * line1b) + line2b) / (line1m - line2m)
        # y = (line1m * x) + line1b
        # return LatLongPoint(y, x)

        xdiff = pointA.lng - pointB.lng, pointC.lng - pointD.lng
        ydiff = pointA.lat - pointB.lat, pointC.lat - pointD.lat

        div = self.determinentTup(xdiff, ydiff)
        d = self.determinentPoint(pointA, pointB), self.determinentPoint(pointC, pointD)

        resultx = float(self.determinentTup(d, xdiff)) / float(div)
        resulty = float(self.determinentTup(d, ydiff)) / float(div)
        return LatLongPoint(resulty, resultx)

    def determinentTup(self, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the algebraic determinent of the parameterized tuple using linear combinations of their coordinate pairs ([0], [1]).
         _    _
        | A, C |
        |_B, D_|    =   (A * D) - (B * C) = return value

        `pointA`: start point of line
        `pointB`: end point of line
        """
        return (pointA[0] * pointB[1] - pointA[1] * pointB[0])

    def determinentPoint(self, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the algebraic determinent of the parameterized LatLongPoints using linear combinations of their coordinate pairs (lat, lng).
        Uses similar manner to that described above
        Note: this method will only work when used on LatlongPoints, as it requires lat, lng object s

        `pointA`: start point of line
        `pointB`: end point of line
        """
        return (pointA.lng * pointB.lat - pointA.lat * pointB.lng)

    def doLinesIntersect(self, pointA, pointB, pointC, pointD):
        """
        `Author`: Bob Seedorf, Eliakah K.

        Returns True if the line segments composed of points A, B and points C, D have an intersection point
        By finding the orientation of any three given points the trait of the lines intersection can be determined through relatioinal equality
        The orientation of the lines, being only the decision that they rotate either clockwise, counterclockwise, or not at all (collinear) is used to determine the
        In the case that the orientation of A, B, and C is the same as A, B, and D, and the the orientation of C, D, and A is the same as C, D, and B, then the lines do not intersect

        `pointA`: start point of first line
        `pointB`: end point of first line
        `pointC`: start point of second line
        `pointD`: end point of second line
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

        Returns orientation of three given points in coordinate space.
        Through projection of the combinations of lines and extraneous points the slopes of the projections are found to be of an appropriate orientatoin

        `pointA`: first point being passed
        `pointB`: second point being passed
        `pointC`: third point being passed
        """
        val = (pointB.lat - pointA.lat) * (pointC.lng - pointB.lng) - (pointB.lng - pointA.lng) * (pointC.lat - pointB.lat);
        if (val == 0.0): return 0   # Orientation.COLLINEAR
        elif (val > 0): return -1   # Orientation.RIGHT
        else: return 1              # Orientation.LEFT

    def getClosestPoint(self, target, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the point, of only pointA or pointB, that is dimensionally closest to the point target
        By using the pythagorean theorem and calculating the hypotenuse of the triangle composed of sides difference in x and difference in y for the two given points, the closest point is selected based on this distance.
        NOTE: in the case that the two points are of equal distance, point A will be chosen over point B

        `target`: control point form whom the distances of the other two will be checked
        `pointA`: first point to be checked, has return precedence over pointB
        `pointB`: second point to be checked
        """
        distToA = math.sqrt(((target.lng - pointA.lng) ** 2) + (target.lat - pointA.lat) ** 2)
        distToB = math.sqrt(((target.lng - pointB.lng) ** 2) + (target.lat - pointB.lat) ** 2)
        return pointA if distToA <= distToB else pointB

    def getClipped(self, P, Q, Ie):
        """
        `Author`: Bob S, Nick L, Bill C.

        This method returns the result of the clipping algorithm as a collection of coordinate pairs; a list of tuples
        Using the collections, P, Q, and Ie, the resultant clipped polyogn is found through an iteration over P and Q based on Ie.
        The collection of P is used to find all the necessary points on the subject polygon, while the collection of Q is used to find the necessary points on the viewport polygon.
        by 'bouncing back and forth' between these two collections, as we pop intersection points off Ie, the bounded regiion of the result is constructed and returned as a list of points representing every vertex of the shape

        `return`: result, the collection of tuples representing the points of the new polygon
        """
        # P = [(2.0, 2.25), (1.4, 3.0), (1.0, 3.5), (0.557142857142857, 3.0), (-1.0, 1.241935483870968), (-2.1, 0.0), (0.0, -3.0), (2.0, -1.0), (2.0, -1.0), (3.0, 0.0), (3.0, 1.0)]
        # Q = [(2.0, 3.0), (1.4, 3.0), (0.557142857142857, 3.0), (-1.0, 3.0), (-1.0, 1.241935483870968), (-1.0, -1.0), (2.0,-1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, 2.25)]
        # Ie = Stack()
        # Ie.items = [(2.0, -1.0), (2.0, -1.0), (-1.0, 1.241935483870968), (0.557142857142857, 3.0), (1.4, 3.0), (2.0, 2.25)]
        # result should be: [(2.0, 2.25), (1.4, 3.0), (0.557142857142857, 3.0), (-1.0, 1.241935483870968), (-1.0,
        # -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0), (2.0, -1.0)]

        result = Stack()
        reserve = Ie.peek()
        location = reserve
        flag = 1
        while flag:
            Ie.pop()
            end = Ie.peek()
            index = P.index(location)
            while not location == end :
                location.rewrap()
                result.push(location)
                index = (index+1) % len(P)
                location = P[index]
            Ie.pop()

            if Ie.isEmpty():
                end = reserve
                flag = 0
            else:
                end = Ie.peek()

            index = Q.index(location)
            while not location == end:
                location.rewrap()
                result.push(location)
                index = (index+1) % len(Q)
                location = Q[index]
            # try:
            #     end = Ie.peek()
            # except Exception:
            #     end = reserve
            #     flag = False
        return result

    def getP(self, subjectlines, viewportlines):
        """
        'Author' Bob S. Nick L. and Bill C.

        This method caluctlates and mainatnins the lsit of points, P, to be used during the iterative phase of the getCLipped method

        :param subjectlines:
        :param viewportlines:
        :return: P, the collection of all points that lie on the subject lines of the polyogn being examined
        """
        P = []
        Ie = Stack()
        for subjectline in reversed(subjectlines):
            P.append(subjectline[1])
            crossCount = 0
            for viewportline in viewportlines:
                poi = None
                if self.doLinesIntersect(subjectline[0], subjectline[1], viewportline[0], viewportline[1]):
                    poi = self.getLineIntersection(subjectline[0], subjectline[1], viewportline[0], viewportline[1])
                    P.append(poi)
                    Ie.push(poi)
                    crossCount += 1
                if crossCount > 1:
                    if Ie.peek() == self.getClosestPoint(P[-3], Ie[-2], Ie[-1]):
                        # perform swap
                        Ie.items[-1], Ie.items[-2] = Ie.items[-2], Ie.items[-1]
                        P[-1], P[-2] = P[-2], P[-1]
                if crossCount == 2:
                    break
        P.reverse()
        return P, Ie

    def getQ(self, viewportlines, Ie):
        """
        'Author' Bob S. Nick L., and Bill C.

        this method returns the collection, Q, of all points that lie on the lines of the viewport polyogn being examined
        By iterating over Ie, the list of points of intersection, every point of intersection cooresponding to the line starting with the point at index 1-4 of the viewport is checked and ordered as to generate a counter clockwise, flattened collection of the viewport
        :param viewportlines:
        :param Ie:
        :return: Q, the collection of all points that lie on the viewport polygon
        """
        Q = []
        storagebank = []
        for i in range(0, 4):
            corner = viewportlines[i][0]
            storage = []
            storage.append(corner)
            for point in Ie:
                corner_coords = [corner.lat, corner.lng]
                point_coords = [point.lat, point.lng]
                if corner_coords[i % 2] == point_coords[i % 2]:
                    storage.append(point)
                #if i == 0 or i == 2:
                #    if(corner.lat == point.lat):
                #        storage.append(point)
                #else:  # i == 1 or i == 3
                #    if(corner.lng == point.lng):
                #        storage.append(point)
            storagebank.append(storage)
        storagebank[0].sort(key=lambda tup: tup.lng, reverse=True)
        storagebank[1].sort(key=lambda tup: tup.lat, reverse=True)
        storagebank[2].sort(key=lambda tup: tup.lng)
        storagebank[3].sort(key=lambda tup: tup.lat)
        Q = storagebank[0] + storagebank[1] + storagebank[2] + storagebank[3]
        return Q

    def unwrap(self, list):
        """
        'Author' Bob S. and Nick L.

        this method 'wraps' the longitude points of an *already un-flattened list*
        By ensuring the polygon crosses the anti-meridian, then moving all points that extend around the anti-meridian going negative to positive;
        by moving those points into the extra dimensional standard coordinate plain 'off the map' from the polar plain

        :param list - the un-flattened list of the polygon being modified
        :return: None, this method statically modifies the parameterized list
        """
        for p in list:
            if (p[0].lng * p[1].lng) < 0:    # if one is negative and the other positive
                if p[0].lng > p[1].lng:
                    if p[0].lng - p[1].lng > 180:
                        p[1].lng = p[1].lng + 360
                elif p[1].lng > p[0].lng:
                    if p[1].lng - p[0].lng > 180:
                        p[0].lng = p[0].lng + 360

    def unFlattenList(self, list):
        """
        'Author' Bob S.

        this method 'un-flattens' the list being passed
        by creating a tuple of each lat-long-point and it's respective neighbor a new list of 'lines' is created for the purpose of iteration by the necessary methods.

        :param list - list to be modified.
        :return: new list of tuples of coordinate pairs (LatLongPoints) for the subsequent methods
        """
        temp = list[1:] + list[:1]  # rotate list by one, to the left
        return zip(list, temp)      # zip list, with the stepped temp to create all necessary point pairs; lines


    def runMe(self, subjectlines, viewportlines):

        # unflatten subject viewport...
        subjectlines = self.unFlattenList(subjectlines)
        viewportlines = [(viewportlines[0], viewportlines[1]), (viewportlines[1], viewportlines[2]),(viewportlines[2], viewportlines[3]),(viewportlines[3], viewportlines[0])]

        # next unwrap these line sets
        self.unwrap(subjectlines)
        self.unwrap(viewportlines)

        # run me, in order
        P, Ie = self.getP(subjectlines, viewportlines)         # find P
        print "P :",P
        print "Ie:", Ie.items
        Q = self.getQ(viewportlines, Ie)                       # find Q
        print "Q :",Q
        result = self.getClipped(P, Q, Ie)                     # get clipped

        return result


class Stack():
     """
     'Author' Bob S.

     this class is used only to ensure the proper procedures of the getClipped algorithm are executed appropriately

     """
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

     def __getitem__(self, int):
         return self.items[int]

if __name__ == '__main__':

    clipper = Clipper()

    # P = [(2.0, 2.25), (1.4, 3.0), (1.0, 3.5), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0), (0.0, -3.0), (0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5), (3.0, 1.0)]
    # Q = [(2.0, 3.0), (1.4, 3.0), (0.8571428571428571, 3.0), (-1.0, 3.0), (-1.0, -1.0), (0.0, -1.0), (0.6666666666666666, -1.0), (2.0, -1.0), (2.0, 0.5), (2.0, 2.25)]
    # Ie = Stack()
    # Ie.items = [(2.0, 0.5), (0.6666666666666666, -1.0), (0.0, -1.0), (0.8571428571428571, 3.0), (1.4, 3.0), (2.0, 2.25)]
    # # Result should be: [(2.0, 2.25), (1.4, 3.0), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0), (0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5)]
    #
    # result = clipper.getClipped(P, Q, Ie).items
    # print result
    # test = [(2.0, 2.25), (1.4, 3.0), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0),(0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5)]
    #
    # subjectlines = [((3.0, 1.0), (1.0, 3.5)) , ((1.0, 3.5), (0.0, 0.0)), ((0.0, 0.0), (0.0, -3.0)), ((0.0, -3.0), (1.0, 0.0)), ((1.0, 0.0), (3.0, 1.0))]
    # viewportlines = [((2.0, 3.0), (-1.0, 3.0)),  ((-1.0, 3.0), (-1.0, -1.0)),  ((-1.0, -1.0), (2.0, -1.0)),  ((2.0, -1.0), (2.0, 3.0))]
    #
    # testP = [(2.0, 2.25), (1.4, 3.0), (1.0, 3.5), (0.8571428571428571, 3.0), (0.0, 0.0), (0.0, -1.0), (0.0, -3.0), (0.6666666666666666, -1.0), (1.0, 0.0), (2.0, 0.5), (3.0, 1.0)]
    # testP.reverse()
    # testIe = [(2.0, 0.5), (0.6666666666666666, -1.0), (0.0, -1.0), (0.8571428571428571, 3.0), (1.4, 3.0), (2.0, 2.25)]
    # resultP, resultIe = clipper.getP(subjectlines, viewportlines)
    # print (testP == resultP, testIe == resultIe)
    # print (testIe)
    # print (resultIe.items)
    #
    # testQ = [(2.0, 3.0), (1.4, 3.0), (0.8571428571428571, 3.0), (-1.0, 3.0), (-1.0, -1.0), (0.0, -1.0), (0.6666666666666666, -1.0), (2.0, -1.0), (2.0, 0.5), (2.0, 2.25)]
    # resultQ = clipper.getQ(viewportlines, testIe)
    # print (testQ == resultQ)
    # print (testQ)
    # print (resultQ)
    #
    # print test == result
    # print test
    # print clipper.getClipped(resultP, resultQ, resultIe).items


    subjectlines = [LatLongPoint(1,3), LatLongPoint(3.5,1), LatLongPoint(0,0), LatLongPoint(-3,0), LatLongPoint(0,1)]
    viewportlines = [LatLongPoint(3,2), LatLongPoint(3,-1), LatLongPoint(-1,-1), LatLongPoint(-1,2)]
    for point in clipper.runMe(subjectlines, viewportlines).items:
        print point

    print "\n--------------------------------------------------------------------------------------------\n"

    subjectlines = [LatLongPoint(1,3), LatLongPoint(3.5,1), LatLongPoint(1.5,0.75), LatLongPoint(3.5,0.5), LatLongPoint(1,-0.5)]
    viewportlines = [LatLongPoint(3,2), LatLongPoint(3,-1), LatLongPoint(-1,-1), LatLongPoint(-1,2)]
    for point in clipper.runMe(subjectlines, viewportlines).items:
        print point

    print "\n--------------------------------------------------------------------------------------------\n"

    list = [(-122.084073,37.430983152841), (-122.08387556846,37.430981784499),
          (-122.07566645719,37.428010604887), (-122.07553564869,37.427893171576),
          (-122.07293386374,37.420439569303), (-122.07296986194,37.420285414427),
          (-122.07876327046,37.41406822808), (-122.07893836645,37.41399584117),
          (-122.08830978301,37.41367089012), (-122.08849215429,37.413730881959),
          (-122.09494567437,37.419523409628), (-122.09499845163,37.419674486238),
          (-122.09322460731,37.427279812044), (-122.09310718708,37.427405852613),
          (-122.08446780291,37.430977679891), (-122.08427043154,37.430981784499),
          (-122.084073,37.430983152841)]

    newlist = list[0::2]
    lllist = []

    for pair in newlist:
        lllist.append(LatLongPoint(pair[1], pair[0]))

    for ll in lllist:
        print ll

    subjectlines = lllist
    viewportlines = [LatLongPoint(37.419523409628, -122.09494567437), LatLongPoint(37.427279812044, -122.09322460731), LatLongPoint(37.430977679891,-122.08446780291), LatLongPoint(37.430983152841,-122.084073)]
    for point in clipper.runMe(subjectlines, viewportlines).items:
        print point

