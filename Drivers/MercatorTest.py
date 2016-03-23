from StaticMapsConnections.UrlBuilder import UrlBuilder
import GeometricDataStructures.Mercator

zoom = 16

build = UrlBuilder('600x600')
build.centerparams("40.856299,-74.243730", repr(zoom))

centerLat = 40.856299
centerLon = -74.243730
centerpoint = Mercator.LatLongPoint(centerLat, centerLon)
size = 600
corners = Mercator.get_corners(centerpoint, zoom, size, size)
cornerCoords = [repr(corners['N']) + "," + repr(corners['W']),
                repr(corners['N']) + "," + repr(corners['E']),
                repr(corners['S']) + "," + repr(corners['E']),
                repr(corners['S']) + "," + repr(corners['W']),
                repr(corners['N']) + "," + repr(corners['W'])]

build.addmarkers({"color":"red"}, ["-75.094389,40.049510"])
build.addpath({"color":"red", "weight":'5'}, cornerCoords)
print build.url
