from lxml import etree
#import lxml.etree.ElementTree as ET
from RestrictionEngine import LocationRadialRestriction
from Geometrics import *
import Utils

debug = 0

class KmlFasade(object):

    def __init__(self, path):
        self.filepath = path
        self.placemarks = None
        self.geometrics = None
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
        self.placemarks = ret
        return ret

    def placemarkToGeometrics(self):
        if(self.placemarks is None):
            self.loadPlacemarks()
        factory = GeometricFactory()
        ret = []
        for element in self.placemarks:
            for x in element.iter():
                if x.tag in Utils.geometryTypes:
                    z = factory.create(x, x.tag, x[0].text)
                    if z is not None: ret.append(z)
        self.geometrics = ret
        return ret

    def fasadeUpdate(self):
        for element in self.geometrics:
            #element.coordinates = [0,1]
            element.applyEdits()

if __name__ == '__main__':
    fasade = KmlFasade('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1.kml')
    fasade.loadPlacemarks()
    z = LocationRadialRestriction([-99,40], 75)
    fasade.placemarkToGeometrics()
    z.restrict(fasade.geometrics)
    fasade.fasadeUpdate()
    fasade.rewrite('C:\Users\Research\Documents\Code Repositories\javaapiforkml-master\\advancedexample1copy.kml')
