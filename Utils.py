"""
The Utility module contains individual methods that are useful to multiple others.
The value of having each of these pulled out is simply that they can be accessed from
a variety of modules, preventing code repetition.
"""
import math
from lxml import etree

debug = 0
geometryTypes = ('Point', 'LineString','LinearRing', 'MultiGeometry')  # Polygon is removed

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
    return math.sqrt(((end[0]-start[0])**2)+((end[1]-start[1])**2))
