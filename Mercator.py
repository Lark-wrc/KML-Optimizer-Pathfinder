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


class GeoPoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class GeoLatLng:
    def __init__(self, lt, ln):
        self.lat = lt
        self.lng = ln

    def __repr__(self):
        return repr(self.lat) + "," + repr(self.lng)

class MercatorProjection:
    def __init__(self):
        self.pixelOrigin_ = GeoPoint(MERCATOR_RANGE / 2, MERCATOR_RANGE / 2)
        self.pixelsPerLonDegree_ = MERCATOR_RANGE / 360
        self.pixelsPerLonRadian_ = MERCATOR_RANGE / (2 * math.pi)

    def from_lat_lng_to_point(self, lat_lng, opt_point=None):
        point = opt_point if opt_point is not None else GeoPoint(0, 0)
        origin = self.pixelOrigin_
        point.x = origin.x + lat_lng.lng * self.pixelsPerLonDegree_
        # NOTE: Truncating to 0.9999 effectively limits latitude to
        # 89.189.  This is about a third of a tile past the edge of the world tile.
        sin_y = bound(math.sin(degrees_to_radians(lat_lng.lat)), -0.9999, 0.9999)
        point.y = origin.y + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -self.pixelsPerLonRadian_
        return point

    def from_point_to_lat_lng(self, point):
        origin = self.pixelOrigin_
        lng = (point.x - origin.x) / self.pixelsPerLonDegree_
        lat_radians = (point.y - origin.y) / -self.pixelsPerLonRadian_
        lat = radians_to_degrees(2 * math.atan(math.exp(lat_radians)) - math.pi / 2)
        return GeoLatLng(lat, lng)


def get_corners(center, zoom, map_width, map_height):
    scale = 2 ** zoom
    projection = MercatorProjection()

    center_pixel = projection.from_lat_lng_to_point(center)

    ne_point = GeoPoint(center_pixel.x + (map_width / 2) / scale, center_pixel.y - (map_height / 2) / scale)
    ne_lat_lon = projection.from_point_to_lat_lng(ne_point)

    nw_point = GeoPoint(center_pixel.x - (map_width / 2) / scale, center_pixel.y - (map_height / 2) / scale)
    nw_lat_lon = projection.from_point_to_lat_lng(nw_point)

    se_point = GeoPoint(center_pixel.x + (map_width / 2) / scale, center_pixel.y + (map_height / 2) / scale)
    se_lat_lon = projection.from_point_to_lat_lng(se_point)

    sw_point = GeoPoint(center_pixel.x - (map_width / 2) / scale, center_pixel.y + (map_height / 2) / scale)
    sw_lat_lon = projection.from_point_to_lat_lng(sw_point)

    return dict(N=ne_lat_lon.lat, E=ne_lat_lon.lng, S=sw_lat_lon.lat, W=sw_lat_lon.lng,
                NE=ne_lat_lon, NW=nw_lat_lon, SE=se_lat_lon, SW=sw_lat_lon)
