
class KmlComposite:

    def __init__(self, *fasades):
        """
        `Author`: Bill Clark

        This class wraps kml fasades. It's functions through the composite method. Any call made to a
        KmlComposite calls the associated method on the fasades it wraps. No other actions are taken.
        One method is missing from KmlFasade, adding geometry. It's rarely used, and more importantly
        doesn't work with the concept of apply the same action to all members.

        `fasades`: A list of Kml Fasades.
        """
        self.fasades = fasades

    def rewrite(self):
        for fasade in self.fasades:
            fasade.rewrite()

    def removeGarbageTags(self):
        for fasade in self.fasades:
            fasade.removeGarbageTags()

    def pullPlacemarksAndGarbage(self):
        for fasade in self.fasades:
            fasade.pullPlacemarksAndGarbage()

    def fasadeUpdate(self):
        for fasade in self.fasades:
            fasade.fasadeUpdate()

    def createAdditionsFolder(self):
        for fasade in self.fasades:
            fasade.createAdditionsFolder()

    def yieldGeometrics(self):
        for fasade in self.fasades:
            yield fasade.geometrics