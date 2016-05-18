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
        """
        `Author`: Bill Clark

        This class parses command line switches. A variety are supported, and can be parsed
        as flags with their data, or as the argv array provided by the sys module.
        Switches: wa - use weiler atherton clipping.
                  w - rewrite changes back to the file.
                  sr - use a square restriction.
                  m - use the static maps connections, to generate urls and merge the images.
                  c - set the center point for the viewport and restrictions.
                  z - set the zoom value for google static.
                  s - set the size for google static.
                  v - verbose output to the console.
        Example arg list.
        -wa -w "Outputs/Driver Rewrite.kml" -m Outputs/Outfile.png -v -z 8 -c
            40.0583,-74.4057 -s 600 "Inputs/KML Files/us_states.kml"
        """
        self.switches = {'wa':0, 'w':0, 'sr':0, 'm':0, 'c':None, 'z':None, 's':None, 'v':0}

    def parse(self, flag, data):
        """
        `Author`: Bill Clark

        This is the method that parses a flag with it's data. It sets the class wide switches when provided.

        `flag`: The flag being set. IE -v, -wa.

        `data`: The data associated with the flag. paths, coordinates etc.
        """
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
        """
        `Author`: Bill Clark

        Parses the arguments passed in as a list. Usually this will be sys.argv. Calls parse on paired up args.
        TODO is that if wa or v are at the end of the parameters, the kml input ends up as it's value.
        TODO optional data arguments. I'll admit, not my smoothest code, but I didn't want a massive if chain.

        `args`: The list of arguments from the command line.
        """
        try:
            for x in range(1, len(args)-1):
                if args[x][0] == '-' and args[x+1][0] == '-':
                    self.parse(args[x], None)
                elif args[x][0] == '-':
                    self.parse(args[x], args[x+1])
        except IndexError:
            print 'The input has an improper closing. Be sure to include a KML file.'

    def export(self):
        """
        `Author`: Bill Clark

        Returns the switches set in the parse methods.

        'return': the Switches dict.
        """
        return self.switches


def interface():
    """
    `Author`: Bill Clark

    This is a refined version of the driver. It parses command line args to run through the driver.
    The code only executes what it needs to, saving cycles. Selective execution is based off the switches.
    """
    parser = Parser()
    merc = MercatorProjection()
    f = RestrictionFactory()

    # parse args.
    parser.parseArgs(sys.argv)
    switches = parser.export()

    if switches['v']: print 'Arguments parsed correctly.'

    # processes the data values in the switches, c, z, and s.
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

    # open the kml fasade.
    fasade = KmlFasade(sys.argv[-1])
    fasade.placemarkToGeometrics()

    if switches['w']: fasade.removeGarbageTags()
    if switches['v']: print 'garbage data removed.'

    # clip if requested in the args.
    if switches['wa']:
        restrict = f.newWAClipping(merc.get_corners(center, zoom, size, size))
    if switches['sr']:
        restrict = f.newSquareRestriction([center.lat, center.lng], switches['sr'])
    if switches['wa'] or switches['sr']:
        restrict.restrict(fasade.geometrics)
        fasade.fasadeUpdate()
    if switches['v']: print 'Clipping completed.'

    # rewrite if requested.
    if switches['w']: fasade.rewrite(switches['w'])
    if switches['v']: print 'KML file rewritten.'

    # Creates urls out of the geometrics, downloads and merges them.
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

if __name__ == "__main__":
    interface()
