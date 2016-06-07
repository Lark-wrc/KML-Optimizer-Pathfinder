from math import sqrt, log
from WeilerAtherton import WeilerClipping

ZOOM_CONSTANT = 10 + log(45, 2)  # Final Variable, Do Not Modify


class RestrictionFactory(object):

    def __init__(self, metric=0):
        """
        `Author`: Bill Clark

        This method generates a new restriction. The factory makes sure that every restriction created works off
        the same measurement scale, metric or imperial.
        """
        self.metric = metric

    def newSquareRestriction(self, viewport):
        """
        `Author`: Bill Clark

        See SquareRestriction, this method returns a new instance of that object.
        """
        return SquareRestriction(viewport)

    def newWAClipping(self, viewport):
        """
        `Author`: Bill Clark

        see MercatorRestriction, this method returns a new instance of the object.
        """
        return WAClippingRestriction(viewport)


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

        Determines the proper  zoom level and filter range for the given frame size.

        `width`: The desired size in miles for the view port.

        `return`: A tuple of the zoom level and the filter range respectively
        """
        zoom_level = ZOOM_CONSTANT - log(width, 2)
        filter_range = sqrt(width)
        return zoom_level, filter_range


class WAClippingRestriction(Restriction):

    def __init__(self, viewport):
        """
        `Author`: Bill Clark

        This method uses the weiler atherton algorithm module to clip geometrics. Any points and lines
        within the viewport's corners are left in the geometric, everything else is removed. The polygon
        is closed as well.

        `Viewport`: = The return from the get_corners method of the mercator module. This is the 4 points
        that make up the corner of the viewport.
        """
        super(WAClippingRestriction, self).__init__(0)
        self.viewport = viewport
        self.NW = self.viewport[1]
        self.SE = self.viewport[3]

    def restrict(self, geometrics):
        """
        `Author`: Bill Clark

        This restriction iterates all through the provided list of geometrics. On each iteration,
        the coordinates in the geometry are checked for two things; being within the viewport of the
        Restriction and if the point is an entry point. An entry point is required for WA clipping to work,
        simply a point that the prior point was not in the viewport. After the iteration, any geometry that is
        partially in the viewport is clipped via the WeilerAtherton module.

        `geometrics`: list of geometric objects.
        """
        atherton = WeilerClipping()
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
                newgeometry = atherton.clip(geometry.coordinates, self.viewport)
                geometry.coordinates[:] = newgeometry

    def pointWithinCorners(self, coordinates):
        """
        `Author`: Bill Clark

        Returns true if the given coordinates are contained by this classes NW and SE lines. Helper method to
        restrict.

        `coordinates`: A LatLongPoint object.

        `return`: True if the point is contained, false else.
        """
        if coordinates.lng >= self.NW.lng and coordinates.lng <= self.SE.lng:
            if coordinates.lat <= self.NW.lat and coordinates.lat >= self.SE.lat:
                return True
        return False


class SquareRestriction(Restriction):

    def __init__(self, viewport):
        """
        `Author`: Bill Clark

        DEPRECIATED: Use WAClipping.

        A restriction that flags all points that are not within distance x from a given center point to be removed.
        This is done in a square pattern by using two points, the NW corner and the SW corner. 

        `center`: the center point to draw distances from.

        `distance`: the distance in the given metric that a point must be within from center.

        `metric`: the measure of distance to be used. True is metric system, False is imperial (miles).
        """
        super(SquareRestriction, self).__init__(0)
        self.viewport = viewport
        self.NW = self.viewport[1]
        self.SE = self.viewport[3]

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
                if not self.pointWithinCorners(geometry.coordinates[0]):
                    geometry.remove = 1
            elif geometry.tag == "LineString" or geometry.tag == "LinearRing" or geometry.tag == "Polygon":
                for coord in geometry.coordinates:
                    if self.pointWithinCorners(coord):
                        pass
                    else:
                        geometry.remove = len(geometry.coordinates)
                        break
            else:
                print "uh oh spagettios."

    def pointWithinCorners(self, coordinates):
        """
        `Author`: Bill Clark

        Returns true if the given coordinates are contained by this classes NW and SE lines. Helper method to
        restrict.

        `coordinates`: A LatLongPoint object.

        `return`: True if the point is contained, false else.
        """
        if coordinates.lng >= self.NW.lng and coordinates.lng <= self.SE.lng:
            if coordinates.lat <= self.NW.lat and coordinates.lat >= self.SE.lat:
                return True
        return False
