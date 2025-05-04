from shapely.geometry import shape
from shapely.ops import unary_union
import geopandas as gpd
from shapely.geometry import Polygon

class GeoService:
    def __init__(self):
        pass

    def are_geometries_similar(self, geometry1, geometry2, threshold=0.8):
        """
        Check if two geometries are similar based on their intersection area.

        Args:
            geometry1: The first geometry (GeoJSON format).
            geometry2: The second geometry (GeoJSON format).
            threshold: The minimum overlap ratio to consider as similar (default is 0.8).

        Returns:
            True if the overlap ratio is greater than or equal to the threshold, False otherwise.
        """
        geom1 = shape(geometry1)
        geom2 = shape(geometry2)

        # Calculate intersection and union areas
        intersection_area = geom1.intersection(geom2).area
        union_area = unary_union([geom1, geom2]).area

        # Calculate overlap ratio
        overlap_ratio = intersection_area / union_area

        return overlap_ratio >= threshold
    
    def calculate_area_square(self, region_coordinates):
        """
        Calculate the area in square kilometers of a selected region.
        :param region_coordinates: List of tuples [(lat, lon), ...] representing the region
        :return: Area in square kilometers
        """
        # Create a polygon from region coordinates
        region_polygon = Polygon(region_coordinates)

        # Convert the polygon to a GeoDataFrame for area calculation
        region_gdf = gpd.GeoDataFrame([1], geometry=[region_polygon], crs="EPSG:4326")

        # Transform the GeoDataFrame to a projected CRS (meters) for accurate area calculation
        region_gdf_projected = region_gdf.to_crs("EPSG:3857")

        # Calculate the area in square meters and convert to square kilometers
        area_square_km = region_gdf_projected.geometry[0].area / 1_000_000

        return area_square_km