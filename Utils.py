"""
The Utility module contains individual methods that are useful to multiple others.
The value of having each of these pulled out is simply that they can be accessed from
a variety of modules, preventing code repetition.
"""


from lxml import etree
from math import radians, sin, cos, sqrt, asin

debug = 0
geometryTypes = ('Point', 'LineString','LinearRing', 'MultiGeometry') #Polygon is removed

def elementPrint(element, bool=0):
    """
    Author: Bill Clark
    Version = 1.0
    Quick method to print an lxml element. For quicker writing.
    :param element: lxml element.
    :param bool: To pretty print or to compress to a single line.
    :return: the tostring of the element.
    """

    if bool:
        return etree.tostring(element, pretty_print=False)
    else:
        return etree.tostring(element, pretty_print=True)


def coordinateDistance(start, end):
    #print start, end, sqrt(((end[0]-start[0])**2)+((end[1]-start[1])**2))
    return sqrt(((end[0]-start[0])**2)+((end[1]-start[1])**2))


def haversine(start, end, metric=0):
    """
    Author: Nick Laposta, Bill Clark
    Version = 1.0
    Uses the mathmatical function of the same name to find the distance between two long lat coordinates.
    :param start: The first coordinate, a long lat value pair in a list.
    :param end: The second coordinate, a long lat value pair in a list.
    :param metric: A boolean value to use the metric system or imperial system.
    :return: The distance in the given metric system.
    """

    start = [start[1],start[0]]
    end = [end[1],end[0]]

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

    #  Returns distance in km
    #print start, end, r * c
    return r * c

#haversine([39.706583333333334, 75.11438888888888], [39.71036111111111, 75.12022222222221])
