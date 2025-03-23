"""
Some ultility functions for stuff related to Farm Accounts
"""

# Imports
from .models import FarmInfo
from UserAuth.models import UserProfile, user_farm


# Functions
def getFarmUsersByFarmID(farmID):
    userIDs = user_farm.objects.filter(farm_id=farmID).values("user_id")
    users = UserProfile.objects.filter(id__in=userIDs)

    return users
