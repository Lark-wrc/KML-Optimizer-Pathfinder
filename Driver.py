from KmlFasade import KmlFasade
from UrlBuilder import UrlBuilder
from RestrictionEngine import RestrictionFactory
argzero = 'C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1.kml'

#Create the KmlFasade

fasade = KmlFasade(argzero)
fasade.placemarkToGeometrics()
f = RestrictionFactory()
f = f.newSquareRestriction([-103.528629, 41.260352], 5000)
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
#build.viewportparam(markerlist)
#build.centerparams('-103.528629,41.260352', '11')
build.addmarkers({"color":"yellow"}, markerlist)
build.addpath({"color":"red", "weight":'5'}, element.printCoordinates())
print build.url
