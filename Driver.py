from KmlFasade import KmlFasade
from UrlBuilder import UrlBuilder
from RestrictionEngine import RestrictionFactory
import ImageMerge
import Image
import Utils
import time
argzero = 'Inputs\KML Files\\advancedexample1.kml'
argtwo = 'Inputs\KML Files\\advancedexample2.kml'
argone = 'Inputs\KML Files\us_states.kml'
argarctic = 'Inputs\KML FIles\\arctic lines jan 31.kml'

#Create the KmlFasade

fasade = KmlFasade(argarctic)
fasade.placemarkToGeometrics()
f = RestrictionFactory()
#f = f.newSquareRestriction([-103.528629, 41.260352], 2000)
f = f.newSquareRestriction([-64.871826, 66.833851], 4000)
f.restrict(fasade.geometrics)
fasade.fasadeUpdate()
fasade.rewrite('Inputs\KML Files\\rewritten recent.kml')

#Build the Url

build = UrlBuilder('600x600')
#build.viewportparam(markerlist)
build.centerparams('-64.871826,66.833851', '4')

markerlist = []
for element in fasade.geometrics:
    element.switchCoordinates()
    #print element.printCoordinates()
    if element.tag == "Point":
        markerlist.append(element.printCoordinates())
    if element.tag == "Polygon":
        #markerlist = element.coordinatesAsList()
        build.addpath({"color":"red", "weight":'5'}, element.coordinatesAsListStrings())
    if element.tag == "LineString":
        build.addpath({"color":"blue", "weight":'5'}, element.coordinatesAsListStrings())

build.addmarkers({"color":"blue"}, markerlist)
build.printUrls()

print "Number of urls: ", len(build.urllist) + 2

#Merge the Url Images

#merges by downloading everything and merging everything.

images = build.download()
print "Downloaded."
images = ImageMerge.convertPtoRGB(*images)
ImageMerge.mergeModeRGB('Inputs\Static Maps\Outfile.png', *images)

#merges by downloading, merging, and repeating till none are left.

# ImageMerge.debug = 0
#
# layers = ImageMerge.MergeGenerator('Inputs\Static Maps\Outfile.png', build.downloadBase())
# for img in build.downloadGenerator():
#     im = ImageMerge.convertPtoRGB(img)[0]
#     layers.add(im)


im = Image.open('Inputs\Static Maps\Outfile.png')
im.show()
