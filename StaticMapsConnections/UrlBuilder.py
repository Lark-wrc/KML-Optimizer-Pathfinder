from urllib import urlretrieve
from time import sleep
from Observations.Observer import Observable


class UrlBuilder(Observable):

    def __init__(self, height, width=0):
        """
        `Author`: Bill Clark

        The UrlBuilder Class should be created anew for each url the user wants to build.
        Using the methods contained, the user may create a valid google maps static api url.
        Input is not checked, and ALL INPUTS SHOULD BE STRINGS. Even integer values should be entered repr()'d.
        All inputs will be need to be converted to Long Lat, as all other files use Lat Long.

        `size`: the size of the returned image in pixels. [0-640]x[0-640]
        """

        super(UrlBuilder, self).__init__()
        self.dcount = 1
        self.setStatus('Initialized.')
        self.urlbase = 'https://maps.googleapis.com/maps/api/staticmap?'
        self.urlbase += 'size='+repr(height) + "x" + repr(height) if width == 0 else repr(width)
        self.url = self.urlbase
        self.urllist = []
        self.limit = 2000 #Proper limit is 2048, buffer of 48. Url can only be that many characters.
        self.debug = 0

    def addparam(self, feature, value):
        """
        `Author`: Bill Clark

        Appends the given parameter to the static maps url. This applies to all urls in a split scenerio.

        `feature: The name of the parameter. Valid`: scale | maptype | format

        `value: the value of the parameter. Valid`: 1,2,4 | roadmap, satellite, hybrid, terrain |
                                                                png, jpg, png32, gif, jpg-baseline
        `return`: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = ""
        curr += '&&' + feature + '='
        curr += value

        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def addparams(self, dict):
        """
        `Author`: Bill Clark

        Allows for a list of parameters to be added to the static map. This is applied to all urls in a split scenario.

        `dict: a dictionary of features`:values from the addparam method.

        `return`: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = ""
        for key in dict:
            curr += '&&' + key + '=' + dict[key]

        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def centerparams(self, center, zoom):
        """
        `Author`: Bill Clark

        This method adds two parameters to the url that are required for a consistent image. In order to merge
        images, these parameters are required to keep the image displaying the same area. In a split scenario,
        these are applied to each url. Multiple calls are unnecessary.

        `center`: The center point the map will display. latitude and longitude coordinates.

        `zoom`: How far zoomed in the map slice will be. [1-20]

        `return`: the url with the given parameter appended to it. Also updates saved url.
        """

        if len(self.urlbase) > 59:
            return 0
        curr = ""
        curr += '&&center='+center
        curr += '&&zoom='+zoom
        curr += '&&key=AIzaSyAdYQpSjMl5wE2GNIknG63nZpOcadeNhDc'
        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def viewportparam(self, viewports):
        """
        `Author`: Bill Clark

        Appends a viewport parameter. A viewport makes each point it is given visible on the map. If the parameters
        are provided as a list, when a coordinate is added and the length is pushed over the character limit,
        the url will be split. If the locations are provided as a solid string, the url will only be checked after
        everything is appended. (This could cause data loss.)

        `viewports`: Locations in a list format. Each will be made visible.

        `return`: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&visible='
        if type(viewports) is list:
            for coordin in viewports:
                curr += coordin
                if self.retireUrl(curr):
                    curr = self.url + '&&visible='
                    curr += coordin + '|'
                else:
                    curr += '|'
            curr = curr[:-1]
        elif type(viewports) is str:
            curr += (viewports)

        self.url = curr
        self.retireUrl(self.url)
        return self.url

    def addmarkers(self, styles, locations):
        """
        `Author`: Bill Clark

        Adds the locations listed as markers to the url. Each point will have the supplied style settings. If the
        parameters are provided as a list, when a coordinate is added and the length is pushed over the character limit,
        the url will be split. If the locations are provided as a solid string, the url will only be checked after
        everything is appended. (This could cause data loss.)

        `styles`: Style settings, which function like parameters, a dict of name and value.
                        Valid Names: size | label | color
                        Valid value: tiny, mid, small, normal | [A-Z] or [0-9] | [hexvalue] or color name
        `locations`: Locations in a list format. Each will be added to be marked. list of  coordinates.

        `return`: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&markers='

        for key in styles:
            curr += key + ':' + styles[key] + '|'

        if type(locations) is list:
            for coordin in locations:
                curr += coordin
                if self.retireUrl(curr):
                    curr = self.url + '&&markers='
                    for key in styles:
                        curr += key + ':' + styles[key] + '|'
                    curr += coordin + '|'
                else:
                    curr += '|'
            curr = curr[:-1]
        elif type(locations) is str:
            curr += (locations)

        self.url = curr
        self.retireUrl(self.url)
        return curr

    def addpath(self, styles, locations):
        """
        `Author`: Bill Clark

        Adds the path listed to the url. The lines drawn and area filled will have the style setting specified.
        If the url is split, filling with not work, and can possibly break the url. Filled areas are expected to
        with in a single url by google maps static.
        If the parameters are provided as a list, when a coordinate is added and the length is pushed over the
        character limit, the url will be split. If the locations are provided as a solid string, the url will only be
        checked after everything is appended. (This could cause data loss.)

        `styles`: Style settings, which function like parameters, a dict of name and value.
                        Valid Names: weight | geodesic | color | fillcolor
                        Valid value: [0-.] | T or F | [hexvalue] or [hexvalue32] or color name | same as color
        `locations`: Locations in a list format. Each will be added to be marked. list of coordinates.

        `return`: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&path='

        for key in styles:
            curr += key + ':' + styles[key] + '|'

        if type(locations) is list:
            for coordin in locations:
                curr += coordin
                if self.retireUrl(curr):
                    curr = self.url + "&&path="
                    for key in styles:
                        curr += key + ':' + styles[key] + '|'
                    curr += coordin + '|'
                else:
                    curr += "|"
            curr = curr[:-1]
        elif type(locations) is str:
            curr += (locations)

        self.url = curr
        self.retireUrl(self.url)
        return curr

    def addGeometrics(self, geometrics):
        """
        `Author`: Bill Clark

        Exported from the original driver. This code takes a list of geometrics and adds their data to the urls.
        Points are  NOT included, the line is commented out. Linestrings are drawn in red, Polygons in blue, and
        if markers are uncommented they will be yellow.

        `geometrics`: A list of geometrics from a KmlFasade.
        """
        markerlist = []
        for element in geometrics:
            if element.tag == "Point":
                markerlist.append(element.printCoordinates())
            if element.tag == "Polygon":
                self.addpath({"color": "blue", "weight": '5'}, element.coordinatesAsListStrings())
            if element.tag == "LineString":
                self.addpath({"color": "red", "weight": '5'}, element.coordinatesAsListStrings())
        #self.addmarkers({"color": "yellow"}, markerlist)

    def download(self, path="""Inputs\Static Maps\Mass\{} {}.png""", prefix='image'):
        """
        `Author`: Bill Clark

        Takes a parameter path and downloads the generated url to that path. Using the symbol {} {} twice will replace
        the first with the given prefix, and the second with a counter. This is the recommended way of using this path,
        because mulitple urls may be downloaded.

        `path`: a file path to save the generated image to.

        `prefix`: The prefix to the count in the file name. Defaults to image.

        `return`: A list of the file locations for the downloaded files.
        """

        ret = []
        count = 1
        ret.append(urlretrieve(self.urlbase, path.format(prefix, '0'))[0])
        for url in self.urllist:
            ret.append(urlretrieve(url, path.format(prefix, repr(count)))[0])
            count += 1
            self.setStatus('Downloaded {} of {} Images.'.format(count, len(self.urllist)+2))
            sleep(.3)
        ret.append(urlretrieve(self.url, path.format(prefix, repr(count)))[0])
        self.dcount = count+1
        self.setStatus('Downloaded {} Images Successfully.'.format(self.dcount+1))
        return ret

    def downloadBase(self, path='Inputs\Static Maps\\Mass\{} 0.png', prefix='image'):
        """
        `Author`: Bill Clark

        Downloads only the base url. The generator method does not download that url (better for automation), so this
        method was a required addition.

        `path`: a file path to save the generated image to.

        `prefix`: The prefix to the count in the file name. Defaults to image.

        'return' the base url's saved location.
        """

        return urlretrieve(self.urlbase, path.format(prefix, '0'))[0]

    def countUrl(self, url):
        """
        `Author`: Bill Clark

        This method counts the characters in the given url. Of note, This does not use internal values, unlike most
        methods in the class. This method is necessary because | characters count as 3 when actually read by static
        maps.

        `url`: The url to be counted.

        `return`: returns the number of characters in the url.
        """

        ret = 0
        for character in url:
            if character == "|": ret += 3
            else: ret += 1
        return ret

    def retireUrl(self, url, offset=0):
        """
        `Author`: Bill Clark

        This method is used to split urls that have hit the size limit. It uses side effects to great effect.
        This method actually checks the url (and an optional offset) against the limit, and if the number is greater
        than or equal to the limit, returns true. When it does return true, it adds the current url to the url list
        and provides a new url copied from the urlbase saved in the object. This is how all parameters are kept the
        same across splits, parameters update the base url and not the actual current url. (technically they do update
        both, but you get the idea.) The method returns false if the url is shorter than the limit.

        `url`: The url to check the length of.
        """
        count = self.countUrl(url)+offset
        if count >= self.limit:
            self.urllist.append(url)
            self.url = self.urlbase[:]
            return 1
        else:
            return 0

    def printUrls(self, prin=0):
        """
        `Author`: Bill Clark

        This method prints all the urls contained in the object in a readable manner. As readable as lines of character
        length 2000~ can be. It labels the base url (used for image merging) and then lists all layer images.
        The print is actually optional now, because we now have proper handlers that can print the string in better
        places. Now the generated string is returned by default.

        `return`: the list of urls for logging in UI
        """
        ret = ""
        ret += "Base Url: " + self.urlbase + '\n'
        for url in self.urllist:
            ret += url + '\n'
        ret += self.url + '\n'
        if prin: print ret
        return ret

    def __str__(self):
        """
        `Author`: Bill Clark

        Simple override so that printing the object prints the url's it has with in it.

        `return`: ToString of the url's contained in the object.
        """
        return self.printUrls()
