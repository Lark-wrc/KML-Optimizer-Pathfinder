from urllib import urlretrieve
from time import sleep
from random import uniform
from Mercator import GeoLatLng


class UrlBuilder(object):

    def __init__(self, height, width=0):
        """
        Author: Bill Clark, Nick LaPosta
        The UrlBuilder Class should be recreated for each url the user wants to build.
        Using the methods contained, the user may create a valid google maps static api url.
        Input is not checked, and ALL INPUTS SHOULD BE NUMERIC.
        :param height: the vertical size of the returned image in pixels. [0-640]
        :param width: default to zero if a square image is desired. Otherwise, the horizontal size of the returned image in pixels. [0-640]
        """

        self.url = 'https://maps.googleapis.com/maps/api/staticmap?'
        self.url += 'size='+repr(height) + "x" + repr(height) if width == 0 else repr(width)
        self.url = self.urlbase
        self.urllist = []
        self.limit = 2000 #Proper limit is 2048, buffer of 48. Url can only be that many characters.
        self.debug = 0

    def addparam(self, feature, value):
        """
        Author: Bill Clark
        Appends the given parameter to the static maps url. This applies to all urls in a split scenerio.
        :param feature: The name of the parameter. Valid: scale | maptype | format
        :param value: the value of the parameter. Valid: 1,2,4 | roadmap, satellite, hybrid, terrain |
                                                                png, jpg, png32, gif, jpg-baseline
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = ""
        curr += '&&' + feature + '='
        curr += value

        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def addparams(self, dict):
        """
        Author: Bill Clark
        Allows for a list of parameters to be added to the static map. This is applied to all urls in a split scenerio.
        :param dict: a dictionary of features:values from the addparam method.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = ""
        for key in dict:
            curr += '&&' + key + '=' + dict[key]

        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def centerparams(self, center_point, zoom):
        """
        Author: Bill Clark, Nick LaPosta
        This is a shortcut method that adds the two values a url must contain to be valid, given the url
        has no viewpoint, marker, or path. It adds center and zoom.
        :param center: The center point the map will display. GeoLatLng object
        :param zoom: How far zoomed in the map slice will be. [1-20]
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        if len(self.urlbase) > 59:
            return 0
        curr = ""
        curr += '&&center='+repr(center_point)
        curr += '&&zoom='+repr(zoom)
        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def viewportparam(self, viewports):
        """
        Author: Bill Clark, Nick LaPosta
        Appends a viewport parameter. A viewport makes each point it is given visible on the map.
        :param viewports: Locations in a list format. Each will be made visible. list of GeoLatLng objects
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&visible='

        for coordinate in viewports:
            curr += coordinate
            if self.retireUrl(curr):
                curr = self.url + '&&visible='
                curr += coordinate + '|'
            else:
                curr += '|'
        curr = curr[:-1]

        self.url = curr
        self.retireUrl(self.url)
        return self.url

    def addmarkers(self, styles, locations):
        """
        Author: Bill Clark, Nick LaPosta
        Adds the marker list to the url. Each point will have the supplied style settings.
        :param styles: Style settings, which function like parameters, a dict of name and value.
                        Valid Names: size | label | color
                        Valid value: tiny, mid, small, normal | [A-Z] or [0-9] | [hexvalue] or color name
        :param locations: Locations in a list format. Each will be added to be marked. list of GeoLatLng objects.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&markers='

        for key in styles:
            curr += key + ':' + styles[key] + '|'

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

        self.url = curr
        self.retireUrl(self.url)
        return curr

    def addpath(self, styles, locations):
        """
        Author: Bill Clark, Nick LaPosta
        Adds the path list to the url. The lines drawn and area filled will have the style setting specified.
        :param styles: Style settings, which function like parameters, a dict of name and value.
                        Valid Names: weight | geodesic | color | fillcolor
                        Valid value: [0-.] | T or F | [hexvalue] or [hexvalue32] or color name | same as color
        :param locations: Locations in a list format. Each will be added to be marked. list of GeoLatLng objects.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&path='

        for key in styles:
            curr += key + ':' + styles[key] + '|'

        for coordinate in locations:
            curr += coordinate
            if self.retireUrl(curr):
                curr = self.url + "&&path="
                for key in styles:
                    curr += key + ':' + styles[key] + '|'
                curr += coordinate + '|'
            else:
                curr += "|"
        curr = curr[:-1]

        self.url = curr
        self.retireUrl(self.url)
        return curr

    def download(self, path='C:\Users\Research\Documents\Code Repositories\KML-Optimizer-Pathfinder\Inputs\Static Maps\\Mass\{} {}.png', prefix='image'):
        """
        Author: Bill Clark
        Takes a parameter path and downloads the generated url to that path. Using the symbol {} {} twice will replace
        the first with the given prefix, and the second with a counter. This is the recommended way of using this path,
        because mulitple urls may be downloaded.
        :param path: a file path to save the generated image to.
        :param prefix: The prefix to the count in the file name. Defaults to image.
        :return: A list of the file locations for the downloaded files.
        """

        ret = []
        count = 1
        ret.append(urlretrieve(self.urlbase, path.format(prefix, '0'))[0])
        for url in self.urllist:
            ret.append(urlretrieve(url, path.format(prefix, repr(count)))[0])
            count+=1
            sleep(.5)
        ret.append(urlretrieve(self.url, path.format(prefix, repr(count)))[0])
        return ret

    def downloadGenerator(self, path='Inputs\Static Maps\\Mass\{} {}.png', prefix='image'):
        """
        Author: Bill Clark
        Takes a parameter path and downloads the generated url to that path. Using the symbol {} {} twice will replace
        the first with the given prefix, and the second with a counter. This is the recommended way of using this path,
        because mulitple urls may be downloaded. This is a python generator, it can be treated as an iterable
        object and it will yield a url in every iteration, until no more exist. The generator does not return the
        base url, as the base url is needed in every iteration.
        :param path: a file path to save the generated image to.
        :param prefix: The prefix to the count in the file name. Defaults to image.
        :return: A list of the file locations for the downloaded files.
        """

        count = 1
        #yield urlretrieve(self.urlbase, path.format(prefix, '0'))[0]
        for url in self.urllist:
            yield urlretrieve(url, path.format(prefix, repr(count)))[0]
            count+=1
            sleep(.5)
        yield urlretrieve(self.url, path.format(prefix, repr(count)))[0]

    def downloadBase(self, path='Inputs\Static Maps\\Mass\{} 0.png', prefix='image'):
        return urlretrieve(self.urlbase, path.format(prefix, '0'))[0]


    def countUrl(self, url):
        """
        Author: Bill Clark
        This method counts the characters in the given url. Of note, This does not use internal values, unlike most
         methods in the class. This method is necessary because | characters count as 3 when actually read by static
         maps.
        :param url: The url to be counted.
        :return: returns the number of characters in the url.
        """
        ret = 0
        for character in url:
            if character == "|": ret += 3
            else: ret += 1
        return ret

    def retireUrl(self, url, offset=0):
        """
        Author: Bill Clark
        This method is used to split urls that have hit the size limit. It uses side effects to great effect.
        This method actually checks the url (and an optional offset) against the limit, and if the number is greater
        than or equal to the limit, returns true. When it does return true, it adds the current url to the url list
        and provides a new url copied from the urlbase saved in the object. This is how all parameters are kept the
        same across splits, parameters update the base url and not the actual current url. (technically they do update
        both, but you get the idea.) The method returns false if the url is shorter than the limit.
        :param url: The url to check the length of.
        :return:
        """
        count = self.countUrl(url)+offset
        if count >= self.limit:
            self.urllist.append(url)
            self.url = self.urlbase[:]
            return 1
        else:
            return 0

    def printUrls(self):
        """
        Author: Bill Clark
        This method prints all the urls contained in the object in a readable manner. As readable as lines of character
        length 2000~ can be. It labels the base url (used for image merging) and then lists all layer images.
        """
        print "Base Url: " + self.urlbase
        for url in self.urllist:
            print url
        print self.url

    def __str__(self):
        """
        Author: Bill Clark
        Simple override so that printing the object prints the url's it has with in it.
        :return: ToString of the url's contained in the object.
        """
        ret = ""
        ret += self.urlbase + '\n'
        for url in self.urllist:
            ret += url + '\n'
        ret += self.url
        return ret

if __name__ == "__main__":
    url = UrlBuilder('600x600')
    url.centerparams('40.714728,-73.998672', '17')
    loc = ['40.714728,-73.998372', '40.715728,-73.999672', '40.715728,-73.998372', '40.714728,-73.998372']
    #locmini = {'40.714728,-73.998372', '40.715728,-73.999672'}
    url.addparam('scale', '2')
    url.addmarkers({'color': 'red'}, loc)
    url.addpath({'weight':'1', 'fillcolor': 'yellow'}, loc)
    url.printUrls()
    url.download()
