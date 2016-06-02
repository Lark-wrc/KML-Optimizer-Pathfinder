from PIL import Image

import StaticMapsConnections.ImageMerge as ImageMerge
from GeometricDataStructures.Geometrics import LatLongPoint
from GeometricDataStructures.KmlFasade import KmlFasade
from GeometricDataStructures.Mercator import *
from RestrictionEngine.RestrictionEngine import RestrictionFactory
from StaticMapsConnections.UrlBuilder import UrlBuilder

argzero = 'Inputs\KML Files\\advancedexample1.kml'
argtwo = 'Inputs\KML Files\\advancedexample2.kml'
argone = 'Inputs\KML Files\us_states.kml'
argarctic = 'Inputs\KML FIles\\arctic lines jan 31.kml'
argtest = 'Inputs\KML FIles\\tester.kml'

#center = [-103.528629, 41.260352]
center = [-103, 41]
centerPoint = LatLongPoint(center[0], center[1])
zoom = 8
size = 600

#Create some restrictions.
merc = MercatorProjection()
f = RestrictionFactory()

clipped = f.newWAClipping(merc.get_corners(centerPoint, zoom, size, size))



#Create the KmlFasade

fasade = KmlFasade(argone)
fasade.placemarkToGeometrics()
fasade.removeGarbageTags()

clipped.restrict(fasade.geometrics)
fasade.fasadeUpdate()
fasade.rewrite('Outputs\\Driver Rewrite.kml')



#Build the Url



build = UrlBuilder(size)
build.centerparams(','.join([repr(x) for x in center]), repr(zoom))

markerlist = []
for element in fasade.geometrics:
    if element.tag == "Point":
        markerlist.append(element.printCoordinates())
    if len(element.element.attrib) > 0 and element.element.attrib["id"] == "Viewport":
        build.addpath({"color":"red", "weight":'5'}, element.coordinatesAsListStrings())
    elif element.tag == "Polygon":
        build.addpath({"color":"blue", "weight":'5'}, element.coordinatesAsListStrings())
    if element.tag == "LineString":
        build.addpath({"color":"yellow", "weight":'5'}, element.coordinatesAsListStrings())

build.addmarkers({"color":"yellow"}, '41.3079222,-74.6096236')
build.printUrls()

print "Number of urls: ", len(build.urllist) + 2

#Merge the Url Images

#merges by downloading everything and merging everything.
images = build.download()
print "Downloaded."
im = ImageMerge.Merger('Outputs\Outfile.png', images[0])
print images[0]
im.mergeAll(*images)

im = Image.open('Outputs\Outfile.png')
im.show()
