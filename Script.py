from KmlFasade import KmlFasade
from UrlBuilder import UrlBuilder
from RestrictionEngine import CenterDistanceRestriction
argzero = 'C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1.kml'

#Create the KmlFasade

fasade = KmlFasade(argzero)
fasade.placemarkToGeometrics()
f = CenterDistanceRestriction([-103.528629, 41.260352], 1025.17)
f.restrict(fasade.geometrics)
fasade.fasadeUpdate()
fasade.rewrite('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1copy.kml')

markerlist = []
for element in fasade.geometrics:
    element.switchCoordinates()
    print element.printCoordinates()
    if element.tag == "Point":
        markerlist.append(element.printCoordinates())

build = UrlBuilder('600x600')
build.viewportparam(markerlist)
build.addmarkers({}, markerlist)
build.addpath({"fillcolor":"blue", "weight":'2'}, element.coordinateStringList())
print build.url
