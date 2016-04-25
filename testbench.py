from GeometricDataStructures.Geometrics import LatLongPoint
from Clipper import Clipper

clipper = Clipper()
subjectlines = [LatLongPoint(87, -155), LatLongPoint(87, -255), LatLongPoint(0,-305), LatLongPoint(-87, -255), LatLongPoint(-87, -155), LatLongPoint(0, -105)]
subjectlines = clipper.unFlattenList(subjectlines)

for p in subjectlines:
    print p

print "\n-------------------------------\n"

anti_meridian = (LatLongPoint(180, -180), LatLongPoint(-180, -180))
for p in subjectlines:
    if(p[0].lng * p[1].lng < 0):
        start = p[0]
        end = p[1]
        poi = clipper.getLineIntersection(p[0], p[1], anti_meridian[0], anti_meridian[1])
        temp = p[1]
        p[1].lng = poi.lng
        p[1].lat = poi.lat
        subjectlines.insert(subjectlines.index(p) + 1, (poi, temp))

print "\n-------------------------------\n"
for p in subjectlines:
    print p

print LatLongPoint(0, -190)
print LatLongPoint(0, 181)
print LatLongPoint(-180, 255)
print LatLongPoint(180, -720)