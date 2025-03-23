"""
Tests for UserAuth
"""

# Import
from django.test import TestCase
import random

from utils.testing_data import FARM_SUPERSET, FILRECORD_SUPERSET
from utils.testing_data import generate_dataset_from_model

from UserAuth.models import *
from UserAuth.forms  import *
from UserAuth.views  import *


# Base
class BaseTestCase(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"    : FARM_SUPERSET["farm_name"    ][0],
            "farm_street"  : FARM_SUPERSET["farm_street"  ][0],
            "farm_state"   : FARM_SUPERSET["farm_state"   ][0],
            "farm_postcode": FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"     : FARM_SUPERSET["farm_bio"     ][0],
            "farm_image"   : FARM_SUPERSET["farm_image"   ][0]
        }

        farmList = [
            FarmInfo(**farm_data)
            for farm_data
            in generate_dataset_from_model(VALID_FARMS)
        ]
        self.farm = FarmInfo.objects.bulk_create(farmList)

        self.user = UserProfile.objects.create_user(
            username    = "testuser"          ,
            email       = "testuser@test.test",
            password    = "12345"             ,
            currentFarm = self.farm[0]
        )


# Forms
class SignUserUpFormTest(BaseTestCase):
    def setUp(self):
        super().setUp()


class UserLoginFormTest(BaseTestCase):
    def setUp(self):
        super().setUp()
