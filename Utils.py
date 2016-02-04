from lxml import etree

debug = 0
geometryTypes = ('Point', 'LineString','LinearRing', 'MultiGeometry') #Polygon is removed

def elementPrint(element, bool=0):
    if bool:
        return etree.tostring(element,pretty_print=False)
    else:
        return etree.tostring(element,pretty_print=True)
