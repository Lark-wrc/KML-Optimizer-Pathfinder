import Utils

class GeometricObject(object):

    def __str__(self):
        return str(self.tag)+ ' ' +str(self.coordinates)+ " " + Utils.elementPrint(self.element)

    def __init__(self, element, tag, coordinates):
        self.element = element
        self.tag = tag
        self.remove = 0
        self.coordinates = []
        for x in coordinates.split('\n'):
            s = x.split(',')
            self.coordinates.append(float(s[0]))
            self.coordinates.append(float(s[1]))
        #print self.coordinates

    def applyEdits(self):
            if self.remove:
                x = self.element.getparent()
                y = x.getparent()
                y.remove(x)


class Point(GeometricObject):
    def __init__(self, element, tag, coordinates):
        super(Point, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        super(Point,self).applyEdits()
        if self.remove == 1: return 0
        self.element.find('coordinates').text = ','.join([str(x)for x in self.coordinates])


class LinearRing(GeometricObject):
    def __init__(self, element, tag, coordinates):
        super(LinearRing, self).__init__(element, tag, coordinates)
        self.remove = 1

    def applyEdits(self):
        super(LinearRing,self).applyEdits()
        if self.remove:
                x = self.element.getparent()
                x = x.getparent()
                y = x.getparent()
                y.remove(x)
                return 0
        self.element.find('coordinates').text = ','.join([str(x)for x in self.coordinates])


class GeometricFactory(object):

    def __init__(self):
        pass

    def create(self, element, tag, coordinates):
        if tag == 'Point':
            return Point(element, tag, coordinates)
        elif tag == 'LinearRing':
            return LinearRing(element, tag, coordinates)
        else:
            print 'derpy'
