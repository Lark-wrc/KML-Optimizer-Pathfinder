from GeometricDataStructures.KmlFasade import KmlFasade

argzero = 'C:\Users\Bob S\PycharmProjects\KML-Optimizer-Pathfinder\Inputs\KML Files\\advancedexample1.kml'
argtwo = 'Inputs\KML Files\\advancedexample2.kml'
argone = 'C:\Users\Bob s\PycharmProjects\KML-Optimizer-Pathfinder\Inputs\KML Files\us_states.kml'
argarctic = 'Inputs\KML Files\\arctic lines jan 31.kml'
argtest = 'Inputs\KML Files\\tester.kml'


#Create the KmlFasade
fasade = KmlFasade(argone)

fasade.removeGarbageTags()
fasade.extract_html_metadata()