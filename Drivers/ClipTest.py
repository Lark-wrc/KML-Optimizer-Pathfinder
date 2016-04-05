from RestrictionEngine import Clipper
from GeometricDataStructures import Geometrics, KmlFasade

gf = Geometrics.GeometricFactory()
viewport = gf.createLiteral(None, "LineString", "2,3 -1,3 -1,-1 2,-1 2,3")
subject = gf.createLiteral(None, "LineString", "3,1 1,3.5 0,0 0,-3 1,0 3,1")

a = KmlFasade.LatLongPoint(-1, 0)
b = KmlFasade.LatLongPoint(1, 0)
c = KmlFasade.LatLongPoint(-1, -1)
d = KmlFasade.LatLongPoint(1, 1)

print Clipper.intersect(a, b, c, d)


intersection = Clipper.clip(viewport, subject)#.coordinates

print type(intersection)

for i in intersection:
    print i
