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
