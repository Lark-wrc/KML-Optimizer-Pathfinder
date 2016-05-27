from GeometricDataStructures.KmlFasade import KmlFasade
import os

argzero = os.path.dirname(os.path.dirname(__file__)) + '\Inputs\KML Files\\advancedexample1.kml'
argtwo = os.path.dirname(os.path.dirname(__file__)) + '\Inputs\KML Files\\advancedexample2.kml'
argone = os.path.dirname(os.path.dirname(__file__)) + '\Inputs\KML Files\us_states.kml'
argarctic = os.path.dirname(os.path.dirname(__file__)) + '\Inputs\KML Files\\arctic lines jan 31.kml'
argtest = os.path.dirname(os.path.dirname(__file__)) + '\Inputs\KML Files\\tester.kml'


#Create the KmlFasade
fasade = KmlFasade(argone)

fasade.removeGarbageTags()
fasade.extract_html_metadata()