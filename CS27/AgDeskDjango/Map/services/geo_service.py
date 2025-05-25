from shapely.geometry import shape
from shapely.ops import unary_union
import geopandas as gpd
from shapely.geometry import Polygon

class GeoService:
    """
    A utility service class for geospatial operations, such as comparing geometries and calculating area.
    """

    def __init__(self):
        """
        Initialize the GeoService class.
        """
        pass

    @staticmethod
    def are_geometries_similar(geometry1, geometry2, threshold=0.8):
        """
        Check whether two geometries are spatially similar based on their intersection area ratio.

        Args:
            geometry1 (dict): The first geometry in GeoJSON format.
            geometry2 (dict): The second geometry in GeoJSON format.
            threshold (float): A threshold value (between 0 and 1) indicating the minimum
                               overlap ratio required to consider the geometries similar.
                               Default is 0.8.

        Returns:
            bool: True if the geometries overlap at or above the threshold, False otherwise.
        """
        geom1 = shape(geometry1)
        geom2 = shape(geometry2)

        intersection_area = geom1.intersection(geom2).area
        union_area = unary_union([geom1, geom2]).area

        overlap_ratio = intersection_area / union_area

        return overlap_ratio >= threshold

    @staticmethod
    def calculate_area_square(region_coordinates):
        """
        Calculate the area of a polygonal region given its coordinates, in square kilometers.

        Args:
            region_coordinates (list of tuple): A list of (longitude, latitude) tuples representing
                                                the region boundary as a polygon.

        Returns:
            float: The area of the region in square kilometers.
        """
        region_polygon = Polygon(region_coordinates)
        region_gdf = gpd.GeoDataFrame([1], geometry=[region_polygon], crs="EPSG:4326")
        region_gdf_projected = region_gdf.to_crs("EPSG:3857")

        area_square_km = region_gdf_projected.geometry[0].area / 1_000_000

        return area_square_km
