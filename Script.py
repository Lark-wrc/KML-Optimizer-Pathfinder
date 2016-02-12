from KmlFasade import KmlFasade
from UrlBuilder import UrlBuilder
from RestrictionEngine import CenterDistanceRestriction
argzero = 'C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1.kml'

#Create the KmlFasade

fasade = KmlFasade(argzero)
fasade.placemarkToGeometrics()
f = CenterDistanceRestriction([-99.000000,40.000000], 5000)
f.restrict(fasade.geometrics)
fasade.fasadeUpdate()

markerlist = []
for element in fasade.geometrics:
    if element.tag == "Point":
        markerlist.append(element.switchCoordinates())
print markerlist

build = UrlBuilder('600x600')
build.viewportparam(markerlist)
build.addmarkers({}, markerlist)
print build.url
