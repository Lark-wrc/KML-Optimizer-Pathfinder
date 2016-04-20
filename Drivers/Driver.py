from GeometricDataStructures.KmlFasade import KmlFasade
from StaticMapsConnections.UrlBuilder import UrlBuilder
from RestrictionEngine.RestrictionEngine import RestrictionFactory
import StaticMapsConnections.ImageMerge as ImageMerge
import Image
from GeometricDataStructures.Mercator import *
from GeometricDataStructures.Geometrics import LatLongPoint
import Clipper
import time


argzero = 'Inputs\KML Files\\advancedexample1.kml'
argtwo = 'Inputs\KML Files\\advancedexample2.kml'
argone = 'Inputs\KML Files\us_states.kml'
argarctic = 'Inputs\KML FIles\\arctic lines jan 31.kml'

#center = [-103.528629, 41.260352]
center = [40.0583, -74.4057] # jersey
centerPoint = LatLongPoint(center[0], center[1])
zoom = 7
size = 600

#Create some restrictions.
merc = MercatorProjection()
f = RestrictionFactory()

square = f.newSquareRestriction(center, 1000)
#square = f.newSquareRestriction([64.871826, 66.833851], 250)
clipped = f.newMercatorClipped(merc.get_corners(centerPoint, zoom, size, size))



#Create the KmlFasade



fasade = KmlFasade(argone)

fasade.placemarkToGeometrics()
fasade.garbageFilter()

clipped.restrict(fasade.geometrics)
fasade.fasadeUpdate()
fasade.rewrite('Outputs\\Driver Rewrite.kml')

#Create the KmlFasade

# fasade = KmlFasade(argone)
#
# fasade.placemarkToGeometrics()
# fasade.garbageFilter()
#
# square.restrict(fasade.geometrics)
# fasade.fasadeUpdate()
# fasade.rewrite('Outputs\\Driver Rewrite1.kml')

#Build the Url

build = UrlBuilder(size)
# build.centerparams('64.871826,66.833851', '4')
build.centerparams(','.join([repr(x) for x in center]), repr(zoom))

markerlist = []
for element in fasade.geometrics:
    #element.switchCoordinates()
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
ImageMerge.mergeModeRGB('Outputs\Outfile.png', *images)

#merges by downloading, merging, and repeating till none are left.

# ImageMerge.debug = 0
#
# layers = ImageMerge.MergeGenerator('Outputs\Outfile.png', build.downloadBase())
# for img in build.downloadGenerator():
#     im = ImageMerge.convertPtoRGB(img)[0]
#     layers.add(im)

im = Image.open('Outputs\Outfile.png')
im.show()
