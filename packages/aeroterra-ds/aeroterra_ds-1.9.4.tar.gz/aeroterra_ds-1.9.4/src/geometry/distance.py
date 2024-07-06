from haversine import haversine, Unit

from shapely.ops import nearest_points
from shapely import distance

from .change_crs import change_crs

def distance_geometries(geom_a, geom_b, crs_a=None, crs_b=None, do_haversine=True, units=Unit.KILOMETERS):
    """
    Given 2 shapely geometries, it returns the distance between them

    Parameters:
        - geom_a: First geometry to compare
        - geom_b: Seconda geometry to compare
        - crs_a: CRS of the geom_a. If not given and asked for haversine,
            epsg:4326 will be assumed.
        - crs_b: CRS of the geom_b. If not given and asked for haversine,
            epsg:4326 will be assumed.
        - do_haversine (Optional): If wanted to check the distance in haversine.
            By default in True.
        - units (Optional): If using haversine, what unit to return. Must use 
            Haversine.Units strcuture like element. By default in Kilometers
    """
    if not do_haversine and crs_a and crs_b and crs_b != crs_a:
        raise Exception("Can't Use Different CRS for non haversine distance")
    
    if do_haversine and crs_a != 4326:
        geom_a = change_crs(geom_a, crs_a, 4326)
    
    if do_haversine and crs_b != 4326:
        geom_b = change_crs(geom_b, crs_b, 4326)
    
    point_a, point_b = nearest_points(geom_a, geom_b)

    if not do_haversine:
        return distance(point_a, point_b)
    else:
        point_a = (point_a.y, point_a.x)
        point_b = (point_b.y, point_b.x)
        return haversine(point_a, point_b, unit=units)


