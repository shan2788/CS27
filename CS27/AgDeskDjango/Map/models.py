from django.contrib.gis.db import models  # ✅ GeoDjango
from django.utils import timezone

from FarmAcc.models import FarmInfo


class NDVIRegion(models.Model):
    farm = models.ForeignKey(FarmInfo, on_delete=models.CASCADE)
    geometry = models.PolygonField(srid=4326)
    image = models.ImageField(upload_to='ndvi_images/')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"NDVIRegion {self.id} - {self.farm.farm_name}"

class NDVIReport(models.Model):
    farm = models.ForeignKey(FarmInfo, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='report/')
    geolocation = models.PolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"NDVI Report: {self.start_date} → {self.end_date}"
    
class CarbonCredit(models.Model):
    farm = models.ForeignKey(FarmInfo, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    file_path = models.FileField(upload_to='report/')
    geolocation = models.PolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carbon Credit Report: {self.start_date} → {self.end_date}"