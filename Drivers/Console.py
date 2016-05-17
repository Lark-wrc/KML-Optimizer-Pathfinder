import sys
from GeometricDataStructures.Geometrics import LatLongPoint
from PIL import Image
import StaticMapsConnections.ImageMerge as ImageMerge
from GeometricDataStructures.KmlFasade import KmlFasade
from GeometricDataStructures.Mercator import *
from RestrictionEngine.RestrictionEngine import RestrictionFactory
from StaticMapsConnections.UrlBuilder import UrlBuilder

class Parser():
    def __init__(self):
        self.switches = {'wa':0, 'w':0, 'sr':0, 'm':0, 'c':None, 'z':None, 's':None, 'v':0}

    def parse(self, flag, data):
        flag = flag[1:]
        if flag in self.switches:
            if not (flag == 'wa' or flag == 'v'):
                self.switches[flag] = data
            else:
                self.switches[flag] = 1
            return 1
        else:
            print "Error: flag", flag, 'not a valid input.'
            return -1

    def parseArgs(self, args):
        try:
            for x in range(1, len(args)-1):
                if args[x][0] == '-' and args[x+1][0] == '-':
                    self.parse(args[x], None)
                elif args[x][0] == '-':
                    self.parse(args[x], args[x+1])
        except IndexError:
            print 'The input has an improper closing. Be sure to include a KML file.'

    def export(self):
        return self.switches



if __name__ == "__main__":
    parser = Parser()
    merc = MercatorProjection()
    f = RestrictionFactory()

    parser.parseArgs(sys.argv)
    switches = parser.export()

    if switches['v']: print 'Arguments parsed correctly.'

    if switches['c'] is not None: center = LatLongPoint(float(switches['c'].split(',')[0]),float(switches['c'].split(',')[1]))
    else:
        print 'No center point.'
        if switches['m'] or switches['wa'] or switches['sr']: exit()
    if switches['z'] is not None: zoom = int(switches['z'])
    else:
        print 'No zoom value.'
        if switches['m'] or switches['wa']: exit()
    if switches['s'] is not None:
        size = int(switches['s'])
    else:
        print 'No size has been specified.'
        if switches['m'] or switches['wa']: exit()

    if switches['v']: print 'Values have been set.'

    fasade = KmlFasade(sys.argv[-1])
    fasade.placemarkToGeometrics()

    if switches['w']: fasade.removeGarbageTags()
    if switches['v']: print 'garbage data removed.'

    if switches['wa']:
        restrict = f.newWAClipping(merc.get_corners(center, zoom, size, size))
    if switches['sr']:
        restrict = f.newSquareRestriction([center.lat, center.lng], switches['sr'])
    if switches['wa'] or switches['sr']:
        restrict.restrict(fasade.geometrics)
        fasade.fasadeUpdate()
    if switches['v']: print 'Clipping completed.'

    if switches['w']: fasade.rewrite(switches['w'])
    if switches['v']: print 'KML file rewritten.'

    if switches['m']:
        build = UrlBuilder(size)
        build.centerparams(switches['c'],repr(zoom))

        markerlist = []
        for element in fasade.geometrics:
            if element.tag == "Point":
                markerlist.append(element.printCoordinates())
            if element.tag == "Polygon":
                build.addpath({"color": "blue", "weight": '5'}, element.coordinatesAsListStrings())
            if element.tag == "LineString":
                build.addpath({"color": "red", "weight": '5'}, element.coordinatesAsListStrings())
        build.addmarkers({"color": "yellow"}, '41.3079222,-74.6096236')

        if switches['v']:
            build.printUrls()
            print "Number of urls: ", len(build.urllist) + 2

        images = build.download()
        if switches['v']: print "All images downloaded."
        images = ImageMerge.convertPtoRGB(*images)
        ImageMerge.mergeModeRGB(switches['m'], *images)
        im = Image.open(switches['m'])
        im.show()