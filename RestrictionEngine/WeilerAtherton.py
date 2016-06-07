from GeometricDataStructures.Geometrics import LatLongPoint
import math

class WeilerClipping:
    """
    `Author`: Bob S. Bill C. Nick L. and Eliakah K.

    This class encapsulates all of the functionality of our implementation of the 'Weiler Atherton' Polygon Clipping Algorithm.

    Included are all of the arithmetic operations, transformations and calculations necessary to accomplish our goal.
    First build the polygons composed of the subject, being clipped, and the viewport against which the subject is being clipped are defined
    Next we construct the integral collections, P, Q, and Ie (see the methods getP and getQ) to stage the execution of clipping.
    Finally, these collections are fed into the clip method, that returns the new polygon as a flat list of points, in sequence, representing the new polygon as a set of vertices

    """

    def __init__(self, debug=0):
        self.debug = debug

    def getLineIntersection(self, pointA, pointB, pointC, pointD):
        """
        `Author`: Bob Seedorf, Eliakah K.

        Returns the point, as a LatLongPoint object, at which the line segments composed of points A, B and points C, D intersect
        First the tuple of the difference in the x's an y's of points A, B and then points C, D are found.
        Next the determinant of the difference of the x values y values, respctively, are stored
        Next the determinant of the the individual lines, A, B and C, D are found, this yields value d.
        Subsequently the corresponding point of intersection's x and y values are found through the division of the determinant of d and ydiff and d and xdiff by div
        The return is the pair of values, resutltx and resulty, representing the coordinate pair that is the point of intersection

        NOTE: Does NOT check if lines intersect, as a precondition that should be accomplished before this method is called

        `pointA`: start point of first line

        `pointB`: end point of first line

        `pointC`: start point of second line

        `pointD`: end point of second line
        """

        xdiff = pointA.lng - pointB.lng, pointC.lng - pointD.lng
        ydiff = pointA.lat - pointB.lat, pointC.lat - pointD.lat

        div = self.determinant(xdiff, ydiff)
        d = self.determinant(pointA.getTup(), pointB.getTup()), self.determinant(pointC.getTup(), pointD.getTup())

        resultx = float(self.determinant(d, xdiff)) / float(div)
        resulty = float(self.determinant(d, ydiff)) / float(div)
        return LatLongPoint(resulty, resultx)

    def determinant(self, tupA, tupB):
        """
        `Author`: Bob Seedorf

        Returns the algebraic determinant of the parameterized tuple using linear combinations of their coordinate pairs ([0], [1]).
         _    _
        | A  C |
        |_B, D_|    =   (A * D) - (B * C) = return value

        `pointA`: start point of line

        `pointB`: end point of line
        """
        return (tupA[0] * tupB[1] - tupB[0] * tupA[1])

    def doLinesIntersect(self, pointA, pointB, pointC, pointD):
        """
        `Author`: Bob Seedorf, Eliakah K.

        Returns True if the line segments composed of points A, B and points C, D have an intersection point.
        By finding the orientation of any three given points the traits of the lines intersection can be determined through relational equality
        The orientation of the lines, being only the decision that they rotate either clockwise, counterclockwise, or not at all (collinear) is used to determine the
        In the case that the orientation of A, B, and C is the same as A, B, and D, and the the orientation of C, D, and A is the same as C, D, and B, then the lines do not intersect

        `pointA`: start point of first line

        `pointB`: end point of first line

        `pointC`: start point of second line

        `pointD`: end point of second line
        """

        o1 = self.findOrientation(pointA, pointB, pointC)
        o2 = self.findOrientation(pointA, pointB, pointD)
        o3 = self.findOrientation(pointC, pointD, pointA)
        o4 = self.findOrientation(pointC, pointD, pointB)

        if o1 != o2 and o3 != o4:
            return True
        return False

    def findOrientation(self, pointA, pointB, pointC):
        """
        `Author`: Bob Seedorf

        Returns orientation of three given points in coordinate space.
        The assumption lines drawn between points A, B and B, C and C, A are used to define this 'orientation'
        Through projection of the combinations of lines and extraneous points the slopes of the projections are found to be of an appropriate orientatoin

        `pointA`: first point being passed

        `pointB`: second point being passed

        `pointC`: third point being passed
        """
        val = (pointB.lat - pointA.lat) * (pointC.lng - pointB.lng) - \
              (pointB.lng - pointA.lng) * (pointC.lat - pointB.lat);
        if val == 0.0: return 0   # Orientation.COLLINEAR
        elif val > 0: return -1   # Orientation.RIGHT
        else: return 1            # Orientation.LEFT

    def getClosestPoint(self, target, pointA, pointB):
        """
        `Author`: Bob Seedorf

        Returns the point, of the set {pointA, pointB} that is dimensionally closest to the point target
        By using the pythagorean theorem and calculating the hypotenuse of the triangle composed of sides of the difference in x and difference in y for the two given points, the closest point is selected based on this distance.

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
        Using the collections, P, Q, and Ie, the resultant clipped polygon is found through an iteration over P and Q based on Ie.
        The collection of P is used to find all the necessary points on the subject polygon, while the collection of Q is used to find the necessary points on the viewport polygon.
        by 'bouncing back and forth' between these two collections, as we pop intersection points off Ie, the bounded region of the result is constructed in a dynamic fashion and returned as a list of points representing every vertex of the shape

        `return`: result, the collection of tuples representing the points of the new polygon

        """

        result = []
        reserve = Ie[-1]
        location = reserve
        flag = 1
        while flag:
            Ie.pop()
            end = Ie[-1]
            index = P.index(location)
            while not location == end:
                location.rewrap()
                result.append(location)
                index = (index+1) % len(P)
                location = P[index]
            Ie.pop()

            if len(Ie) == 0:
                end = reserve
                flag = 0
            else:
                end = Ie[-1]

            index = Q.index(location)
            while not location == end:
                location.rewrap()
                result.append(location)
                index = (index+1) % len(Q)
                location = Q[index]
        return result

    def getP(self, subjectlines, viewportlines):
        """
        'Author' Bob S. Nick L. and Bill C.

        This method calculates and maintains the list of points, P, to be used during the iterative phase of the getCLipped method

        `subjectlines`: The collection points that compose all vertices of the subject which we are clipping

        `viewportlines`: The collection of points that compose all vertices of the restriction space, against which, we are clipping subjectlines

        `return`: P and Ie, the collection of all points that lie on the subject lines of the polygon being examined and the collection of all points of intersection respectively
        """
        P = []
        Ie = []
        for subjectline in reversed(subjectlines):
            P.append(subjectline[1])
            crossCount = 0
            for viewportline in viewportlines:
                poi = None
                if self.doLinesIntersect(subjectline[0], subjectline[1], viewportline[0], viewportline[1]):
                    poi = self.getLineIntersection(subjectline[0], subjectline[1], viewportline[0], viewportline[1])
                    P.append(poi)
                    Ie.append(poi)
                    crossCount += 1
                if crossCount > 1:
                    if Ie[-1] == self.getClosestPoint(P[-3], Ie[-2], Ie[-1]):
                        # perform swap
                        Ie[-1], Ie[-2] = Ie[-2], Ie[-1]
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

        `viewportlines`: The collection of points that compose all vertices of the restriction space, against which, we are clipping subjectlines

        `Ie`:  and the collection of all points of intersection between subjeclines and viewportlines

        `return`: Q, the collection of all points that lie on the viewport polygon
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

        NOTE: this method acts on the implication that the points of the polygon being transformed are NO MORE than 180 degrees apart longitudinally
        This is required to be the case as there exists no other way to determine whether or not a point should or should not be transformed
        By relying on a maximum limit, we have chosen to be 180, the polyogns' diemnsion are capped at a width of no more 180 degreees
        However, the path of the visualization software in google earth will not limit the capacity for polygons' dimensions to exceed 180 degrees width

        `list`: the un-flattened list of the polygon being modified

        `return`: None, this method statically modifies the parameterized list
        """
        for p in list:
            if (p[0].lng * p[1].lng) < 0:    # if one is negative and the other positive
                if p[0].lng > p[1].lng:
                    if p[0].lng - p[1].lng > 180:
                        p[1].lng = p[1].lng + 360
                elif p[1].lng > p[0].lng:
                    if p[1].lng - p[0].lng > 180:
                        p[0].lng = p[0].lng + 360

    def rewrap(self, list):
        """
        'Author' Bob S.

        This method 're-wraps' all the elements of a given list of tuples of Lat Long Points by calculating each of the coordinate pair's values individually

        `list`: the un-flattened list of the polygon being modified

        `return`: None, this method statically modifies the parameterized list
        """
        for p in list:
            p[0].rewrap()
            p[1].rewrap()

    def unFlattenList(self, list):
        """
        'Author' Bob S.

        this method 'un-flattens' the list being passed
        by creating a tuple of each lat-long-point and it's respective neighbor a new list of 'lines' is created for the purpose of iteration by the necessary methods.

        `list`: list to be modified.

        `return`: new list of tuples of coordinate pairs (LatLongPoints) for the subsequent methods
        """
        temp = list[1:] + list[:1]  # rotate list by one, to the left
        return zip(list, temp)      # zip list, with the stepped temp to create all necessary point pairs; lines


    def clip(self, subjectlines, viewportlines):
        """
        This method takes in flattened, lists of lat long points representing the polygon of the subject polygon and the viewport polygon.
        first the two collections are un-flattened to form the list of lists needed to run the algorithm
        Next the lists are unwrapped to fold them over the anti-meridian, allowing analysis of continuous lines in the solution space
        Next the three integral collections P, Ie, and Q are found using the deferred methods
        Finally the resultant clipped polygon is found with a call to the local method and returned

        `subjectlines`: list of points on subject shape
        `viewportlines`: list of pints on the viewport shape
        `return`: the result of the call to get clipped
        """

        # un-flatten subject viewport
        subjectlines = self.unFlattenList(subjectlines)
        viewportlines = [(viewportlines[0], viewportlines[1]), (viewportlines[1], viewportlines[2]),(viewportlines[2], viewportlines[3]),(viewportlines[3], viewportlines[0])]

        # next unwrap these line sets
        self.unwrap(subjectlines)
        self.unwrap(viewportlines)

        # find P, Ie
        P, Ie = self.getP(subjectlines, viewportlines)
        if self.debug: print "P :",P
        if self.debug: print "Ie:", Ie
        if not Ie or Ie == []:
            return None

        # then find Q
        Q = self.getQ(viewportlines, Ie)
        if self.debug: print "Q :",Q

        # then get Clipped
        result = self.getClipped(P, Q, Ie)
        result.append(result[0])
        return result
