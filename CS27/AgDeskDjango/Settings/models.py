from django.db import models
from FarmAcc.models import FarmInfo
from django.contrib.auth.models import Group
from UserAuth.models import UserProfile
from FarmAcc.models import FarmInfo


# from UserAuth.models import User

class orgSettingsModel(models.Model):
    timezone          = models.CharField(max_length=100)
    datetime_format   = models.CharField(max_length=100)
    temperature_label = models.CharField(max_length=50 )
    mass_label        = models.CharField(max_length=50 )
    area_label        = models.CharField(max_length=50 )
    length_label      = models.CharField(max_length=50 )


class internalTeamsModel(Group):
    """
    The internalTeam model is used to define teams which are situated within a specific farming
    tenant.
    """

    teamName        = models.CharField(max_length=100)
    # creationDate    = models.DateTimeField(default=)
    # teamModerator   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    teamDescription = models.CharField(max_length=1000)
    active          = models.BooleanField(default=True)
    teamImage       = models.ImageField(upload_to="images/internalTeams", default="images/internalTeams/default.jpg")
    farm            = models.ForeignKey(FarmInfo, on_delete=models.SET_NULL, null=True)
