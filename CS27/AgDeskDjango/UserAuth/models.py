"""
Models for UserAuth.
"""

# Imports
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, Group, Permission
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.text import slugify

from .apps import UserauthConfig

from FarmAcc.models import FarmInfo


# Models
class UserProfile(AbstractUser):
    """
    The UserProfile model is used to define the user object within the Django application.
    """

    firstName   = models.CharField(max_length=200, null=True)
    lastName    = models.CharField(max_length=200, null=True)
    phoneNumber = models.CharField(max_length=200, null=True)
    farm        = models.ManyToManyField(FarmInfo, related_name="user_profiles", through="user_farm")
    currentFarm = models.ForeignKey(null=True, on_delete=models.CASCADE, to=FarmInfo)


class user_farm(models.Model):
    user            = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    farm            = models.ForeignKey(FarmInfo, on_delete=models.CASCADE)
    is_active       = models.BooleanField(default=True)
    date_joined     = models.DateTimeField(auto_now_add=True)
    workingLocation = models.CharField(max_length=300, null=True)
    role            = models.CharField(max_length=200, null=True)
    jobTitle        = models.CharField(max_length=30, null=True)

    # class Meta:
    #     permissions = [
    #         ("can_view_other_users", "Can view other user accounts")
    #     ]


class SecurityGroup(Group):
    """
    The SecurityGroup model is used to define security groups within the application.
    """

    class Meta:
        pass


# Database Permissions Initialisation
@receiver(post_migrate)
def create_instances(sender, **kwargs):
    """
    ### docstring 1:
        The following function, following a migration, will instantiate the necessary Security
        Groups into the Django application.

    ### docstrong 2:
        This function is invoked following a migration and will instantiate the RBAC groups within
        the application.

    ---

    ### Hot take
    This stuff doesn't seem to work, probably due to a missapplication of `posrt_migrate`. More
    details can be found on the Notion once that's available.
    """

    # FARM_EMPLOYEE          = SecurityGroup.objects.get_or_create(name="Farm Employee"          )
    # INVENTORY_MANAGER      = SecurityGroup.objects.get_or_create(name="Inventory Manager"      )
    # FARM_MANAGER           = SecurityGroup.objects.get_or_create(name="Farm Manager"           )
    # TEAM_LEADER            = SecurityGroup.objects.get_or_create(name="Team Leader"            )
    # FARM_OWNER             = SecurityGroup.objects.get_or_create(name="Farm Owner"             )
    # FLEET_MANAGER          = SecurityGroup.objects.get_or_create(name="Fleet Manager"          )
    # FARM_OPERATIONS_MANGER = SecurityGroup.objects.get_or_create(name="Farm Operations Manager")
    # STORAGE_MANAGER        = SecurityGroup.objects.get_or_create(name="Storage Manager"        )
    # FINANCIAL_CONTROLLER   = SecurityGroup.objects.get_or_create(name="Financial Controller"   )

    # # Assign permissions to groups
    # # https://medium.com/djangotube/django-roles-groups-and-permissions-introduction-a54d1070544#:~:text=What%20are%20permissions%20Permissions%20are%20a%20rule%20%28or,permissions%20to%20specific%20users%20and%20groups%20of%20users.
    # # - - - - - - - - - - - - - - -

    # viewOtherUsersPerm = Permission.objects.get(codename="can_view_other_users")
    # viewOtherUsersPerm.save()
    # farmOwner = SecurityGroup.objects.get(name="Farm Owner")
    # farmOwner.permissions.add(viewOtherUsersPerm)
