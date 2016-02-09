class UrlBuilder(object):

    def __init__(self):
        self.url = 'https://maps.googleapis.com/maps/api/staticmap?'

    def addparam(self, feature, value):
        curr = self.url
        curr += '&&' + feature + '='
        curr += value
        self.url = curr
        return curr

    def requiredparam(self, center, size):
        curr = self.url
        curr += 'center='+center
        curr += '&&size='+size
        self.url = curr
        return curr

    def addmarkers(self, locations):
        for key in locations:
