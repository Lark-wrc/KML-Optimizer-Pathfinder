import math
from GeometricDataStructures import Geometrics, KmlFasade

def closest_point(source, a, b):
    # Verified
    a_distance = math.sqrt((a.lat - source.lat)**2+(a.lng-source.lng)**2)
    b_distance = math.sqrt((b.lat - source.lat)**2+(b.lng-source.lng)**2)
    if a_distance > b_distance:
        return b
    return a

def find_poi(a, b, p, q):

    if p.lng == q.lng:
        sub_m = (b.lat - a.lat) / (b.lng - a.lng)
        sub_b = a.lt - (sub_m * a.lng)
        y = (sub_m * p.lng) + sub_b
        return KmlFasade.LatLongPoint(p.lng, y)

    if a.lng == b.lng:
        obj_m = (q.lat - p.lat) / (q.lng - p.lng)
        obj_b = p.lat - (obj_m * p.lng)
        y = (obj_m * a.lng) + obj_b
        return KmlFasade.LatLongPoint(a.lng, y)

    sub_m = (b.lat - a.lat) / (b.lng - a.lng)
    obj_m = (q.lat - p.lat) / (q.lng - p.lng)
    sub_b = a.lt - (sub_m * a.lng)
    obj_b = p.lat - (obj_m * p.lng)
    x = ((-1 * sub_b) + obj_b) / (sub_m - obj_m)
    y = (sub_m * p.lng) + sub_b
    return KmlFasade.LatLongPoint(x, y)

def intersect(a, b, p, q):
    o1 = get_orientation(a, b, p)
    o2 = get_orientation(a, b, q)
    if o1 != o2:
        o3 = get_orientation(p, q, a)
        o4 = get_orientation(p, q, b)
        if o3 != o4:
            return True
    return False

def get_orientation(a, b, c):
    mat = [[a.lat, b.lat, c.lat], [a.lng, b.lng, c.lng]]
    first = mat[0][0] * mat[1][1] + mat[1][0] * mat[0][2] + mat[0][1] * mat[1][2]
    second = mat[0][2] * mat[1][1] + mat[1][2] * mat[0][0] + mat[0][1] * mat[1][0]
    if first - second > 0:
        return 1
    elif first - second < 0:
        return -1
    else:
        return 0

def clip(viewport, subject):
    viewport_points = viewport.coordinates
    subject_points = subject.coordinates
    intersections = []
    intersection_polygon = []
    return viewport_points
    # Construct the new subject polygon
    new_subject = subject_points
    for sub_start in xrange(1, len(subject_points)):
        sub_start_point = subject_points[-sub_start]
        sub_end = sub_start + 1
        sub_end_point = subject_points[-sub_end]
        new_subject.append(sub_start_point)
        intersection_count = 0
        for view_start in xrange(0, len(viewport_points)):
            view_start_point = viewport_points[view_start]
            view_end = view_start + 1
            view_end_point = viewport_points[view_end]
            # Remember negative indexes in this part
            if intersect(sub_start_point, sub_end_point, view_start_point, view_end_point):
                point = find_poi(sub_start_point, sub_end_point, view_start_point, view_end_point)
                new_subject.append(point)
                intersections.append(point)
                intersection_count += 1
            if intersection_count > 1:
                closest = closest_point(sub_start, intersections[-1], intersections[-2])
                if closest is point:
                    temp = intersections[-1]
                    intersections[-1] = intersections[-2]
                    intersections[-2] = temp

                    temp = new_subject[-1]
                    new_subject[-1] = new_subject[-2]
                    new_subject[-2] = temp

    gf = Geometrics.GeometricFactory()
    string_list = ""
    for i in intersection_polygon:
        string_list += repr(i) + " "
    return gf.createLiteral(None, "LineString", string_list)
