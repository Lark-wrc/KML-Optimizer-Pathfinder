import sys
from PIL import Image
import StaticMapsConnections.ImageMerge as ImageMerge
from GeometricDataStructures.KmlFasade import KmlFasade
from GeometricDataStructures.Mercator import *
from RestrictionEngine.RestrictionEngine import RestrictionFactory
from StaticMapsConnections.UrlBuilder import UrlBuilder
from Observations.observableConsole import ObservableConsole

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
        -wa -w "Outputs/Driver Rewrite.kml" -m Outputs/Outfile.png -v -z 8 -c 40.0583,-74.4057 -s 600 "Inputs/KML Files/us_states.kml"
        """
        self.switches = {'wa':0, 'v':0}
        self.data = {'w':0, 'sr':0, 'm':0, 'c':0, 'z':0, 's':0}

    def parse(self, flag, data):
        """
        `Author`: Bill Clark

        This is the method that parses a flag with it's data. It sets the class wide switches when provided.

        `flag`: The flag being set. IE -v, -wa.

        `data`: The data associated with the flag. paths, coordinates etc.
        """
        flag = flag[1:]

        if data is None:
            self.switches[flag] = 1
        else:
            self.data[flag] = data

    def parseArgs(self, args):
        """
        `Author`: Bill Clark

        Parses the arguments passed in as a list. Usually this will be sys.argv. Calls parse on paired up args.
        Following the parsing loop are some switch checks. These cause some switches to fail if things they
        rely on aren't set. Mostly based on needing a center point.

        `args`: The list of arguments from the command line.
        """
        while args[0][0] == '-':
            if args[0][1:] in self.switches: self.parse(args.pop(0), None)
            elif args[0][1:] in self.data: self.parse(args.pop(0), args.pop(0))
            else: print 'Bad parse.'
        #Switch checks
        self.switches['wa'] = self.switches['wa'] and self.data['c'] and self.data['z'] and self.data['s']
        if not self.data['c']: self.data['sr'] = 0
        if not (self.data['m'] and self.data['c'] and self.data['z'] and self.data['s']): self.data['m'] = 0


    def export(self):
        """
        `Author`: Bill Clark

        Returns the switches set in the parse methods.

        'return': the Switches dict.
        """
        return self.switches, self.data


def interface(args=None, uiObserve=None, imObserve=None, urlObserve=None):
    """
    `Author`: Bill Clark

    This is a refined version of the driver. It parses command line args to run through the driver.
    The code only executes what it needs to, saving cycles. Selective execution is based off the switches.

    `args`: A list of command line style parameters. Pulled from argv if not defined.

    `uiObserve`: An observer for the ui and the ui's console.

    `imObserve`: An observer for the image merging.

    `urlObserve`: An observer for the url downloads.
    """
    observe = ObservableConsole()
    if uiObserve is not None:
        observe.register(uiObserve)

    parser = Parser()
    merc = MercatorProjection()
    f = RestrictionFactory()

    # parse args.
    if not args: args = sys.argv[1:]
    parser.parseArgs(args)
    switches, data = parser.export()

    if switches['v']: observe.setStatus('Arguments parsed correctly.\n', 'CONSOLE')

    # processes the data values in the switches, c, z, and s.
    if data['c']: center = LatLongPoint(float(data['c'].split(',')[0]),float(data['c'].split(',')[1]))
    else:
        observe.setStatus('No center point. Cancelled restrictions and static maps.\n', 'ERROR')
    if data['z']: zoom = int(data['z'])
    else:
        observe.setStatus('No zoom value. Cancelled wa restriction and static maps.\n', 'ERROR')
    if data['s']: size = int(data['s'])
    else:
        observe.setStatus('No size has been specified. Cancelled wa restriction and static maps.\n', 'ERROR')

    if switches['v']: observe.setStatus('Values have been set.\n', 'CONSOLE')

    # open the kml fasade.
    fasade = KmlFasade(args[-1])
    fasade.placemarkToGeometrics()

    if data['w']: fasade.removeGarbageTags()
    if switches['v']: observe.setStatus('Garbage data removed.\n', 'CONSOLE')

    # clip if requested in the args.
    if switches['wa']:
        restrict = f.newWAClipping(merc.get_corners(center, zoom, size, size))
    if data['sr']:
        restrict = f.newSquareRestriction([center.lat, center.lng], data['sr'])
    if switches['wa'] or data['sr']:
        for geometrics in fasade.yieldGeometrics():
            restrict.restrict(geometrics)
        fasade.fasadeUpdate()
    if switches['v']: observe.setStatus('Clipping completed.\n', 'CONSOLE')

    # rewrite if requested.
    if data['w']: fasade.rewrite(data['w'])
    if switches['v']: observe.setStatus('KML file rewritten.\n', 'CONSOLE')

    # Creates urls out of the geometrics, downloads and merges them.
    if data['m']:
        build = UrlBuilder(size)
        if urlObserve is not None: build.register(urlObserve)
        build.centerparams(data['c'], repr(zoom))

        for geometrics in fasade.yieldGeometrics():
            build.addGeometrics(geometrics)

        #Mark the center point.
        build.addmarkers({"color": "yellow"}, repr(center))

        # allows logging to ui's console for accessible urls
        if switches['v']:
            observe.setStatus(build.printUrls(), 'URLS')

        images = build.download()
        if switches['v']: observe.setStatus("All images downloaded.\n", 'CONSOLE')
        merger = ImageMerge.Merger(data['m'], images[0])
        if imObserve is not None: merger.register(imObserve)
        images = merger.convertAll(*images)
        merger.mergeAll(data['m'], *images)
        im = Image.open(data['m'])
        if __name__ == "__main__": im.show()

if __name__ == "__main__":
    interface()
