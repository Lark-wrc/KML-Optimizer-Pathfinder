from GeometricDataStructures.Mercator import MercatorPoint

class Clipper():

    def __init__(self):
        pass

    def verticalCheck(self, aLine, bLine):
        if aLine.start.x == aLine.end.x:
            aLine.slope = (aLine.end.y - aLine.start.y) / (aLine.end.x - aLine.start.x)
            aLine.cept = aLine.start.y - (aLine.slope * aLine.start.x)
            y = (aLine.slope * bLine.start.x) + aLine.cept
            return MercatorPoint(bLine.start.x, y)
        else: return None
