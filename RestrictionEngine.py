import json
import Utils


class RestrictionFactory(object):

    def __init__(self):
        """
        LOL not actually done.
        :return:
        """
        pass

    def newLocationRestriction(self):
        pass


# kinda really an interface
class Restriction(object):

    def __init__(self):
        """
        An 'interface' (as interface as python gets) for new Restrictions. With it templating and the composite
        methods can be built into the restriction engines.
        """
        pass

    def restrict(self, geometrics):
        """
        The primary method for a restriction. The only method that *should* be called from outside the class.
        Should modify the geometrics it gets, (not remove them) as the implementation chooses to do so.
        :param geometrics: A list of geometric objects, which wrap an xml coordinate tag for easy access.
        """
        pass


class LocationRadialRestriction(object):

    def __init__(self, center, distance, metric):
        """
        A restriction that flags all points that are not with in distance x from a given center point to be removed.
        :param center: the center point to draw distances from.
        :param distance: the distance in the given metric that a point must be within from center.
        :param metric: the measure of distance to be used. True is metric system, False is imperial (miles).
        """
        self.center = center
        self.distance = distance

    def restrict(self, geometrics):
        """
        Looks at each geometric object in the list and, if it is not within distance of center, flags it for removal.
        :param geometrics: A list of geometic objects.
        """
        for geometry in geometrics:
            d = Utils.coordinateDistance(self.center, geometry.coordinates)
            if d > self.distance:
                geometry.remove = 1
