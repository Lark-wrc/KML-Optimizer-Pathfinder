from math import radians, sin, cos, asin, sqrt, log
import State
from Clipper import Clipper

ZOOM_CONSTANT = 10 + log(45, 2)  # Final Variable, Do Not Modify


class RestrictionFactory(object):

    def __init__(self, metric=0):
        """
        `Author`: Bill Clark

        This method generates a new restriction. The factory makes sure that every restriction created works off
        the same measurement scale, metric or imperial.
        """
        self.metric = metric

    def newCircleRadiusRestriction(self, center, distance):
        """
        `Author`: Bill Clark

        See CircleRadiusRestriction, this method returns a new instance of that object.
        """
        return CircleRadiusRestriction(center, distance, self.metric)

    def newSquareRestriction(self, center, distance):
        """
        `Author`: Bill Clark

        See SquareRestriction, this method returns a new instance of that object.
        """
        return SquareRestriction(center, distance, self.metric)

    def newMercatorClipped(self, viewport):
        return MercatorClipperRestriction(viewport, 0)


class Restriction(object):

    def __init__(self, metric):
        """
        `Author`: Bill Clark

        An 'interface' (as interface as python gets) for new Restrictions. With it templating and the composite
        methods can be built into the restriction engines.
        """
        self.metric = metric
        self.debug = 0
        pass

    def restrict(self, geometrics):
        """
        `Author`: Bill Clark

        The primary method for a restriction. The only method that *should* be called from outside the class.
        Should modify the geometrics it gets, (not remove them) as the implementation chooses to do so.

        `geometrics`: A list of geometric objects, which wrap an xml coordinate tag for easy access.
        """
        pass

    def zoom(self, width):
        """
        `Author`: Nick LaPosta

        Determines the proper zoom level and filter range for the given frame size

        `width`: The desired size in miles for the view port.

        `return`: A tuple of the zoom level and the filter range respectively
        """
        zoom_level = ZOOM_CONSTANT - log(width, 2)
        filter_range = sqrt(width)
        return zoom_level, filter_range

    def haversine(self, start, end):
        """
        `Author`: Nick LaPosta, Bill Clark

        Uses the mathematical function of the same name to find the distance between two long lat coordinates.

        `start`: The first coordinate, a lat long value pair in a list.

        `end`: The second coordinate, a lat long value pair in a list.

        `return`: The distance in the given metric system.
        """

        start = [start[1], start[0]]
        end = [end[1], end[0]]

        if self.metric:
            r = 6371  # Earth radius in kilometers
        else:
            r = 3959  # Earth radius in miles

        d_lat = radians(end[0] - start[0])
        d_lon = radians(end[1] - start[1])
        start[0] = radians(start[0])
        end[0] = radians(end[0])
        a = sin(d_lat / 2)**2 + cos(start[0]) * cos(end[0]) * sin(d_lon / 2)**2
        c = 2*asin(sqrt(a))

        return r * c

class MercatorClipperRestriction(Restriction):

    def __init__(self, viewport, metric=0):
        super(MercatorClipperRestriction,self).__init__(metric)
        self.viewport = viewport
        self.NW = self.viewport[1]
        self.SE = self.viewport[3]


    def restrict(self, geometrics):
        clippy = Clipper()
        for geometry in geometrics:
            last_pos = -1
            startCoord = 0
            count = 0
            for coordin in geometry.coordinates:
                count = count+1
                if not self.pointWithinCorners(coordin):
                    geometry.remove += 1
                    curr_pos = 0
                else: curr_pos = 1

                if last_pos == 0 and curr_pos == 1:
                    startCoord = geometry.coordinates.index(coordin)-1
                last_pos = curr_pos

            length = len(geometry.coordinates)
            geometry.coordinates[:] = geometry.coordinates[-(length - startCoord):] + geometry.coordinates[:startCoord]
            if not length == geometry.remove and not geometry.remove == 0:  # Completely in/outside the viewport.
                newgeometry = clippy.runMe(geometry.coordinates, self.viewport)
                geometry.coordinates = newgeometry.items

    def pointWithinCorners(self, coordinates):
        """
        `Author`: Bill Clark

        Returns true if the given coordinates are contained by this classes NW and SE lines. Helper method to
        restrict.

        `coordinates`: List of coordinate values, long lat.

        `return`: True if the point is contained, false else.
        """
        if coordinates.lng >= self.NW.lng and coordinates.lng <= self.SE.lng:
            if coordinates.lat <= self.NW.lat and coordinates.lat >= self.SE.lat:
                return True
        return False


class SquareRestriction(Restriction):

    def __init__(self, center, distance, metric=0):
        """
        `Author`: Bill Clark

        A restriction that flags all points that are not within distance x from a given center point to be removed.
        This is done in a square pattern by using two points, the NW corner and the SW corner. 

        `center`: the center point to draw distances from.

        `distance`: the distance in the given metric that a point must be within from center.

        `metric`: the measure of distance to be used. True is metric system, False is imperial (miles).
        """
        super(SquareRestriction,self).__init__(metric)
        self.center = center
        self.distance = distance
        if metric:
            distance *= 0.62137
        latDist = distance/69
        lonDist = distance/(69.172)
        self.NW = [center[0]-lonDist, center[1]+latDist]
        self.SE = [center[0]+lonDist, center[1]-latDist]

    def restrict(self, geometrics):
        """
        `Author`: Bill Clark

        This method restricts based off of the NW and SE values this object contains. It looks at each point
        in a geometric and checks to see if it's contained by the lines drawn from NW and SE. If it's contained,
        we know that the point is in our frame of mind.

        `geometrics`: A list of geometric objects, which wrap an xml coordinate tag for easy access.
        """
        for geometry in geometrics:
            if geometry.tag == "Point":
                if not self.pointWithinDistance(geometry.coordinates[0].listed()):
                    geometry.remove = 1
            elif geometry.tag == "LineString" or geometry.tag == "LinearRing" or geometry.tag == "Polygon":
                for coord in geometry.coordinates:
                    if self.pointWithinDistance(coord.listed()):
                        pass
                    else:
                        geometry.remove = 1
                        break
            else:
                print "uh oh spagettios."

    def pointWithinDistance(self, coordinates):
        """
        `Author`: Bill Clark

        Returns true if the given coordinates are contained by this classes NW and SE lines. Helper method to
        restrict.

        `coordinates`: List of coordinate values, long lat.

        `return`: True if the point is contained, false else.
        """
        if coordinates[0] >= self.NW[0] and coordinates[0] <= self.SE[0]:
            if coordinates[1] <= self.NW[1] and coordinates[1] >= self.SE[1]:
                return True
        return False


    def intersect(self, start, end):
        """
        `Author`: Nick LaPosta

        A function for determining the possible intersection of the segment between two points and the region
        Warning! Does not properly function for a zone passing over the Anti-Prime Meridian, whatever that is called

        `start`: List containing longitude and latitude of start point of segment

        `end`: List containing longitude and latitude of end point of segment

        `return`: If the segment created by start and end intersects this region then return True, else return False
        """
        State.init_state(self.NW, self.SE)
        start_state = State(start[0], start[1])
        end_state = State(end[0], end[1])
        if cmp(start_state, end_state):
            # Check if line intersects
            if start_state.in_region() or end_state.in_region():
                return True
            else:
                line_slope = (start[1] - end[1]) / (start[0] - end[0])
                (min_slope, max_slope) = start_state.get_slope()
                if line_slope < min_slope or line_slope > max_slope:
                    return False
                else:
                    return True
        else:
            return False


class CircleRadiusRestriction(Restriction):

    def __init__(self, center, distance, metric=0):
        """
        `Author`: Bill Clark

        A restriction that flags all points that are not with in distance x from a given center point to be removed.

        `center`: the center point to draw distances from.

        `distance`: the distance in the given metric that a point must be within from center.

        `metric`: the measure of distance to be used. True is metric system, False is imperial (miles).
        """

        super(CircleRadiusRestriction,self).__init__(metric)
        self.center = center
        self.distance = distance

    def restrict(self, geometrics):
        """
        `Author`: Bill Clark

        Looks at each geometric object in the list and, if it is not within distance of center, flags it for removal.

        `geometrics`: A list of geometic objects.
        """

        for geometry in geometrics:
            if geometry.tag == "Point":
                d = self.haversine(self.center, geometry.coordinates[0].listed())
                if d > self.distance:
                    geometry.remove = 1
            elif geometry.tag == "LineString" or geometry.tag == "LinearRing" or geometry.tag == "Polygon":
                for coord in geometry.coordinates:
                    d = self.haversine(self.center, coord.listed())
                    if d <= self.distance:
                        pass
                    else:
                        geometry.remove = 1
                        break
            else:
                print "Are you sure that was a good idea?"