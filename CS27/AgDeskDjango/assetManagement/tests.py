# from django.test import TestCase
# from random import *
# from .views import *
# # from UserAuth.models import UserProfile
# from FarmAcc.models import FarmInfo

# farmSet = FarmInfo.objects.filter().all()

# def pickRandomFarm():
#     farmSetMin = farmSet[0]
#     farmSetMax = len(farmSet)

#     return randrange(farmSetMin, farmSetMax)["id"]


# smallAssetGroup = [
#     {
#         "assetName": "Small Generator",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2020-01-01",
#         "serialNumber": "123456789",
#         "Manufacturer": "Honda",
#         "Age": 2,
#         "partsList": "Spark Plug, Oil Filter, Air Filter",
#         "Location": "Barn"
#     },
#     {
#         "assetName": "Drill",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2021-01-01",
#         "serialNumber": "123433356789",
#         "Manufacturer": "DeWalt",
#         "Age": 2,
#         "partsList": "Drill Bits, Battery Pack",
#         "Location": "Tool Shed"
#     },
#     {
#         "assetName": "Flashlight",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2023-01-01",
#         "serialNumber": "123452226789",
#         "Manufacturer": "Maglite",
#         "Age": 10,
#         "partsList": "Batteries",
#         "Location": "House"
#     },
#     {
#         "assetName": "Wrench",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2023-01-01",
#         "serialNumber": "123452226333789",
#         "Manufacturer": "Craftsman",
#         "Age": 4,
#         "partsList": "N/A",
#         "Location": "Tool Shed"
#     }
# ]

# LargeAssetGroup = [
#     {
#         "assetName": "Large Generator",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2024-01-01",
#         "vin": "123456789",
#         "Manufacturer": "Cater",
#         "Age": 2,
#         "partsList": "Spark Plug, Oil Filter, Air Filter",
#         "Location": "Barn"
#     },
#     {
#         "assetName": "Solar Panel",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2024-01-01",
#         "vin": "1234567832319",
#         "Manufacturer": "energex",
#         "Age": 2,
#         "partsList": "Flux capacitor, Cobalt, Glass",
#         "Location": "Barn Roof"
#     },
#     {
#         "assetName": "Petrol Powered Pump",
#         "farmID": pickRandomFarm(),
#         "datePurchased": "2024-01-01",
#         "vin": "123456789",
#         "Manufacturer": "Cater",
#         "Age": 2,
#         "partsList": "Spark Plug, Oil Filter, Air Filter",
#         "Location": "Dam"
#     },
# ]


# iterator = 0
# testAssetManager = AssetManager()

# while iterator < len(smallAssetGroup):
#     testAssetManager.createAsset("sequipment", smallAssetGroup[iterator])
#     testAssetManager.createAsset("lequipment", LargeAssetGroup[iterator])
#     iterator += 1

# Adivice from a madman
# The following line will increment and compare at once.
#     while (i := i + 1) < len(amallAssetGroup):
# Though, I'm not sure if you'll be yelled at by your fellows for using this.
# Also, you need to make sure that you start with i = -1, since it's ++i rather than i++.
