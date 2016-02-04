from lxml import etree
#import lxml.etree.ElementTree as ET
from RestrictionEngine import LocationRadialRestriction
from Geometrics import *
import Utils

debug = 0

class KmlFasade(object):

    def __init__(self, path):
        self.filepath = path
        self.kmlTree = etree.parse(path)
        self.kmlRoot = self.kmlTree.getroot()

    def rewrite(self, path=None):
        if path == None:
            f = open(self.filepath, 'w')
            f.write(Utils.elementPrint(self.kmlRoot))
            f.close()
        else:
            f = open(path, 'w')
            f.write(Utils.elementPrint(self.kmlRoot))
            f.close()

    #Returns a list of elements that contain geometric coordinates (Placemarks)
    def loadPlacemarks(self):
        ret = []
        for x in self.kmlRoot.iter():
            if x.tag == 'Placemark':
                if debug: print x.tag, x.text
                ret.append(x)
        return ret

    def placemarkToGeometrics(self, list):
        factory = GeometricFactory()
        ret = []
        for element in list:
            for x in element.iter():
                if x.tag in Utils.geometryTypes:
                    z = factory.create(x, x.tag, x[0].text)
                    if z is not None: ret.append(z)
        return ret

if __name__ == '__main__':
    fasade = KmlFasade('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1.kml')
    y = fasade.loadPlacemarks()
    z = LocationRadialRestriction(1, 2)
    geos = fasade.placemarkToGeometrics(y)
    for element in geos:
        element.coordinates = 0
        element.applyEdits()
    fasade.rewrite('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1copy.kml')
