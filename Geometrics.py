import Utils

class GeometricObject(object):

    def __str__(self):
        """
        Author: Bill Clark
        Version = 1.0
        Overrides the tostring method of a geometic object.
        :return: This object as a string.
        """
        return str(self.tag)+ ' ' +str(self.coordinates)+ " " + Utils.elementPrint(self.element)

    def __init__(self, element, tag, coordinates):
        """
        Author: Bill Clark
        Version = 1.0
        Creates a geometic object, which is a wrapper for an xml element that contains geometric coordinates.
        This class makes it easier to access the values in the xml element and provides a quick method of
        replacing or removing them.
        :param element: The element that is being wrapped.
        :param tag: The tag value, otherwise the name of the element.
        :param coordinates: the coordinate values for the tag, pulled out of the xml for easy of access.
        :return:
        """
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
        """
        Author: Bill Clark
        Version = 2.0
        This is the super method for all applyEdit methods. This method and it's children are used to take the changes
        made to the pulled out xml values and apply them back to the file.
        This super method removes any geometric flagged for removal.
        ToDO: Setup for differing high removal or delegate to subclasses.
        """
        if self.remove:
            x = self.element.getparent()
            y = x.getparent()
            y.remove(x)


class Point(GeometricObject):
    def __init__(self, element, tag, coordinates):
        """
        Author: Bill Clark
        Version = 1.0
        See Geometric Object. This class specifies rules for a point xml object.
        """
        super(Point, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        """
        Author: Bill Clark
        Version = 2.0
        See geometric object. This calls the super applyEdits, as well as applies the pulled out coordinates,
        which may have been changed, back to the file.
        """
        super(Point,self).applyEdits()
        if self.remove == 1: return 0
        self.element.find('coordinates').text = ','.join([str(x)for x in self.coordinates])


class LinearRing(GeometricObject):
    """
    Author: Bill Clark
    Version = 1.0
    See Geometric Object. This class specifies rules for a linearring xml object.
    """
    def __init__(self, element, tag, coordinates):
        super(LinearRing, self).__init__(element, tag, coordinates)
        self.remove = 1

    def applyEdits(self):
        """
        Author: Bill Clark
        Version = 2.0
        See geometric object. This calls the super applyEdits, as well as applies the pulled out coordinates,
        which may have been changed, back to the file. This method also overrides the super's functionality to
        remove the object from the xml if the remove flag is set.
        """
        #super(LinearRing,self).applyEdits()
        if self.remove:
                x = self.element.getparent()
                x = x.getparent()
                y = x.getparent()
                y.remove(x)
                return 0
        self.element.find('coordinates').text = ','.join([str(x)for x in self.coordinates])


class GeometricFactory(object):

    def __init__(self):
        """
        Author: Bill Clark
        Version = 0
        Simple factory object to produce geometric objects. Can be extended to do input checking and other
        such utility functions.
        """
        pass

    def create(self, element, tag, coordinates):
        """
        Author: Bill Clark
        Version = 1.0
        Generates a new Geometric object based on what the extracted tag is. This is important as certain objects
        require different functions to properly update changes.
        :param element: The element that is being wrapped.
        :param tag: The tag value, otherwise the name of the element.
        :param coordinates: the coordinate values for the tag, pulled out of the xml for easy of access.
        :return:
        """
        if tag == 'Point':
            return Point(element, tag, coordinates)
        elif tag == 'LinearRing':
            return LinearRing(element, tag, coordinates)
        else:
            print 'derpy'
