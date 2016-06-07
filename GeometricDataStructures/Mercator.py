from __future__ import division
import math
from GeometricDataStructures.Geometrics import LatLongPoint


class MercatorPoint:
    """
    `Author`: Nick LaPosta

    Container for the location of a pixel on a Mercator map projection
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class MercatorProjection:
    """
    `Author`: Nick LaPosta

    Contains conversion functions to convert a GeoPoint to a GeoLatLng and back using a center pixel of a Mercator map
    projection.
    """

    def __init__(self):
        """
        `Author`: Nick LaPosta

        Creates a pixel coordinate for the center point of the map that every pixel coordinate will be relative to as
        well as the ratio of longitude degrees/radians to pixels
        """
        # Google Maps full Earth image is 256x256 pixels
        self.MERCATOR_RANGE = 256
        self.pixelOrigin_ = MercatorPoint(self.MERCATOR_RANGE / 2, self.MERCATOR_RANGE / 2)
        self.pixelsPerLonDegree_ = self.MERCATOR_RANGE / 360
        self.pixelsPerLonRadian_ = self.MERCATOR_RANGE / (2 * math.pi)

    def from_lat_lng_to_point(self, lat_lng, opt_point=None):
        """
        `Author`: Nick LaPosta

        Converts a GeoLatLng object into a GeoPoint object

        `lat_lng`:  The GeoLatLng object that will be converted into a GeoPoint object

        `opt_point`:  The GeoPoint that will contain the converted GeoLatLng. Default creates a new GeoPoint

        `return`:  A GeoPoint that refers to the same location on the map by pixel rather than by latitude and longitude
        """
        point = opt_point if opt_point is not None else MercatorPoint(0, 0)
        origin = self.pixelOrigin_
        point.x = origin.x + lat_lng.lng * self.pixelsPerLonDegree_
        # NOTE: Truncating to 0.9999 effectively limits latitude to
        # 89.189.  This is about a third of a tile past the edge of the world tile.
        sin_y = self.bound(math.sin(self.degrees_to_radians(lat_lng.lat)), -0.9999, 0.9999)
        point.y = origin.y + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -self.pixelsPerLonRadian_
        return point

    def from_point_to_lat_lng(self, point):
        """
        `Author`: Nick LaPosta

        Converts a GeoPoint object into a GeoPoint object

        `point`:  The GeoPoint object that will be converted into a GeoLatLng object

        `return`:  A GeoLatLng that refers to the same location on the map by latitude and longitude rather than by pixel
        """
        origin = self.pixelOrigin_
        lng = (point.x - origin.x) / self.pixelsPerLonDegree_
        lat_radians = (point.y - origin.y) / -self.pixelsPerLonRadian_
        lat = self.radians_to_degrees(2 * math.atan(math.exp(lat_radians)) - math.pi / 2)
        return LatLongPoint(lat, lng)

    def bound(self, value, opt_min, opt_max):
        """

        :param value:
        :param opt_min:
        :param opt_max:
        :return:
        """
        if opt_min is not None:
            value = max(value, opt_min)
        if opt_max is not None:
            value = min(value, opt_max)
        return value

    def degrees_to_radians(self, deg):
        """
        `Author`: Nick LaPosta

        Converts degrees to radians

        `deg`:  Angle in degrees

        `return`:  Angle in radians
        """
        return deg * (math.pi / 180)

    def radians_to_degrees(self, rad):
        """
        `Author`: Nick LaPosta

        Converts radians to degrees

        `rad`:  Angle in radians

        `return`:  Angle in degrees
        """
        return rad / (math.pi / 180)

    def get_corners(self, center, zoom, map_width, map_height):
        """
        `Author`: Nick LaPosta

        This function returns a dict of all of the corner points and the four cardinal direction limits of the image that
        will be downloaded from the Google Maps API

        `center`:  The center GeoLatLng object that the URL will use as the center

        `zoom`:  The zoom level that the UrlBuilder will use to generate the image

        `map_width`:  The pixel width of the image to be downloaded

        `map_height`:  The pixel height of the image to be downloaded

        `return`:  A dict of all of the corner points and the four cardinal direction limits of the image
        """
        scale = 2 ** zoom

        center_pixel = self.from_lat_lng_to_point(center)

        # Create Latitude and Longitude for the North East point of the image
        ne_point = MercatorPoint(center_pixel.x + (map_width / 2) / scale, center_pixel.y - (map_height / 2) / scale)
        ne_lat_lon = self.from_point_to_lat_lng(ne_point)

        # Create Latitude and Longitude for the North West point of the image
        nw_point = MercatorPoint(center_pixel.x - (map_width / 2) / scale, center_pixel.y - (map_height / 2) / scale)
        nw_lat_lon = self.from_point_to_lat_lng(nw_point)

        # Create Latitude and Longitude for the South East point of the image
        se_point = MercatorPoint(center_pixel.x + (map_width / 2) / scale, center_pixel.y + (map_height / 2) / scale)
        se_lat_lon = self.from_point_to_lat_lng(se_point)

        # Create Latitude and Longitude for the South West point of the image
        sw_point = MercatorPoint(center_pixel.x - (map_width / 2) / scale, center_pixel.y + (map_height / 2) / scale)
        sw_lat_lon = self.from_point_to_lat_lng(sw_point)

        # return dict(N=ne_lat_lon.lat, E=ne_lat_lon.lng, S=sw_lat_lon.lat, W=sw_lat_lon.lng,
        #             NE=ne_lat_lon, NW=nw_lat_lon, SE=se_lat_lon, SW=sw_lat_lon)

        return (ne_lat_lon, nw_lat_lon, sw_lat_lon, se_lat_lon)
