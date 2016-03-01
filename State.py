global lon_min
global lon_max
global lat_min
global lat_max

global NE, SE, NW, SW
global corner_points


class State:

    def __init__(self, lon, lat):
        """
        Author: Nick LaPosta
        Version = 1.0
        A state class that represents the location of a point relative to the region
        :param lon: The longitude value of the point
        :param lat: The latitude value of the point
        """
        self.longitude = lon
        self.latitude = lat
        if lon < lon_min:
            self.lon = 0
        elif lon > lon_max:
            self.lon = 2
        else:
            self.lon = 1

        if lat < lat_min:
            self.lat = 0
        elif lat > lat_max:
            self.lat = 2
        else:
            self.lat = 1

    def get_slope(self):
        """
        Author: Nick LaPosta
        Version = 1.0
        Returns the slopes that should be used for the intersection calculation.
        :return: A tuple of the slopes of the two comparison lines sorted in ascending order
        """
        points = corner_points[self.lon * 3 + self.lat]
        first_slope = float(self.latitude - points[0][1]) / float(self.longitude - points[0][0])
        second_slope = float(self.latitude - points[1][1]) / float(self.longitude - points[1][0])
        if first_slope > second_slope:
            return second_slope, first_slope
        else:
            return first_slope, second_slope

    def in_region(self):
        """
        Author: Nick LaPosta
        Version = 1.0
        :return: A boolean value of the state's presence in the region
        """
        return self.lon == 1 and self.lat == 1

    def __cmp__(self, other):
        """
        Author: Nick LaPosta
        Version = 1.0
        Compares the two states and returns True if a line between them could possibly intersect the region
        :param other: The second State to compare to this one
        :return: A boolean value representing possible intersection with region
        """
        if self.lon == other.lon:  # Checks all possibilities where the lon states are the same
            if self.lon != 1:      # All states where both points are on the same side of the region
                return False
            else:
                if self.lat != other.lat or self.lat == 1:  # If the lat states are not equal or one is in the region
                    return True
                else:
                    return False

        elif self.lat == other.lat:  # Checks all possibilities where the lat states are the same
            if self.lat != 1:      # All states where both points are on the same side of the region
                return False
            else:
                if self.lon != other.lon or self.lon == 1:  # If the lon states are not equal or one is in the region
                    return True
                else:
                    return False
        return True


def init_state(northwest, southeast):
    """
    Author: Nick LaPosta
    Version = 1.0
    Initializes the global fields that is shared by all instances of State
    :param northwest: Top left coordinate list
    :param southeast: Bottom right coordinate list
    """
    global lon_min
    global lon_max
    global lat_min
    global lat_max
    (lon_min, lat_max) = northwest
    (lon_max, lat_min) = southeast

    global NE
    global SE
    global NW
    global SW
    NE = (lon_max, lat_max)
    SE = (lon_max, lat_min)
    NW = (lon_min, lat_max)
    SW = (lon_min, lat_min)

    global corner_points
    corner_points = [[[NE, SW]], [[NW, SW]], [[NW, SE]], [[NW, NE]],
                     [(0, 0), (0, 0)],
                     [[SW, SE]], [[NW, SE]], [[NE, SE]], [[NE, SW]]]
