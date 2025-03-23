from django.shortcuts import render, redirect
from . import forms
from .models import Expense
from django.forms.models import model_to_dict
from assetManagement.views import AssetManager, AssetStructures
from assetMaintenance.views import maintenanceManager
from django.http import JsonResponse
from django.contrib import messages
from assetManagement.views import AssetStructures
from django.contrib.auth.decorators import login_required

class expensemanager():

    def retrieveExpenseByID(self, expenseID=None):
        try:
            return model_to_dict(Expense.objects.get(pk=expenseID))
        except Expense.DoesNotExist:
            return {"error": "Expense Record Not Found"}
        except Exception as e:
            return {"error": str(e)}

    def retrieveExpenseByAsset(self, AssetID=None):
        try:
            return Expense.objects.filter(assetID_id=AssetID, deleted=False)
        except Expense.DoesNotExist:
            return {"error": "Asset Record Not Found"}
        except Exception as e:
            return {"error": str(e)}

    def retrieveExpenseByMaintenanceRecord(self, MaintenanceID=None):
        try:
            return model_to_dict(Expense.objects.get(MaintenanceID=MaintenanceID))
        except Expense.DoesNotExist:
            return {"error": "maintenance Record Not Found"}
        except Exception as e:
            return {"error": str(e)}

    def retrieveAllExpenses(self):
        try:
            expenses = Expense.objects.all()
            expenseList = []
            for expense in expenses:
                expenseList.append(expense)
            return expenseList
        except Expense.DoesNotExist:
            return {"error": "No Expense Records Found"}
        except Exception as e:
            return {"error": str(e)}

    def createExpense(self, expenseData, assetCategory, assetID, UserProfile):
        assetmanager = AssetManager()
        maintenancemanager = maintenanceManager()
        assetStructures = AssetStructures()
        targetAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(assetID=assetID)
        try:
            if UserProfile is None or assetID is None:
                return {"error": "User Profile and Asset ID cannot be None"}
            elif expenseData.get("expenseType") == 1:
                targetMaintenanceCost = maintenancemanager().retrieveMaintenanceByID(expenseData.get("MaintenanceID")).get("cost")
                expense = Expense(
                    assetID         = targetAsset,
                    MaintenanceID   = expenseData["MaintenanceID"],
                    expenseType     = expenseData["expenseType"],
                    cost            = targetMaintenanceCost,
                    receiptNumber   = expenseData["receiptNumber"],
                    expenseLodgedBy = expenseData["expenseLodgedBy"]
                )
                expense.save()
                return model_to_dict(expense)
            else:
                expense = Expense(
                    assetID         = targetAsset,
                    MaintenanceID   = expenseData["MaintenanceID"],
                    expenseType     = expenseData["expenseType"],
                    cost            = expenseData["cost"],
                    receiptNumber   = expenseData["receiptNumber"],
                    expenseLodgedBy = expenseData["expenseLodgedBy"]
                )
                expense.save()
                return model_to_dict(expense)
        except Exception as e:
            return {"error": str(e)}

    def editExpense(self, expenseID, expenseData):
        try:
            targetExpense = Expense.objects.get(pk=expenseID)
            for key, value in expenseData.items():
                setattr(targetExpense, key, value)
            targetExpense.save()
        except Expense.DoesNotExist:
            return {"error": "Expense Record Not Found"}
        except Exception as e:
            return {"error": str(e)}

    def deleteExpense(self, expenseID):
        try:
            targetExpense = Expense.objects.get(pk=expenseID)
            setattr(targetExpense, "deleted", True)
            targetExpense.save()
        except Expense.DoesNotExist:
            return {"error": "Expense Record Not Found"}
        except Exception as e:
            return {"error": str(e)}


def get_expense_details(expenseID):
    return JsonResponse(model_to_dict(Expense.objects.get(pk=expenseID)))

@login_required(login_url="login")
def viewAllExpenses(request):
    expenseManagerInstance = expensemanager()
    expenseList = expenseManagerInstance.retrieveAllExpenses()
    context = {
        "expenseData": expenseList
    }
    return render(request, "assetExpenses/expenseList.html", context)

@login_required(login_url="login")
def viewExpenseForSingleAsset(request, assetCategory, assetID):
    expenseManagerInstance = expensemanager()
    assetStructures = AssetStructures()

    currentAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(pk=assetID)
    expenseCreationForm = forms.createExpenseForm(request.user, assetID)
    expenseEditForm = forms.editExpenseForm(request.user, assetID)

    if request.method == "GET":
        assetExpenses = expenseManagerInstance.retrieveExpenseByAsset(assetID)
        context = {
            "currentAsset" : currentAsset,
            "assetCategory": assetCategory,
            "expenseData"  : assetExpenses,
            "creationForm" : expenseCreationForm,
            "editForm"     : expenseEditForm
        }
        return render(request, "assetExpenses/viewExpenses.html", context)

    elif request.method == "POST":
        createExpenseFormPost = forms.createExpenseForm(request.user, assetID, request.POST)
        if createExpenseFormPost.is_valid(): 
            expenseManagerInstance.createExpense(createExpenseFormPost.cleaned_data, assetCategory, assetID, request.user)
            messages.add_message(request, messages.SUCCESS, "Expense Record Created")
            context = {
                "expenseData"  : expenseManagerInstance.retrieveExpenseByAsset(assetID),
                "assetCategory": assetCategory,
                "currentAsset" : currentAsset,
                "creationForm" : createExpenseFormPost,
            }
        else:
            context = {
                "expenseData"  : expenseManagerInstance.retrieveExpenseByAsset(assetID),
                "assetCategory": assetCategory,
                "currentAsset" : currentAsset,
                "creationForm" : createExpenseFormPost,
                "error"        : createExpenseFormPost.errors
            }
            return render(request, "assetExpenses/viewExpenses.html", context)
    return redirect(f'/asset/{assetCategory}/{assetID}/expenses')

@login_required(login_url="login")
def expenseDetails(request, expenseID, assetID=None, assetCategory=None):
    expenseManagerInstance = expensemanager()
    expenseRecord = expenseManagerInstance.retrieveExpenseByID(expenseID)
    currentAsset = None

    # This provides some level of robustness in the event that the assetID is not accesible from the URL.
    try:
        if assetID is None:
            assetID = expenseRecord.get("assetID")
            assetCategory = expenseRecord.get("assetCategory")
        else:
            assetStructures = AssetStructures()
            currentAsset = assetStructures.assetModelMapper.get(assetCategory).objects.get(pk=assetID)
    except Expense.DoesNotExist:
        return JsonResponse({"error": "Expense Record Not Found"})
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)})

    form = forms.editExpenseForm(request.user, assetID, initial=expenseRecord)

    if request.method == "GET":
        if assetID is not None:
            context = {
                "expenseData"  : expenseRecord,
                "currentAsset" : currentAsset,
                "assetCategory": assetCategory,
                "form"         : form,
            }
        else:
            context = {
                "expenseData"  : expenseRecord,
                "currentAsset" : expenseRecord.get("assetID"),
                "assetCategory": expenseRecord.get("assetID").get("assetCategory"),
                "form"         : form,
            }

        return render(request, "assetExpenses/expenseDetails.html", context)

    elif request.method == "POST":
        if "Update" in request.POST:
            editExpenseFormPost = forms.editExpenseForm(request.user, assetID, request.POST)
            if editExpenseFormPost.is_valid():
                expenseManagerInstance.editExpense(expenseID, editExpenseFormPost.cleaned_data)
                messages.add_message(request, messages.SUCCESS, "Expense Record Updated")
                return redirect(f'/asset/{assetCategory}/{assetID}/expenses/{expenseID}/details')
            else:
                context = {
                    "expenseData"  : expenseRecord,
                    "currentAsset" : currentAsset,
                    "assetCategory": assetCategory,
                    "form"         : editExpenseFormPost,
                    "error"        : editExpenseFormPost.errors
                }
                print(editExpenseFormPost.errors)

                return render(request, "assetExpenses/expenseDetails.html", context)

        elif "Delete" in request.POST:
            deleteExpense(request, expenseID, assetCategory, assetID)

    return redirect(f'/asset/{assetCategory}/{assetID}/expenses')

@login_required(login_url="login")
def deleteExpense(request, expenseID, assetCategory, assetID):
    expenseManagerInstance = expensemanager()
    expenseManagerInstance.deleteExpense(expenseID)
    messages.add_message(request, messages.WARNING, "Expense Record Deleted")
    return redirect(f'/asset/{assetCategory}/{assetID}/expenses')
