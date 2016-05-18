from lxml import etree

class LatLongPoint:
    """
    Author: Nick LaPosta

    Container for the lat/lon coordinate for a point on a Mercator map projection.
    GeoLatLng has a wrap around for the anti-meridian so that it never has a longitude > 180 or < -180

    NOTE this implementation may not work, I am changing it to suit a test -Bob 4-23-16
    """
    def __init__(self, lt, ln):
        self.lat = round(lt, 7)
        self.lng = round(ln, 7)
        self.rewrap()

    def rewrap(self):
        if self.lng < -360 and self.lng > 360:
            raise Exception("\"Invalid directional directions\" - Nick")
        elif self.lng < -180:
            self.lng = self.lng + 360
        elif self.lng > 180:
            self.lng = self.lng - 360
        else:
            self.lng = self.lng

    def getTup(self):
        return (self.lng, self.lat)

    def __str__(self):
        return repr(self.lat) + "," + repr(self.lng)

    def __repr__(self):
        return self.__str__()

    def rewriteStr(self):
        return repr(self.lng) + "," + repr(self.lat)

    def listed(self):
        return [self.lat, self.lng]

    def __cmp__(self, other):
        return (self.lat == other.lat and self.lng == other.lng)

    def __eq__(self, other):
        return (round(self.lat,7) == round(other.lat,7) and round(self.lng,7) == round(other.lng,7))

    def __getitem__(self, item):
        return self;

class GeometricObject(object):

    def __str__(self):
        """
        `Author`: Bill Clark

        Overrides the tostring method of a geometric object.

        `return`: This object as a string.
        """

        return str(self.tag)+ ' ' + self.printCoordinates() + " " + elementPrint(self.element)

    def __init__(self, element, tag, coordinates):
        """
        `Author`: Bill Clark

        Creates a geometic object, which is a wrapper for an xml element that contains geometric coordinates.
        This class makes it easier to access the values in the xml element and provides a quick method of
        replacing or removing them.

        `element`: The element that is being wrapped.

        `tag`: The tag value, otherwise the type of the element.

        `coordinates`: the coordinate values for the tag, pulled out of the xml for easy of access.
        """

        self.element = element
        self.tag = tag
        self.remove = 0
        self.debug = 0
        self.coordinates = []  # Most definitely required.
        if type(coordinates) is str:
            for x in coordinates.split():
                s = x.split(',')
                self.coordinates.append(LatLongPoint(float(s[1]), float(s[0])))
        else:
            self.coordinates = coordinates
        if self.debug: print self.coordinates

    def applyEdits(self):
        """
        `Author`: Bill Clark

        This is the super method for all applyEdit methods. This method and it's children are used to take the changes
        made to the pulled out xml values and apply them back to the file object.
        """
        if self.remove == len(self.coordinates):
            y = self.element.getparent()
            if y is not None: y.remove(self.element)
            return 0
        self.element.find('coordinates').text = '\n'.join([x.rewriteStr() for x in self.coordinates])

    # def switchCoordinates(self):
    #     """
    #     Switches the coordinates from lat long. This is used for the google maps static map api, which wants long lat
    #     as opposed to lat long as our files provide. This modifies the file in place.
    #
    #     `return`: the tostring of the coordinate swap. This a side effect, useful for script building.
    #     """
    #     for coordin in self.coordinates:
    #         coordin.lat, coordin.lng = coordin.lng, coordin.lat
    #     return self.printCoordinates()

    def printCoordinates(self):
        """
        `Author`: Bill Clark

        Makes a string out of the coordinates contained in the object. Multiple coordinates are seperated by |.

        `return`: String of the coordinates in the object.
        """
        ret = ""
        for y in self.coordinates:
            ret += str(y) + "|"
        return ret[:-1]

    def coordinatesAsListStrings(self):
        """
        `Author`: Bill Clark

        Takes the coordinates contained in this object and returns them in a list, with each coordinate being converted
        to a String. This method is used to provide to urlbuilder, as seperated points are easier to process.

        `return`: The coordinates as Strings, placed in a list.
        """
        ret = []
        for y in self.coordinates:
            ret.append(str(y))
        return ret


class Point(GeometricObject):
    """
    `Author`: Bill Clark

    See Geometric Object. This class specifies rules for a point xml object.
    """

    def __init__(self, element, tag, coordinates):
        super(Point, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        """
        `Author`: Bill Clark

        See geometric object. This calls the super applyEdits, and if the removal flag has been set for this
        point, the point will be removed from the file. This removal is done from the Placemark containing the point.
        """

        super(Point,self).applyEdits()

    def printCoordinates(self):
        """
        `Author` Bill Clark

        `return`: The string representation of the coordinate in the point.
        """
        return str(self.coordinates[0])

    def coordinatesAsListStrings(self):
        """
        `Author` Bill Clark

        `return` The coordinate that makes up the point as a list of a string. Used for url builder.
        """

        return [str(self.coordinates[0])]


class LinearRing(GeometricObject):
    """
    `Author`: Bill Clark

    See Geometric Object. This class specifies rules for a linearring xml object.
    """

    def __init__(self, element, tag, coordinates):
        super(LinearRing, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        """
        `Author`: Bill Clark

        See geometric object. This calls the super applyEdits, then removes the xml object if it is marked for
        removal. This is done from the placemark above the LinearRing.
        """

        super(LinearRing,self).applyEdits()


class LineString(GeometricObject):
    """
    `Author`: Bill Clark

    See Geometric Object. This class specifies rules for a LineString xml object.
    """

    def __init__(self, element, tag, coordinates):
        super(LineString, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        """
        `Author`: Bill Clark

        See geometric object. This calls the super applyEdits, then removes the xml object if it is marked for
        removal. This is done from the placemark above the LineString.
        """

        super(LineString,self).applyEdits()

class Polygon(GeometricObject):
    """
    `Author`: Bill Clark

    See Geometric Object. This class specifies rules for a Polygon xml object. For reference,
    It only contains the coordinates of the outer ring. Optional inner rings are ignored as a hollow iceberg
    is still an iceberg.
    """

    def __init__(self, element, tag, coordinates):
        super(Polygon, self).__init__(element, tag, coordinates)

    def applyEdits(self):
        """
        `Author`: Bill Clark

        See geometric object. This calls the super applyEdits,then removes the xml object if it is marked for
        removal. This is done from the placemark above the Polygon.
        """

        super(Polygon,self).applyEdits()


class GeometricFactory(object):

    def __init__(self):
        """
        `Author`: Bill Clark

        Simple factory object to produce geometric objects. Can be extended to do input checking and other
        such utility functions.
        """
        self.geometryTypes = ('Point', 'LineString', 'LinearRing', 'Polygon', 'MultiGeometry')
        pass

    def createLiteral(self, element, tag, coordinates):
        """
        `Author`: Bill Clark

        Generates a new Geometric object based on what the extracted tag is. This is important as certain xml objects
        require different functions to properly update changes. The literal means that this method takes the
        values directly. The create method, in comparision, takes the top level element and finds the values itself.

        `element`: The element that is being wrapped.

        `tag`: The tag value, otherwise the name of the element.

        `coordinates`: the coordinate values for the tag, pulled out of the xml for easy of access.
        """

        if tag == 'Point':
            return Point(element, tag, coordinates)
        elif tag == 'LinearRing':
            return LinearRing(element, tag, coordinates)
        elif tag == 'LineString':
            return LineString(element, tag, coordinates)
        else:
            print 'derpy'

    def create(self, element):
        """
        `Author`: Bill Clark

        Given an element, which is expected to have geometric data, create a geometric object for that data.
        Geometric objects wrapped tags such as Point, Polygon, and LinearRing, which have coordinate data.
        This method take the xml tag that starts a set of data, and processes until it has the required information
        to make a new Geometric.
        When this factory is given a multigeometry object, it does an iteration through the multigeometry element
        calling create on each sub element. Those elements are returned as a list.

        `element`: An xml tag that has coordinate data within it.

        `return`: The created Geometric Object, or a list of them.
        """


        if element.tag == "Polygon" :
            for x in element.iter():
                if x.tag in self.geometryTypes and x.tag != "Polygon":
                    for child in range(len(x)):
                        if x[child].tag == "coordinates":
                            break
                    return Polygon(x, element.tag, x[child].text)

        elif element.tag == 'MultiGeometry':
            ret = []
            skip = 0
            first = 1  # Set to 1 initally to skip the actual multigeo tag.
            for x in element.iter():
                if first:
                    first = 0
                    continue

                if skip:
                    skip += len(x)
                    skip -= 1
                elif x.tag in self.geometryTypes:
                    geo = self.create(x)
                    assert geo is not None #Checking an object actually got made.

                    if type(geo) is list: ret.extend(geo) #catches multigeometry returns.
                    else: ret.append(geo)

                    if x.tag == "Polygon" or x.tag == "MultiGeometry": skip += len(x)
                else:
                    pass

            return ret

        else:
            for child in range(len(element)):
                if element[child].tag == "coordinates":
                    break
            if element.tag == 'Point':
                return Point(element, element.tag, element[child].text)
            elif element.tag == 'LinearRing':
                return LinearRing(element, element.tag, element[child].text)
            elif element.tag == 'LineString':
                return LineString(element, element.tag, element[child].text)
            else:
                print 'derpy'

def elementPrint(element, bool=0):
    """
    `Author`: Bill Clark

    Version = 1.0
    Quick method to print an lxml element. For quicker writing.
    `element`: lxml element.

    `bool`: To pretty print or to compress to a single line.

    `return`: the tostring of the element.

    """

    if bool:
        return etree.tostring(element, pretty_print=False)
    else:
        return etree.tostring(element, pretty_print=True)