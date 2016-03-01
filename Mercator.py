from __future__ import division
import math
MERCATOR_RANGE = 256


def bound(value, opt_min, opt_max):
    if opt_min is not None:
        value = max(value, opt_min)
    if opt_max is not None:
        value = min(value, opt_max)
    return value


def degrees_to_radians(deg):
    return deg * (math.pi / 180)


def radians_to_degrees(rad):
    return rad / (math.pi / 180)


class GPoint:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class GLatLng:

    def __init__(self, lt, ln):
        self.lat = lt
        self.lng = ln


class MercatorProjection:

    def __init__(self):
        self.pixelOrigin_ = GPoint(MERCATOR_RANGE / 2, MERCATOR_RANGE / 2)
        self.pixelsPerLonDegree_ = MERCATOR_RANGE / 360
        self.pixelsPerLonRadian_ = MERCATOR_RANGE / (2 * math.pi)

    def fromLatLngToPoint(self, lat_lng, opt_point=None):
        point = opt_point if opt_point is not None else GPoint(0, 0)
        origin = self.pixelOrigin_
        point.x = origin.x + lat_lng.lng * self.pixelsPerLonDegree_
        # NOTE(appleton): Truncating to 0.9999 effectively limits latitude to
        # 89.189.  This is about a third of a tile past the edge of the world tile.
        siny = bound(math.sin(degrees_to_radians(lat_lng.lat)), -0.9999, 0.9999)
        point.y = origin.y + 0.5 * math.log((1 + siny) / (1 - siny)) * -self.pixelsPerLonRadian_
        return point

    def fromPointToLatLng(self, point):
        origin = self.pixelOrigin_
        lng = (point.x - origin.x) / self.pixelsPerLonDegree_
        latRadians = (point.y - origin.y) / -self.pixelsPerLonRadian_
        lat = radians_to_degrees(2 * math.atan(math.exp(latRadians)) - math.pi / 2)
        return GLatLng(lat, lng)

# pixelCoordinate = worldCoordinate * pow(2,zoomLevel)


def getCorners(center, zoom, mapWidth, mapHeight):
    scale = 2**zoom
    proj = MercatorProjection()

    centerPx = proj.fromLatLngToPoint(center)

    SWPoint = GPoint(centerPx.x-(mapWidth/2)/scale, centerPx.y+(mapHeight/2)/scale)
    SWLatLon = proj.fromPointToLatLng(SWPoint)

    NEPoint = GPoint(centerPx.x+(mapWidth/2)/scale, centerPx.y-(mapHeight/2)/scale)
    NELatLon = proj.fromPointToLatLng(NEPoint)
    return {
        'N': NELatLon.lat,
        'E': NELatLon.lng,
        'S': SWLatLon.lat,
        'W': SWLatLon.lng,
    }
