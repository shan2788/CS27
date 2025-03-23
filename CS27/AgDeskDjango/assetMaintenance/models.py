from django.db import models
from assetManagement.models import asset
from UserAuth.models import UserProfile

# choice conversion dictionary

maintenanceTypeChoices = {
    0: "General",
    1: "Scheduled Service",
    2: "Inspection",
    3: "Repair",
}

damageSeverityChoice = {
    0: "Minor",
    1: "Moderate",
    2: "Severe",
    3: "Critical"
}


class Damage(models.Model):
    damageID                 = models.AutoField(primary_key=True)
    assetID                  = models.ForeignKey(asset, on_delete=models.CASCADE, null=False)
    damageObservedDate       = models.DateField(null=False)
    damageOccuredDate        = models.DateField(null=True, blank=True)
    damageType               = models.CharField(max_length=100, null=False)
    damageSeverity           = models.SmallIntegerField(choices=damageSeverityChoice, default=0)
    notes                    = models.CharField(max_length=255, null=True, blank=True)
    damageImage              = models.ImageField(upload_to="damageImages/", default="images/asset_images/defaultImage.jpg", null=False, blank=True)
    scheduledMaintenanceDate = models.DateField(null=True, blank=True)
    deleted                  = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{str(self.damageID)} - ({self.damageType})"


class Maintenance(models.Model):
    maintenanceID             = models.AutoField(primary_key=True)
    assetID                   = models.ForeignKey(asset, on_delete=models.CASCADE, null=False)
    completionDate            = models.DateField(null=False)
    maintenanceType           = models.PositiveIntegerField(choices=maintenanceTypeChoices, default=0)
    maintenanceConductedBy    = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    maintenanceLocation       = models.CharField(max_length=100, null=False)
    maintenanceTasksCompleted = models.CharField(max_length=255, null=False)
    repairsCompleted          = models.ForeignKey(Damage, on_delete=models.CASCADE, null=True, blank=True)
    Cost                      = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    Notes                     = models.CharField(max_length=255, null=False)
    kmsBeforeNextService      = models.IntegerField(null=True, blank=True)
    dateOfNextService         = models.DateField(null=False)
    deleted                   = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{str(self.maintenanceTasksCompleted)} - {self.maintenanceTasksCompleted}"
