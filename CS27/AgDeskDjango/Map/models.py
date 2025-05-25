from django.contrib.gis.db import models  # ✅ GeoDjango
from django.utils import timezone
from FarmAcc.models import FarmInfo

class NDVIRegion(models.Model):
    """
    Model representing a region of interest for NDVI analysis.

    Attributes:
        farm (ForeignKey): Reference to the associated farm.
        geometry (PolygonField): Geospatial polygon representing the region.
        image (ImageField): NDVI image generated for the region.
        created_at (DateTimeField): Timestamp of creation.
    """
    farm = models.ForeignKey(FarmInfo, on_delete=models.CASCADE)
    geometry = models.PolygonField(srid=4326)
    image = models.ImageField(upload_to='ndvi_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"NDVIRegion {self.id} - {self.farm.farm_name}"

class NDVIReport(models.Model):
    """
    Model for storing NDVI analysis reports associated with farms.

    Attributes:
        farm (ForeignKey): Reference to the associated farm.
        start_date (DateField): Start date of the NDVI data period.
        end_date (DateField): End date of the NDVI data period.
        file_path (FileField): File path to the generated PDF report.
        geolocation (PolygonField): Geospatial polygon of the reported region.
        created_at (DateTimeField): Timestamp of report creation.
    """
    farm = models.ForeignKey(FarmInfo, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='report/')
    geolocation = models.PolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NDVI Report: {self.start_date} → {self.end_date}"

class CarbonCredit(models.Model):
    """
    Model representing carbon credit eligibility reports based on biomass predictions.

    Attributes:
        farm (ForeignKey): Reference to the associated farm.
        start_date (DateField): Start date of the report range.
        end_date (DateField): End date of the report range.
        file_path (FileField): File path to the generated carbon report.
        geolocation (PolygonField): Geospatial polygon of the analyzed region.
        created_at (DateTimeField): Timestamp of report creation.
    """
    farm = models.ForeignKey(FarmInfo, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='report/')
    geolocation = models.PolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carbon Credit Report: {self.start_date} → {self.end_date}"
