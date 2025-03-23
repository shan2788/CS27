"""
Models for farms and files
"""

# Imports
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


# Farms
class FarmInfo(models.Model):
    farm_name     = models.CharField(max_length=100)
    farm_street   = models.CharField(max_length=100)
    farm_state    = models.CharField(max_length=20 )
    farm_postcode = models.CharField(max_length=6  )
    farm_address  = f"{farm_street}, {farm_state}, {farm_postcode}"
    farm_bio      = models.TextField()
    farm_image    = models.ImageField(
        upload_to  = "images/farm_images"                  ,
        default    = "images/farm_images/default_image.png",
        blank      = True                                  ,
        null       = True
    )

    def __str__(self):
        return self.farm_name


class LinkingCode(models.Model):
    code       = models.CharField(unique=True)
    farm       = models.ForeignKey(FarmInfo, on_delete=models.CASCADE, related_name="linking_codes")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Default expiry set to 12 hours after creation
            self.expires_at = datetime.now() + timedelta(hours=12)
        super().save(*args, **kwargs)


# Files
class FileCategory(models.Model):
    """
    The following enables users to define categories to assign documents to.
    """

    # File Category Attributes 
    fileCategoryName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.fileCategoryName


class FileRecord(models.Model):
    """
    The FileRecord model is used to store farm related documents within the Django application,
    which farmers can set review dates for. When a new File Record is instantiated, it is uploaded
    under the 'files' directory within the media folder.
    """

    # File Record Attributes
    fileName     = models.CharField(max_length=100    )
    reviewDate   = models.DateField(null=True         )
    file         = models.FileField(upload_to="files/")
    fileCategory = models.ForeignKey(FileCategory, on_delete=models.SET_NULL,  null=True, blank=True)
