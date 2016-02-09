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


def haversine(start, end, metric):
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
    print start, end, r * c
    return r * c

haversine([39.706583333333334, 75.11438888888888], [39.71036111111111, 75.12022222222221])
