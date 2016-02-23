from lxml import etree
from RestrictionEngine import SquareRestriction
from Geometrics import *
from pykml.factory import KML_ElementMaker as KML
import Utils

debug = 0

class KmlFasade(object):

    def __init__(self, path):
        """
        Author: Bill Clark
        Version = 1.0
        This object wraps an lxml object and makes it easy to worth with. This is designed for quick, useful
        functionality that ignores irrelevant carry over data. It provides function to return list of useful
        xml data, tools to apply changes to the xml file based on the objects it generates, and other features.
        :param path: Path of the source file.
        """

        self.filepath = path
        self.placemarks = None
        self.geometrics = None
        self.additionfolder = None
        self.kmlTree = etree.parse(path)
        self.kmlRoot = self.kmlTree.getroot()


    def rewrite(self, path=None):
        """
        Author: Bill Clark
        Version = 1.0
        Writes the stored file back to the orginal file or a provided path. Basically combines a few lxml methods
        to make this task quicker.
        :param path: The path to write to, otherwise it will use the original write path.
        """

        if path == None:
            f = open(self.filepath, 'w')
            f.write(Utils.elementPrint(self.kmlRoot))
            f.close()
        else:
            f = open(path, 'w')
            #f.write(Utils.elementPrint(self.kmlRoot))
            self.kmlTree.write(f, pretty_print=True)
            f.close()

    #Returns a list of elements that contain geometric coordinates (Placemarks)
    def loadPlacemarks(self):
        """
        Author: Bill Clark
        Version = 2.0
        This method is used to append any xml tag with the placemark tag to a list and return it.
        As the most relevant data in a kml file appears in a placemark tag, this is a convience method
        to prevent excess searching.
        :return: A list of lxml Element objects matching the placemark tag. This is also stored in class
        """

        ret = []
        for x in self.kmlRoot.iter():
            if x.tag == 'Placemark':
                if debug: print x.tag, x.text
                ret.append(x)
        self.placemarks = ret
        return ret

    def placemarkToGeometrics(self):
        """
        Author: Bill Clark
        Version = 2.0
        This method take the list of placemarks it has generated (or generates them) and creates geometric
        objects to allow for easy of editing.
        :return: List of geometric objects for each placemark in this object's placemark list. This is stored in class
                  as well.
        """

        if(self.placemarks is None):
            self.loadPlacemarks()

        factory = GeometricFactory()
        ret = []
        skip = 0
        for element in self.placemarks:
            for x in element.iter():
                if x.tag == "Placemark": skip = 0
                if x.tag in factory.geometryTypes and not skip:
                    z = factory.create(x)
                    if z is not None:
                        ret.append(z)
                        if z.tag == "Polygon": skip = 1

        self.geometrics = ret
        return ret

    def fasadeUpdate(self):
        """
        Author: Bill Clark
        Version = 1.0
        Runs the applyedit function on every geometric object contained in this objects geometric's list.
        If the addition folder has been generated, This method will also add that folder to the file.
        """

        for element in self.geometrics:
            #element.coordinates = [0,1]
            element.applyEdits()
        self.geometrics = [e for e in self.geometrics if not e.remove]

        if self.additionfolder is not None:
            for x in self.kmlRoot.iter():
                if x.tag == "Document":
                    x.append(self.additionfolder)
                    break

    def createAdditionsFolder(self):
        """
        Initializes thr folder any additional points will be written to.
        :return: Nothing.
        """
        fld = KML.Folder(KML.name("Additions"))
        self.additionfolder = fld

    def createAdditionalGeometry(self, type, name='blank', coordin='0,0'):
        if type == "Point":
            pm1 = KML.Placemark(KML.name(name),KML.Point(KML.coordinates(coordin)))

        elif type == "LineString":
            pm1 = KML.Placemark(KML.name(name),KML.LineString(KML.coordinates(coordin)))

        elif type == "LinearRing":
            pm1 = KML.Placemark(KML.name(name),KML.LinearRing(KML.coordinates(coordin)))
        else:
            print 'Derp.'

        self.additionfolder.append(pm1)


if __name__ == '__main__':
    fasade = KmlFasade('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1.kml')
    fasade.loadPlacemarks()
    z = CenterDistanceRestriction([-99.000000,40.000000], 75)
    fasade.placemarkToGeometrics()
    z.restrict(fasade.geometrics)
    fasade.createAdditionsFolder()
    fasade.createAdditionalGeometry("LinearRing", coordin="-100.000000,40.00000 -90.000000,30.00000 -100.000000,30.00000 -100.000000,40.00000")
    fasade.fasadeUpdate()
    fasade.rewrite('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1copy.kml')

