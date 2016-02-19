import Utils

class GeometricObject(object):

    def __str__(self):
        """
        Author: Bill Clark
        Version = 1.0
        Overrides the tostring method of a geometic object.
        :return: This object as a string.
        """

        return str(self.tag)+ ' ' +self.printCoordinates()+ " " + Utils.elementPrint(self.element)

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
        """

        self.element = element
        self.tag = tag
        self.remove = 0
        self.coordinates = []
        for x in coordinates.split('\n'):
            s = x.split(',')
            self.coordinates.append([float(s[0]), float(s[1])])
        #print self.coordinates

    def applyEdits(self):
        """
        Author: Bill Clark
        Version = 2.0
        This is the super method for all applyEdit methods. This method and it's children are used to take the changes
        made to the pulled out xml values and apply them back to the file.
        """
        self.element.find('coordinates').text = '\n'.join([','.join([str(y) for y in x]) for x in self.coordinates])

    def switchCoordinates(self):
        """
        Switches the coordinates in each string. This is used for the google maps static map api, which wants lat long
        as opposed to long lat as our files provide.
        :return: the tostring of the coordinate swap. This a side effect, useful for script building.
        """
        for coordin in self.coordinates:
            coordin[0], coordin[1] = coordin[1], coordin[0]
        return self.printCoordinates()

    def printCoordinates(self):
        """
        Author: Bill Clark
        Makes a string out of the coordinates contained in the object. Multiple coordinates are seperated by |.
        :return: String of the coordinates in the object.
        """
        if self.tag == "Point":
            return ','.join([str(x) for x in self.coordinates[0]])
        ret = ""
        for y in self.coordinates:
            ret += ','.join([str(x)for x in y]) + "|"
        return ret[:-1]

    def coordinateStringList(self):
        """
        Author: Bill Clark
        Takes the list of coordinates that is stored and converts the coordinates stored as int and makes them strings.
        This is useful for the url builder, which functions off lists of coordinates.
        :return: List of coordinates as strings.
        """
        ret = []
        for y in self.coordinates:
            ret.append(','.join([str(x)for x in y]))
        return ret


class Point(GeometricObject):
    """
    Author: Bill Clark
    Version = 1.0
    See Geometric Object. This class specifies rules for a point xml object.
    """

    def __init__(self, element, tag, coordinates):
        super(Point, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        """
        Author: Bill Clark
        Version = 2.0
        See geometric object. This calls the super applyEdits, as well as applies the pulled out coordinates,
        which may have been changed, back to the file.
        """

        if self.remove:
            x = self.element.getparent()
            y = x.getparent()
            y.remove(x)
        super(Point,self).applyEdits()


class LinearRing(GeometricObject):
    """
    Author: Bill Clark
    Version = 1.0
    See Geometric Object. This class specifies rules for a linearring xml object.
    """

    def __init__(self, element, tag, coordinates):
        super(LinearRing, self).__init__(element, tag, coordinates)
        for child in self.element.getparent():
            print child.tag

    def applyEdits(self):
        """
        Author: Bill Clark
        Version = 2.0
        See geometric object. This calls the super applyEdits, as well as applies the pulled out coordinates,
        which may have been changed, back to the file. This method also overrides the super's functionality to
        remove the object from the xml if the remove flag is set.
        """

        if self.remove:
                x = self.element.getparent().getparent().getparent()
                y = x.getparent()
                y.remove(x)
                return 0
        super(LinearRing,self).applyEdits()


class LineString(GeometricObject):
    """
    Author: Bill Clark
    Version = 1.0
    See Geometric Object. This class specifies rules for a LineString xml object.
    """

    def __init__(self, element, tag, coordinates):
        super(LineString, self).__init__(element, tag, coordinates)
        for child in self.element.getparent():
            print child.tag

    def applyEdits(self):
        """
        Author: Bill Clark
        Version = 2.0
        See geometric object. This calls the super applyEdits, as well as applies the pulled out coordinates,
        which may have been changed, back to the file. This method also overrides the super's functionality to
        remove the object from the xml if the remove flag is set.
        """

        if self.remove:
                x = self.element.getparent()
                y = x.getparent()
                y.remove(x)
                return 0
        super(LineString,self).applyEdits()


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
        elif tag == 'LineString':
            return LineString(element, tag, coordinates)
        else:
            print 'derpy'
