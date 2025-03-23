from django.db import models
from polymorphic.models import PolymorphicModel
from FarmAcc.models import FarmInfo
from UserAuth import *


class asset(PolymorphicModel):
    assetPrefix      = models.CharField(max_length=2, null=False)
    assetID          = models.AutoField(primary_key=True)
    assetName        = models.CharField(max_length=100, null=False)
    farmID           = models.ForeignKey(FarmInfo, on_delete=models.CASCADE, null=False)
    Manufacturer     = models.CharField(max_length=100)
    partsList        = models.CharField(max_length=255)
    Location         = models.CharField(max_length=100)
    dateManufactured = models.DateField(null=False)
    datePurchased    = models.DateField(null=False)
    deleted          = models.BooleanField(default=False)
    assetImage       = models.ImageField(upload_to="images/asset_images",
                                         default = "images/asset_images/defaultImage.jpg",
                                         null=False, blank=False)
    # Refactoring required:
    #     asset should also contain age, manufacturer, location, and parts list

    def __str__(self):
        return f"{self.assetID}-{self.assetPrefix} - {self.assetName}"


class vehicle(asset):
    vin = models.CharField(max_length=100, null=False)
    Registration = models.CharField(max_length=100)

    class Meta:
        abstract = True


class SmallEquipment(asset):
    """
    Small Equipment Class
    Small Equipment includes tools such as flashlights, drills, small generators, etc.
    """

    serialNumber = models.CharField(max_length=100, null=False)


class LargeEquipment(asset):
    """
    Large Equipment Class
    Large Equipment includes objects such as diesel generators, large pumps, and other large machinery.
    """

    vin = models.CharField(max_length=100, null=False)

#These need refactoring
#The following classes are no longer used in the current build of this app and can be removed in future.
class lightVehicle(vehicle):
    """
    Light Vehicle Class
    A Light Vehicle is any passenger vehicle such as a utility, sedan, or small truck.
    """

    currentlyInUse = models.BooleanField()


class heavyVehicle(vehicle):
    """
    Heavy Vehicle Class
    A Heavy Vehicle can be anything such as a tactor, harvester, large truck or other large farm machinery.
    """

    inTransport = models.BooleanField()
    interFarmTransport = models.BooleanField()
