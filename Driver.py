from KmlFasade import KmlFasade
from UrlBuilder import UrlBuilder
from RestrictionEngine import RestrictionFactory
import ImageMerge
import Image
argzero = 'Inputs\KML Files\\advancedexample1.kml'
argtwo = 'Inputs\KML Files\\advancedexample2.kml'
argone = 'Inputs\KML Files\us_states.kml'

#Create the KmlFasade

fasade = KmlFasade(argone)
fasade.placemarkToGeometrics()
f = RestrictionFactory()
#f = f.newSquareRestriction([-103.528629, 41.260352], 2000)
f = f.newSquareRestriction([-69.871826, 39.833851], 500)
f.restrict(fasade.geometrics)
fasade.fasadeUpdate()
fasade.rewrite('Inputs\KML Files\\advancedexample1copy.kml')

#Build the Url

build = UrlBuilder('600x600')
#build.viewportparam(markerlist)
build.centerparams('39.833851,-74.871826', '5')

markerlist = []
for element in fasade.geometrics:
    element.switchCoordinates()
    print element.printCoordinates()
    if element.tag == "Point":
        markerlist.append(element.printCoordinates())
    if element.tag == "Polygon":
        #markerlist = element.coordinatesAsList()
        build.addpath({"color":"red", "weight":'5'}, element.coordinatesAsListStrings())
    if element.tag == "LineString":
        build.addpath({"color":"blue", "weight":'5'}, element.coordinatesAsListStrings())

build.addmarkers({"color":"blue"}, markerlist)
build.printUrls()

#Merge the Url Images
print "Number of urls: ", len(build.urllist) + 2
images = build.download()
print "Downloaded."

images = ImageMerge.convertPtoRGB(*images)
ImageMerge.mergeModeRGB('Inputs\Static Maps\Outfile.png', *images)
im = Image.open('Inputs\Static Maps\Outfile.png')
im.show()