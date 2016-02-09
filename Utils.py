from lxml import etree
from math import radians, sin, cos, sqrt, asin
debug = 0
geometryTypes = ('Point', 'LineString','LinearRing', 'MultiGeometry') #Polygon is removed

def elementPrint(element, bool=0):
    if bool:
        return etree.tostring(element, pretty_print=False)
    else:
        return etree.tostring(element, pretty_print=True)


def coordinateDistance(start, end):
    print start, end, sqrt(((end[0]-start[0])**2)+((end[1]-start[1])**2))
    return sqrt(((end[0]-start[0])**2)+((end[1]-start[1])**2))



# def haversine(start, end):
#
#     R = 6372.8 # Earth radius in kilometers
#
#     dLat = radians(end[0] - start[0])
#     dLon = radians(end[1] - start[1])
#     start[0] = radians(start[0])
#     end[0] = radians(end[0])
#
#     a = sin(dLat/2)**2 + cos(start[0])*cos(end[0])*sin(dLon/2)**2
#     c = 2*asin(sqrt(a))
#
#     print start, end, R*c
#     return R * c