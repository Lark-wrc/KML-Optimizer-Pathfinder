from math import radians, sin, cos, asin, sqrt, log
import Utils

ZOOM_CONSTANT = 10 + log(45, 2)  # Final Variable, Do Not Modify

class RestrictionFactory(object):

    def __init__(self):
        """
        Author: Bill Clark
        Version = 1.0
        """
        pass

    def newCenterDistanceRestriction(self, center, distance, metric=0):
        """
        See CenterDistanceRestriction, this method returns a new instance of that object.
        """
        return CenterDistanceRestriction(center, distance, metric)


# kinda really an interface
class Restriction(object):

    def __init__(self):
        """
        Author: Bill Clark
        Version = 1.0
        An 'interface' (as interface as python gets) for new Restrictions. With it templating and the composite
        methods can be built into the restriction engines.
        """
        pass

    def restrict(self, geometrics):
        """
        Author: Bill Clark
        Version = 1.0
        The primary method for a restriction. The only method that *should* be called from outside the class.
        Should modify the geometrics it gets, (not remove them) as the implementation chooses to do so.
        :param geometrics: A list of geometric objects, which wrap an xml coordinate tag for easy access.
        """
        pass

    def zoom(width):
        """
        Author: Nick LaPosta
        Version = 1.0
        Determines the proper zoom level and filter range for the given frame size
        :param width: The desired size in miles for the view port.
        :return: A tuple of the zoom level and the filter range respectively
        """
        zoom_level = ZOOM_CONSTANT - log(width, 2)
        filter_range = sqrt(width)
        return zoom_level, filter_range

    def haversine(start, end, metric=0):
        """
        Author: Nick LaPosta, Bill Clark
        Version = 1.0
        Uses the mathematical function of the same name to find the distance between two long lat coordinates.
        :param start: The first coordinate, a long lat value pair in a list.
        :param end: The second coordinate, a long lat value pair in a list.
        :param metric: A boolean value to use the metric system or imperial system.
        :return: The distance in the given metric system.
        """

        start = [start[1], start[0]]
        end = [end[1], end[0]]

        if metric:
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


class SquareRestriction(Restriction):
    def __init__(self, center, distance, metric=0):
        """
        Author: Bill Clark
        Version = 1.1
        A restriction that flags all points that are not with in distance x from a given center point to be removed.
        :param center: the center point to draw distances from.
        :param distance: the distance in the given metric that a point must be within from center.
        :param metric: the measure of distance to be used. True is metric system, False is imperial (miles).
        """
        self.center = center
        self.distance = distance

    def restrict(self, geometrics):
        """
        Author: Bill Clark
        Version = 1.0
        :param geometrics: A list of geometric objects, which wrap an xml coordinate tag for easy access.
        """
        pass


class CenterDistanceRestriction(Restriction):

    def __init__(self, center, distance, metric=0):
        """
        Author: Bill Clark
        Version = 1.1
        A restriction that flags all points that are not with in distance x from a given center point to be removed.
        :param center: the center point to draw distances from.
        :param distance: the distance in the given metric that a point must be within from center.
        :param metric: the measure of distance to be used. True is metric system, False is imperial (miles).
        """

        self.center = center
        self.distance = distance

    def restrict(self, geometrics):
        """
        Author: Bill Clark
        Version = 1.3
        Looks at each geometric object in the list and, if it is not within distance of center, flags it for removal.
        :param geometrics: A list of geometic objects.
        """

        for geometry in geometrics:
            if geometry.tag == "Point":
                d = Utils.haversine(self.center, geometry.coordinates[0])
                if d > self.distance:
                    geometry.remove = 1
            elif geometry.tag == "LineString":
                for coord in geometry.coordinates:
                    d = Utils.haversine(self.center, coord)
                    if d <= self.distance:
                        pass
                    else:
                        geometry.remove = 1
                        break
            elif geometry.tag == "LinearRing":
                for coord in geometry.coordinates:
                    d = Utils.haversine(self.center, coord)
                    if d <= self.distance:
                        pass
                    else:
                        geometry.remove = 1
                        break