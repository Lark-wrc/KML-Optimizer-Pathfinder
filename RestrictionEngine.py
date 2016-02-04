import json
import Utils


class RestrictionFactory(object):

    def __init__(self):
        pass

    def newLocationRestriction(self):
        pass

# kinda really an interface
class Restriction(object):

    def __init__(self):
        pass

    def restrict(self, placemarks):
        pass


class LocationRadialRestriction(object):

    def __init__(self, center, distance):
        self.center = center
        self.distance = distance

    def restrict(self, geometrics):
        for element in geometrics:
            pass

