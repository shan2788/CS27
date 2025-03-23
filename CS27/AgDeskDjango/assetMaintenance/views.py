from django.shortcuts import render, redirect
from . import forms
from .models import Maintenance, Damage
from . import models
from assetManagement.models import asset, SmallEquipment, LargeEquipment, lightVehicle, heavyVehicle
from assetManagement.views import AssetManager, AssetStructures
from assetExpenses.models import Expense
from django.core import serializers
from django.contrib import messages
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required


class maintenanceManager():
    """
    Queries the Maintenance Model and returns maintenance records for assets.

    Arguments:

        assetID: int
        The ID of the asset to retrieve maintenance data for, if this is left blank all assets of a provided class will be retrieved.

        assetCategory: str
        The category of asset to retrieve maintenance data for, if this is left blank all maintenance records in the database will be retrieved.
    """

    def retrieveMaintenanceData(self, assetID=None, assetCategory="ALL"):
        """
            field_name
            The name of the model field that is filtered against. 
            If this argument is not provided, it defaults the filter's attribute name on the FilterSet class. 
            Field names can traverse relationships by joining the related parts with the ORM lookup separator (__). e.g., a product's manufacturer__name.
        """

        if assetID is not None and assetCategory != "ALL":
            #assetID_assetPrefix is a foreign key, so we can use the __ notation to access the assetPrefix field. Review Function documentation below.
            recordsFound = Maintenance.objects.filter(assetID=assetID, assetID__assetPrefix=assetCategory, deleted=False)
            return recordsFound

        elif assetID is not None and assetCategory == "ALL":
            completeRecordSet = Maintenance.objects.filter(assetID=assetID, deleteed=False)
            return completeRecordSet

        elif assetID is None and assetCategory != "ALL":
            completeRecordSet = Maintenance.objects.filter(assetID__assetPrefix=assetCategory, deleted=False)
            return completeRecordSet

        else:
            completeRecordSet = Maintenance.objects.all(deleted=False)
            return completeRecordSet

    def createMaintenanceRecord(self, maintenanceData, assetCategory, assetID):
        """
        Runs a Creation Query on the Maintenance Model to create a new maintenance record.

        Arguments:

                maintenanceData: dict
                The data to create the maintenance record with, this should be in the form of a dictionary with the key being the field to update and the value being the new data.
                maintenanceData should be passed through in the following format:
                {
                    "assetID": int,
                    "assetCategory": str,
                    "completionDate": date,
                    "maintenanceType": int,
                    "maintenanceConductedBy": str,
                    "maintenanceLocation": str,
                    "maintenanceTasksCompleted": str,
                    "repairsCompleted": int,
                    "Cost": decimal,
                    "Notes": str,
                    "kmsBeforeNextService": int,
                    "dateOfNextService": date
                }
        """

        assetStructures = AssetStructures()
        targetAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)
        newRecord = Maintenance(
            assetID                   = targetAsset,
            completionDate            = maintenanceData["completionDate"           ],
            maintenanceType            = maintenanceData["maintenanceType"          ],
            maintenanceConductedBy    = maintenanceData["maintenanceConductedBy"   ],
            maintenanceLocation       = maintenanceData["maintenanceLocation"      ],
            maintenanceTasksCompleted = maintenanceData["maintenanceTasksCompleted"],
            repairsCompleted          = maintenanceData["repairsCompleted"         ],
            Cost                      = maintenanceData["Cost"                     ],
            Notes                     = maintenanceData["Notes"                    ],
            kmsBeforeNextService      = maintenanceData["kmsBeforeNextService"     ],
            dateOfNextService         = maintenanceData["dateOfNextService"        ]
        )
        newRecord.save()

    def editMaintenanceData(self, maintenanceLogID, updateData):
        """
        Queries the Maintenance Model and performs updates based on the provided arguments.

        Arguments:
            MaintenanceLogID: int
            the unique identifier for the maintenance Log you want to update

            updateData: dict
            The data to update the maintenance record with, this should be in the form of a dictionary with the key being the field to update and the value being the new data.
            update data should be passed in the following format:
            {
                "completionDate": date,
                "maintenanceType": int,
                "maintenanceConductedBy": str,
                "maintenanceLocation": str,
                "maintenanceTasksCompleted": str,
                "repairsCompleted": int,
                "Cost": decimal,
                "Notes": str,
                "kmsBeforeNextService": int,
                "dateOfNextService": date
            }
            NOTE: The assetID field cannot be updated, as this is a foreign key and should not be changed.
        """
        targetMaintenanceRecord = Maintenance.objects.get(maintenanceID=maintenanceLogID)

        for key, value in updateData.items():
            setattr(targetMaintenanceRecord, key, value)
        targetMaintenanceRecord.save()

    def deleteMaintenanceData(self, maintenanceLogID):
        targetMaintenanceRecord = Maintenance.objects.get(maintenanceID=maintenanceLogID)
        targetMaintenanceRecord.deleted = True
        targetMaintenanceRecord.repairsCompleted_id = None
        targetMaintenanceRecord.save()

        # Check for associated expense records and update if necessary
        expenseRecords = self.getExpenseRecordFromMaintenance(maintenanceLogID)
        if len(expenseRecords) != 0:
            for expense in expenseRecords:
                expense.MaintenanceID_id = None
                expense.expenseType = 4
                expense.save()

    def getExpenseRecordFromMaintenance(self, maintenanceID):
        return Expense.objects.filter(MaintenanceID_id=maintenanceID)
    
    def retrieveMaintenanceRecordByID(self, maintenanceLogID):
        try:
            completeRecord = Maintenance.objects.get(pk=maintenanceLogID)
            completeRecord = model_to_dict(completeRecord)
            # Convert the date and times to user readable format from a datetime object
            completeRecord["completionDate"   ] = completeRecord["completionDate"   ].strftime("%d/%m/%Y")
            completeRecord["dateOfNextService"] = completeRecord["dateOfNextService"].strftime("%d/%m/%Y")
            return completeRecord
        except Damage.DoesNotExist:
            print("Maintenance Record Not Found")
            return {"error": "Maintenance Record Not Found"}
        except Exception as e:
            print(e)
            return {"error": str(e)}


class damageManager():
    def retrieveDamageData(self, assetID=None, assetCategory="ALL"):
        #The unfiltered Queryset is stored in a variable to be used later.
        completeRecordSet = None
        #The query set after filtered to remove damage logs that are deleted or marked repaired.
        filteredRecordSet = []

        if assetID is not None and assetCategory != "ALL":
            completeRecordSet = Damage.objects.filter(assetID=assetID, assetID__assetPrefix=assetCategory, deleted=False)
            damageInfoWithStatus = []
            repairedRecords = []
            nonRepairedRecords = []
            for damage in completeRecordSet:
                # Create a dict of the damage record and append it to the list
                damageInfo = {
                    "damageID"                : damage.damageID,
                    "damageObservedDate"      : damage.damageObservedDate,
                    "damageOccuredDate"       : damage.damageOccuredDate,
                    "damageType"              : damage.damageType,
                    "damageSeverity"          : models.damageSeverityChoice.get(damage.damageSeverity),
                    "notes"                   : damage.notes,
                    "damageImage"             : damage.damageImage,
                    "scheduledMaintenanceDate": damage.scheduledMaintenanceDate,
                    "deleted"                 : damage.deleted,
                    "assetID"                 : damage.assetID,
                    "status"                  : "Not Repaired"
                }

                if self.checkDamageRepairedByID(damage.damageID):
                    damageInfo["status"] = "Repaired"
                    repairedRecords.append(damageInfo)
                else:
                    nonRepairedRecords.append(damageInfo)
                    filteredRecordSet.append(damage)
                    print(damage)

            # Concatenate non-repaired records with repaired records
            damageInfoWithStatus = nonRepairedRecords + repairedRecords

            return damageInfoWithStatus

        elif assetID is not None and assetCategory == "ALL":
            completeRecordSet = Damage.objects.filter(assetID=assetID, deleted=False)
            for damage in completeRecordSet:
                if (not self.checkDamageRepairedByID(damage.damageID)):
                    filteredRecordSet.append(damage)
                    print(damage)

        elif assetID is None and assetCategory != "ALL":
            completeRecordSet = Damage.objects.filter(assetID__assetPrefix=assetCategory, deleted=False)
            for damage in completeRecordSet:
                if (not self.checkDamageRepairedByID(damage.damageID)):
                    filteredRecordSet.append(damage)
                    print(damage)

        else:
            completeRecordSet = Damage.objects.all(deleted=False)

        return filteredRecordSet

    def retrieveDamageRecordByID(self, damageLogID):
        try:
            completeRecord = Damage.objects.get(pk=damageLogID).__dict__
            completeRecord["damageObservedDate"      ] = completeRecord["damageObservedDate"      ].strftime("%d/%m/%Y")
            completeRecord["damageOccuredDate"       ] = completeRecord["damageOccuredDate"       ].strftime("%d/%m/%Y")
            completeRecord["scheduledMaintenanceDate"] = completeRecord["scheduledMaintenanceDate"].strftime("%d/%m/%Y")
            return completeRecord
        except Damage.DoesNotExist:
            print("Damage Record Not Found")
            return {"error": "Damage Record Not Found"}
        except Exception as e:
            print(e)
            return {"error": str(e)}

    def createDamageRecord(self, damageData, assetCategory, assetID):
        assetStructures = AssetStructures()
        targetAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)

        newRecord = Damage(
            assetID                  = targetAsset                           ,
            damageObservedDate       = damageData["damageObservedDate"      ],
            damageOccuredDate        = damageData["damageOccuredDate"       ],
            damageType               = damageData["damageType"              ],
            damageSeverity           = damageData["damageSeverity"          ],
            notes                    = damageData["notes"                   ],
            damageImage              = damageData["damageImage"             ],
            scheduledMaintenanceDate = damageData["scheduledMaintenanceDate"]
        )

        newRecord.save()

    def editDamageRecord(self, damageData, damageLogID):
        targetDamageRecord = Damage.objects.get(damageID=damageLogID)
        for key, value in damageData.items():
            setattr(targetDamageRecord, key, value)
        targetDamageRecord.save()

    def deleteDamageRecord(self, damageLogID):
        targetDamageRecord = Damage.objects.get(damageID=damageLogID)
        if targetDamageRecord.deleted != True:
            targetDamageRecord.deleted = True
            maintenanceRecord = self.getDamageMaintenanceRecord(damageLogID)\
            
            # If the damage record has been repaired, remove the link to the maintenance record.
            if maintenanceRecord is not None:
                maintenanceRecord.repairsCompleted = None
                maintenanceRecord.maintenanceType = 0
                maintenanceRecord.save()
            targetDamageRecord.save()

    # Check if damage on an asset has been repaired.    
    def checkDamageRepairedByID(self, MaintenanceID):
        return Maintenance.objects.filter(repairsCompleted=MaintenanceID).exists()

    def getDamageMaintenanceRecord(self, damageID):
        if (self.checkDamageRepairedByID(damageID)):
            return Maintenance.objects.get(repairsCompleted_id=damageID)
        else:
            return None

@login_required(login_url="login")
def retrieveDamageRecordByID(request, damageLogID):
    """
    Searches the Asset damage model based on a damage log ID provided as a parameter.

    Django Object Serialisation information obtained from documentation at: https://docs.djangoproject.com/en/5.0/topics/serialization/
        Django's serialization framework provides a mechanism for “translating” Django models into other formats.
        Usually these other formats will be text-based and used for sending Django data over a wire, 
        but it's possible for a serializer to handle any format.
        This function calls the serialiser object directly. This enables the image form data to be passed to the front end and autofilled.
    """

    try:
        completeRecord = Damage.objects.get(pk=damageLogID)
        data = model_to_dict(completeRecord)
        if completeRecord.damageImage:
            data["damageImage"] = completeRecord.damageImage.url
        return JsonResponse(data)
    except Damage.DoesNotExist:
        print("Damage Record Not Found")
        return JsonResponse({"error": "Damage Record Not Found"})
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)})
    
@login_required(login_url="login")
def get_maintenance_details(request, maintenance_id):
    # maintenance = Maintenance.objects.get(pk=maintenance_id)
    maintenanceManagerInstance = maintenanceManager()
    maintenance = maintenanceManagerInstance.retrieveMaintenanceRecordByID(maintenance_id)
    data = model_to_dict(maintenance)  # Converts the model instance to a dictionary
    data["completionDate"   ] = data["completionDate"   ].strftime("%d/%m/%Y")
    data["dateOfNextService"] = data["dateOfNextService"].strftime("%d/%m/%Y")
    return JsonResponse(data)

@login_required(login_url="login")
def viewMaintenance(request, assetCategory, assetID):
    maintenanceManagerInstance = maintenanceManager()
    assetManagerInstance = AssetManager()
    currentAsset = assetManagerInstance.retrieveAssetByID(assetCategory=assetCategory, currentUser=request.user, assetID=assetID)
    creationForm = forms.createMaintenanceForm(request.user, assetCategory, assetID)

    assetLabelMapper = {
        "SE": "Small Equipment",
        "LE": "Large Equipment",
        "LV": "Standard Vehicles",
        "HV": "Heavy Vehicles"
    }

    if request.method == "GET":
        maintenanceData = maintenanceManagerInstance.retrieveMaintenanceData(assetID, assetCategory)
        context = {
            "currentAsset"   : currentAsset,
            "maintenanceData": maintenanceData,
            "assetCategory"  : assetCategory,
            "creationForm"   : creationForm,
            "assetLabel"     : assetLabelMapper[assetCategory]
        }
        return render(request, "assetMaintenance/viewMaintenance.html", context)

    elif request.method == "POST":
        if "createMaintenance" in request.POST: # If the user is creating a new maintenance record
            creationFormPost = forms.createMaintenanceForm(request.user, assetCategory, assetID, request.POST)
            maintenanceData = maintenanceManagerInstance.retrieveMaintenanceData(assetID, assetCategory)

            if creationFormPost.is_valid():
                # Create a new maintenance record
                maintenanceManagerInstance.createMaintenanceRecord(creationFormPost.cleaned_data, assetCategory, assetID)
                context = {
                    "maintenanceData": maintenanceData,
                    "assetCategory"  : assetCategory,
                    "maintenanceForm": creationFormPost,
                    "assetLabel"     : assetLabelMapper[assetCategory]
                }
                # Redirect to the maintenance overview page with a success message
                messages.add_message(request, messages.SUCCESS, "Maintenance Record Added")
                return redirect(f"/asset/{assetCategory}/{assetID}/maintenance")
            else:
                # Return the form with the errors to the user without redirecting to ensure the user can see the errors
                context = {
                    "currentAsset"   : currentAsset,
                    "maintenanceData": maintenanceData,
                    "assetCategory"  : assetCategory,
                    "creationForm"   : creationFormPost,
                    "assetLabel"     : assetLabelMapper[assetCategory]
                }
                return render(request, "assetMaintenance/viewMaintenance.html", context)

    return render(request, "assetMaintenance/viewMaintenance.html", context)

@login_required(login_url="login")
def maintenanceDetails(request, assetCategory, assetID, maintenanceID):
    maintenanceManagerInstance = maintenanceManager()
    assetStrucutures           = AssetStructures()
    maintenanceRecord          = maintenanceManagerInstance.retrieveMaintenanceRecordByID(maintenanceID)
    currentAsset               = assetStrucutures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)
    print(maintenanceRecord)
    updateForm                 = forms.editMaintenanceForm(request.user, assetCategory, assetID, initial=maintenanceRecord)
    # updateForm.fields["maintenanceConductedBy"]
    if request.method == "GET":
        context = {
            "currentAsset"     : currentAsset,
            "maintenanceRecord": maintenanceRecord,
            "assetCategory"    : assetCategory,
            "form"             : updateForm
        }

        return render(request, "assetMaintenance/maintenanceDetails.html", context)
    
    elif request.method == "POST":
        if  "Update" in request.POST: # If the user is updating a maintenance record
            
            formPOST = forms.editMaintenanceForm(request.user, assetCategory, assetID, request.POST, request.FILES)

            if formPOST.is_valid():
                maintenanceManagerInstance.editMaintenanceData(maintenanceID, formPOST.cleaned_data) # Edit the maintenance record
                messages.add_message(request, messages.SUCCESS, "Maintenance Record Updated.")
                return redirect(f"/asset/{assetCategory}/{assetID}/maintenance/{maintenanceID}/details")
            else:
                context = {
                    "currentAsset"     : currentAsset,
                    "maintenanceRecord": maintenanceRecord,
                    "assetCategory"    : assetCategory,
                    "form"             : formPOST,
                    "error"            : formPOST.errors
                }
                return render(request, "assetMaintenance/maintenanceDetails.html", context)

        elif "delete" in request.POST:
            maintenanceManagerInstance.deleteMaintenanceData(maintenanceID)
            messages.add_message(request, messages.WARNING, "Maintenance Record Deleted")
            return redirect(f"/asset/{assetCategory}/{assetID}/maintenance")

    return render(request, "assetMaintenance/maintenanceDetails.html", context)

@login_required(login_url="login")
def deleteMaintenance(request, maintenanceID, assetCategory, assetID):
    maintenanceManagerInstance = maintenanceManager()
    maintenanceManagerInstance.deleteMaintenanceData(maintenanceID)
    messages.add_message(request, messages.WARNING, "Maintenance Record Deleted")

    return redirect(f"/asset/{assetCategory}/{assetID}/maintenance")

@login_required(login_url="login")
def viewDamage(request, assetCategory, assetID):
    damageManagerInstance = damageManager()
    assetStrucutures = AssetStructures()

    currentAsset = assetStrucutures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)
    creationForm = forms.createDamageForm(request.user, assetCategory, assetID)
    editForm = forms.editDamageForm(request.user, assetCategory, assetID)

    if request.method == "GET":
        damageData = damageManagerInstance.retrieveDamageData(assetID, assetCategory)
        context = {
            "currentAsset" : currentAsset,
            "damageData"   : damageData,
            "assetCategory": assetCategory,
            "editForm"     : editForm,
            "creationForm" : creationForm
        }

        return render(request, "assetMaintenance/viewDamage.html", context)

    elif request.method == "POST":
        creationFormPOST = forms.createDamageForm(request.user, assetCategory, assetID, request.POST, request.FILES)
        damageData = damageManagerInstance.retrieveDamageData(assetID, assetCategory)
        if creationFormPOST.is_valid():
            damageManagerInstance.createDamageRecord(creationFormPOST.cleaned_data, assetCategory, assetID)
            context = {
                "currentAsset" : currentAsset,
                "damageData"   : damageData,
                "assetCategory": assetCategory,
                "creationForm" : creationFormPOST
            }
            messages.add_message(request, messages.SUCCESS, "Damage Record Added")
            return redirect(f"/asset/{assetCategory}/{assetID}/damage")
        else:
            context = {
                "currentAsset" : currentAsset,
                "damageData"   : damageData,
                "assetCategory": assetCategory,
                "creationForm" : creationFormPOST,
                "error"        : creationFormPOST.errors
            }
            return render(request, "assetMaintenance/viewDamage.html", context)    

    return render(request, "assetMaintenance/viewDamage.html", context)

@login_required(login_url="login")
def damageDetails(request, assetCategory, assetID, damageID):
    damageManagerInstance = damageManager()
    assetStrucutures = AssetStructures()
    damageRecord = damageManagerInstance.retrieveDamageRecordByID(damageID)
    maintenanceRecord = damageManagerInstance.getDamageMaintenanceRecord(damageID)

    currentAsset = assetStrucutures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)
    form = forms.editDamageForm(initial=damageRecord)

    if request.method == "GET":
        context = {
            "currentAsset"     : currentAsset,
            "damageRecord"     : damageRecord,
            "assetCategory"    : assetCategory,
            "maintenanceRecord": maintenanceRecord,
            "form"             : form
        }

        return render(request, "assetMaintenance/damageDetails.html", context)

    elif request.method == "POST":
        if  "Update" in request.POST:
            formPOST = forms.editDamageForm(request.user, assetCategory, assetID, request.POST, request.FILES)
            if formPOST.is_valid():
                damageManagerInstance.editDamageRecord(formPOST.cleaned_data, damageID)
                messages.add_message(request, messages.SUCCESS, "Damage Record Updated.")
                return redirect(f"/asset/{assetCategory}/{assetID}/damage/{damageID}/details")
            else:
                context = {
                    "currentAsset"     : currentAsset,
                    "damageRecord"     : damageRecord,
                    "assetCategory"    : assetCategory,
                    "maintenanceRecord": maintenanceRecord,
                    "form"             : formPOST,
                    "error"            : formPOST.errors
            }
            return render(request, "assetMaintenance/damageDetails.html", context)

        elif "delete" in request.POST:
            damageManagerInstance.deleteDamageRecord(damageID)
            messages.add_message(request, messages.WARNING, "Damage Deleted")
            return redirect(f"/asset/{assetCategory}/{assetID}/damage")

    return render(request, "assetMaintenance/damageDetails.html", context)

@login_required(login_url="login")
def deleteDamage(request, damageID, assetCategory, assetID):
    damageManagerInstance = damageManager()
    damageManagerInstance.deleteDamageRecord(damageID)
    messages.add_message(request, messages.WARNING, "Damage Record Deleted")

    return redirect(f"/asset/{assetCategory}/{assetID}/damage")
