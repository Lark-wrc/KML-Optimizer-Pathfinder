from urllib import urlretrieve

class UrlBuilder(object):

    def __init__(self, size):
        """
        Author: Bill Clark
        Version = 2.0
        The UrlBuilder Class should be created anew for each url the user wants to build.
        Using the methods contained, the user may create a valid google maps static api url.
        Input is not checked, and ALL INPUTS SHOULD BE STRINGS. Even integer values should be entered repr()'d.
        All inputs will be need to be converted to Lat Long, as all other files use Long Lat.
        :param size: the size of the returned image in pixels. [0-640]x[0-640]
        """

        self.urlbase = 'https://maps.googleapis.com/maps/api/staticmap?'
        self.url = self.urlbase
        self.url += 'size='+size
        self.urllist = []
        self.limit = 50 #Proper limit is 2048, buffer of 48.

    def addparam(self, feature, value):
        """
        Author: Bill Clark
        Version = 1.0
        Appends the given parameter to the static maps url.
        :param feature: The name of the parameter. Valid: scale | maptype | format | region?
        :param value: the value of the parameter. Valid: 1,2,4 | roadmap, satellite, hybrid, terrain |
                                                                png, jpg, png32, gif, jpg-baseline
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = ""
        curr += '&&' + feature + '='
        curr += value

        self.retireUrl(self.url, self.countUrl(curr))
        self.url += curr
        return self.url

    def addparams(self, dict):
        """
        Author: Bill Clark
        Version = 1.0
        Allows for a list of parameters to be added to the static map.
        :param dict: a dictionary of features:values from the addparam method.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = ""
        for key in dict:
            curr += '&&' + key + '=' + dict[key]

        self.retireUrl(self.url, self.countUrl(curr))
        self.url += curr
        return self.url

    def centerparams(self, center, zoom):
        """
        Author: Bill Clark
        Version = 2.0
        This is a shortcut method that adds the two values a url must contain to be valid, given the url
        has no viewpoint, marker, or path. It adds center and zoom.
        :param center: The center point the map will display. latitude and longitude coordinates.
        :param zoom: How far zoomed in the map slice will be. [1-20]
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        if len(self.urlbase) > 47:
            return 0
        curr = ""
        curr += '&&center='+center
        curr += '&&zoom='+zoom
        self.urlbase += curr
        self.url = self.urlbase
        return self.url

    def viewportparam(self, viewports):
        """
        Author: Bill Clark
        Version: 1.0
        Appends a viewport parameter. A viewport makes each point it is given visible on the map.
        :param viewports: Locations in a list format. Each will be made visible.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&visible='
        if type(viewports) is list:
            for coordin in viewports:
                curr += coordin + '|'
                if self.retireUrl(curr):
                    curr += '&&visible=' + coordin + '|'
            curr = curr[:-1]
        elif type(viewports) is str:
            curr += (viewports)
        self.url = curr
        return curr

    def addmarkers(self, styles, locations):
        """
        Author: Bill Clark
        Version = 2.0
        Adds the marker list to the url. Each point will have the supplied style settings.
        :param styles: Style settings, which function like parameters, a dict of name and value.
                        Valid Names: size | label | color
                        Valid value: tiny, mid, small, normal | [A-Z] or [0-9] | [hexvalue] or color name
        :param locations: Locations in a list format. Each will be added to be marked. list of  coordinates.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&markers='

        for key in styles:
            curr += key + ':' + styles[key] + '|'

        if type(locations) is list:
            for coordin in locations:
                curr += coordin + '|'
        elif type(locations) is str:
            curr += (locations)

        curr = curr[:-1]
        self.url = curr
        return curr

    def addpath(self, styles, locations):
        """
        Author: Bill Clark
        Version = 2.0
        Adds the path list to the url. The lines drawn and area filled will have the style setting specified.
        :param styles: Style settings, which function like parameters, a dict of name and value.
                        Valid Names: weight | geodesic | color | fillcolor
                        Valid value: [0-.] | T or F | [hexvalue] or [hexvalue32] or color name | same as color
        :param locations: Locations in a list format. Each will be added to be marked. list of coordinates.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """

        curr = self.url[:]
        curr += '&&path='
        for key in styles:
            curr += key + ':' + styles[key] + '|'
        if type(locations) is list:
            for coordin in locations:
                curr += coordin + '|'
        elif type(locations) is str:
            curr += (locations)
        curr = curr[:-1]
        self.url = curr
        return curr

    def download(self, path="C:\Users\Research\Documents\Code Repositories\KML-Optimizer-Pathfinder\Inputs\Static Maps\\image.png"):
        """
        Author: Bill Clark
        Version: 1.0
        Takes a parameter path and downloads the generated url to that path.
        :param path: a file path to save the generated image to.
        :return: the download function returns the saved path and response data, which is returned.
        """

        return urlretrieve(self.url, path)

    def countUrl(self, url):
        """

        :return:
        """
        ret = 0
        for character in url:
            if character == "|": ret += 3
            else: ret += 1
        return ret

    def retireUrl(self, url, offset=0):
        """

        :param url:
        :return:
        """
        count = self.countUrl(url)+offset
        if count >= self.limit:
            self.urllist.append(url)
            self.url = self.urlbase[:]
            return 1
        else:
            return 0


if __name__ == "__main__":
    url = UrlBuilder('600x600')
    url.centerparams('40.714728,-73.998672', '17')
    loc = ['40.714728,-73.998372', '40.715728,-73.999672', '40.715728,-73.998372', '40.714728,-73.998372']
    locmini = {'40.714728,-73.998372', '40.715728,-73.999672'}
    url.addparam('scale', '2')
    url.addmarkers({'color': 'red'}, loc)
    #url.addpath({'weight':'1', 'fillcolor': 'yellow'}, loc)
    print url.url
    url.download()
