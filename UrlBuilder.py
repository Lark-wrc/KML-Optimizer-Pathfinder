class UrlBuilder(object):

    def __init__(self):
        """
        Author: Bill Clark
        Version = 1.0
        The UrlBuilder Class should be created anew for each url the user wants to build.
        Using the methods contained, the user may create a valid google maps static api url.
        Input is not checked, and ALL INPUTS SHOULD BE STRINGS. Even integer values should be entered repr()'d.
        """
        self.url = 'https://maps.googleapis.com/maps/api/staticmap?'

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
        curr = self.url[:]
        curr += '&&' + feature + '='
        curr += value
        self.url = curr
        return curr

    def addparams(self, dict):
        """
        Author: Bill Clark
        Version = 1.0
        Allows for a list of parameters to be added to the static map.
        :param dict: a dictionary of features:values from the addparam method.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """
        curr = self.url[:]
        for key in dict:
            curr += '&&' + key + '=' + dict[key]
        self.url = curr
        return curr

    def requiredparam(self, center, size, zoom):
        """
        Author: Bill Clark
        Version = 1.0
        These are specific parameters that every static maps url must contain. They're pulled aside they can
        all be hit in one method.
        :param center: The center point the map will display. latitude and longitude coordinates.
        :param size: the size of the returned image in pixels. [0-640]x[0-640]
        :param zoom: How far zoomed in the map slice will be. [1-20]
        :return: the url with the given parameter appended to it. Also updates saved url.
        """
        curr = self.url[:]
        curr += 'center='+center
        curr += '&&size='+size
        curr += '&&zoom='+zoom
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
        :param locations: Locations in a list format. Each will be added to be marked. list of lat long coordinates.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """
        curr = self.url[:]
        curr += '&&markers='

        for key in styles:
            curr += key + '=' + styles[key] + '|'

        for coordin in locations:
            curr += coordin + '|'

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
        :param locations: Locations in a list format. Each will be added to be marked. list of lat long coordinates.
        :return: the url with the given parameter appended to it. Also updates saved url.
        """
        curr = self.url[:]
        curr += '&&path='
        for key in styles:
            curr += key + ':' + styles[key] + '|'
        for coordin in locations:
            curr += coordin + '|'
        curr = curr[:-1]
        self.url = curr
        return curr

if __name__ == "__main__":
    url = UrlBuilder()
    url.requiredparam('40.714728,-73.998672', '600x600', '17')
    loc = ['40.714728,-73.998372', '40.715728,-73.999672', '40.715728,-73.998372']
    locmini = {'40.714728,-73.998372', '40.715728,-73.999672'}
    url.addparam('scale', '2')
    #url.addparams({'scale': '2', 'zoom': '17'})
    url.addmarkers({'color': 'red'}, loc)
    print url.addpath({'weight':'5'}, loc)
