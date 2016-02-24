from KmlFasade import KmlFasade
from UrlBuilder import UrlBuilder
from RestrictionEngine import RestrictionFactory
argzero = 'C:\Users\Research\Documents\KML Files\\advancedexample1.kml'
argtwo = 'C:\Users\Research\Documents\KML Files\\advancedexample2.kml'
argone = 'C:\Users\Research\Documents\KML Files\us_states.kml'

#Create the KmlFasade

fasade = KmlFasade(argzero)
fasade.placemarkToGeometrics()
f = RestrictionFactory()
#f = f.newSquareRestriction([-103.528629, 41.260352], 2000)
f = f.newSquareRestriction([-74.871826, 39.833851], 500)
f.restrict(fasade.geometrics)
fasade.fasadeUpdate()
fasade.rewrite('C:\Users\Research\Documents\KML Files\\advancedexample1copy.kml')

build = UrlBuilder('600x600')
#build.viewportparam(markerlist)
build.centerparams('39.833851,-74.871826', '7')

markerlist = []
for element in fasade.geometrics:
    element.switchCoordinates()
    print element.printCoordinates()
    if element.tag == "Point":
        markerlist.append(element.printCoordinates())
    if element.tag == "Polygon":
        build.addpath({"color":"red", "weight":'5'}, element.printCoordinates())
    if element.tag == "LineString":
        build.addpath({"color":"blue", "weight":'5'}, element.printCoordinates())

#build.addmarkers({"color":"yellow"}, markerlist)
print build.url
