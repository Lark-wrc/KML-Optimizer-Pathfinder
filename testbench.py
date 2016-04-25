from GeometricDataStructures.Geometrics import LatLongPoint
from Clipper import Clipper

def unwrap(list):

    for p in list:
        if (p[0].lng * p[1].lng) < 0:    # if one is negative and the other positive
            if p[0].lng > p[1].lng:
                if p[0].lng - p[1].lng > 180:
                    p[1].lng = p[1].lng + 360
            elif p[1].lng > p[0].lng:
                if p[1].lng - p[0].lng > 180:
                    p[0].lng = p[0].lng + 360

clipper = Clipper()

# broken
# subjectlines1 = [LatLongPoint(87, -155), LatLongPoint(87, -205), LatLongPoint(0,-255), LatLongPoint(-87, -205), LatLongPoint(-87, -155), LatLongPoint(0, -105)]
# subjectlines2 = [LatLongPoint(87, -155), LatLongPoint(87, -205), LatLongPoint(0,-255), LatLongPoint(-87, -205), LatLongPoint(-87, -155), LatLongPoint(0, -105)]

# simple rectangle - works
subjectlines1 = [LatLongPoint(30, -170), LatLongPoint(30, 170), LatLongPoint(-30, 170), LatLongPoint(-30, -170)]
subjectlines2 = [LatLongPoint(30, -170), LatLongPoint(30, 170), LatLongPoint(-30, 170), LatLongPoint(-30, -170)]

# another simple rectangle - works
subjectlines1 = [LatLongPoint(30, 170), LatLongPoint(-30, 170), LatLongPoint(-30, -170), LatLongPoint(30, -170)]
subjectlines2 = [LatLongPoint(30, 170), LatLongPoint(-30, 170), LatLongPoint(-30, -170), LatLongPoint(30, -170)]

# simple rectangle at 0,0 - break system; rectangle is too wide (wider than 180)
subjectlines1 = [LatLongPoint(30, -90), LatLongPoint(30, 91), LatLongPoint(-30, 91), LatLongPoint(-30, -90)]
subjectlines2 = [LatLongPoint(30, -90), LatLongPoint(30, 91), LatLongPoint(-30, 91), LatLongPoint(-30, -90)]


control = clipper.unFlattenList(subjectlines1)
test = clipper.unFlattenList(subjectlines2)

print control
print test

print "\n-------------------------------\n"

unwrap(test)

print control
print test

# do some stuff on the subjectlines / viewport lines here
print "\n-------------------------------\n"
# this ti sthe psot processing for the lat/lng's

for p in test:
    p[0].rewrap()
    p[1].rewrap()

print test
