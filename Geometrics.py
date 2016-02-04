import Utils

class GeometricObject(object):

    def __str__(self):
        return str(self.tag)+ ' ' +str(self.coordinates)+ " " + Utils.elementPrint(self.element)

    def __init__(self, element, tag, coordinates):
        self.element = element
        self.tag = tag
        self.coordinates = []
        for x in coordinates.split('\n'):
            self.coordinates.append((x.split(',')[0], x.split(',')[1]))
        print coordinates

    def applyEdits(self):
            print self.__str__()


class Point(GeometricObject):
    def __init__(self, element, tag, coordinates):
        super(Point, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        self.element.find('coordinates').text = str(self.coordinates)

class LinearRing(GeometricObject):
    def __init__(self, element, tag, coordinates):
        super(LinearRing, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        self.element.find('coordinates').text = str(self.coordinates)

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
