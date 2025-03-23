from django.db import models


class FarmContacts(models.Model):
    farmContactID = models.AutoField(primary_key=True)
    farmID        = models.ForeignKey("FarmAcc.FarmInfo", on_delete=models.CASCADE) # From Tasks
    order         = models.PositiveIntegerField()
    name          = models.CharField(max_length=64)
    image         = models.ImageField(upload_to="images/contact_images", default = "images/contact_images/defaultImage.png", null=False, blank=False)
    desc          = models.CharField(max_length=128)
    deleted       = models.BooleanField(default=False)


class ContactInfo(models.Model):
    contactInfoID = models.AutoField(primary_key=True)
    farmContactID = models.ForeignKey("Emergency.FarmContacts", on_delete=models.CASCADE)
    order         = models.PositiveIntegerField()
    FIELD_CHOICES = {
        "PH": "Phone"  ,
        "EM": "Email"  ,
        "AD": "Address",
        "WB": "Website",
        "NA": "Other"
    }
    field         = models.CharField(max_length=2, choices=FIELD_CHOICES)
    info          = models.CharField(max_length=64)
    deleted       = models.BooleanField(default=False)
