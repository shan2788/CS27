from django import forms
from django.forms import ModelForm
from . import models
from  .models import Maintenance
from .models import Expense
from assetMaintenance.models import Damage
from assetManagement.models import asset
from UserAuth.models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit,Row, Column, Div, HTML
from crispy_forms.bootstrap import Modal,StrictButton,PrependedText

class createExpenseForm(ModelForm):
    def __init__(self, user=None, assetID=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "expenseType", "expenseLodgedBy", PrependedText("cost", '$'),  "receiptNumber", "MaintenanceID",
            StrictButton("Close", css_class="btn btn-secondary float-left", data_bs_dismiss="modal", onclick="closeModal()"),
            StrictButton("Add Expense", type="submit", name="createExpense", css_class="btn custom-button float-right")
        )

        if user is not None:
            currentlyLoggedIn = UserProfile.objects.get(username=user)
            currentFarmID = currentlyLoggedIn.currentFarm_id

            self.fields["expenseType"].widget.attrs.update({"class": "form-control"})
            self.fields["MaintenanceID"].queryset = Maintenance.objects.filter(assetID=assetID, deleted=False)
            self.fields["cost"].widget.attrs.update({"class": "form-control"})
            self.fields["receiptNumber"].widget.attrs.update({"class": "form-control"})
            self.fields["expenseLodgedBy"].queryset = UserProfile.objects.filter(currentFarm_id =currentFarmID, is_active=True)

    EXPENSE_TYPE_CHOICES = [
        (0, "Fuel"),
        (1, "Maintenance"),
        (2, "Insurance"),
        (3, "Registration"),
        (4, "Other")
    ]

    expenseType     = forms.ChoiceField(choices=EXPENSE_TYPE_CHOICES, label="Expense Type", widget=forms.Select(attrs={"class": "form-control"}))
    MaintenanceID   = forms.ModelChoiceField(label="Maintenance Completed", help_text="Link this expense to an existing Maintenance record", queryset=Maintenance.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    cost            = forms.DecimalField(max_digits=10, decimal_places=2, label="Cost ($)", widget=forms.NumberInput(attrs={"class": "form-control"}))
    receiptNumber   = forms.IntegerField(label="Receipt Number", widget=forms.NumberInput(attrs={"class": "form-control"}))
    expenseLodgedBy = forms.ModelChoiceField(label="Lodged By", queryset=UserProfile.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data    = super().clean()
        cost            = cleaned_data.get("cost")
        MaintenanceID   = cleaned_data.get("MaintenanceID")
        maintenanceType = cleaned_data.get("expenseType")
        receiptNumber   = cleaned_data.get("receiptNumber")

        if cost is None or cost <= 0:
            self._errors["cost"] = self.error_class(["Cost must be greater than 0"])

        if receiptNumber is None or receiptNumber < 0 :
            self._errors["receiptNumber"] = self.error_class(["Receipt Number must be greater than 0"])

        # User should not get this. However, this provides robustness in edge cases.
        if MaintenanceID is not None:
            maintenance = Maintenance.objects.get(pk=MaintenanceID.pk)
            if maintenance.deleted:
                self._errors["MaintenanceID"] = self.error_class(["Maintenance record has been deleted."])

        if maintenanceType == '1' and MaintenanceID is None :
            self._errors["MaintenanceID"] = self.error_class(["Maintenance record must be selected for Maintenance expense"])

        if maintenanceType != '1' and MaintenanceID is not None:
            self._errors["MaintenanceID"] = self.error_class(["Maintenance record can only be selected for Maintenance expense"])

        if not super().is_valid():
            raise forms.ValidationError("Please correct the errors below and resubmit the form.")

        return cleaned_data

    class Meta:
        model = Expense
        fields = [
            "expenseType", 
            "MaintenanceID", 
            "cost",
            "receiptNumber",
            "expenseLodgedBy"
        ]

class editExpenseForm(ModelForm):
    def __init__(self, user=None, assetID=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    "expenseID", "expenseType", "expenseLodgedBy", PrependedText("cost", '$'),  "receiptNumber", "MaintenanceID",
                StrictButton("Update", type="submit", name="Update", css_class="btn custom-button"),
                StrictButton("Delete", type="submit", name="Delete", css_class="btn btn-danger"),

                css_class="form-group col-md-6 mb-0")
            )
        )

        if user is not None:
            currentlyLoggedIn = UserProfile.objects.get(username=user)
            currentFarmID = currentlyLoggedIn.currentFarm_id

            self.fields["expenseID"].widget.attrs.update({"class": "form-control"})
            self.fields["expenseType"].widget.attrs.update({"class": "form-control"})
            self.fields["MaintenanceID"].queryset = Maintenance.objects.filter(assetID=assetID, deleted=False)
            self.fields["cost"].widget.attrs.update({"class": "form-control"})
            self.fields["receiptNumber"].widget.attrs.update({"class": "form-control"})
            self.fields["expenseLodgedBy"].queryset = UserProfile.objects.filter(currentFarm_id=currentFarmID)

    EXPENSE_TYPE_CHOICES = [
        (0, "Fuel"),
        (1, "Maintenance"),
        (2, "Insurance"),
        (3, "Registration"),
        (4, "Other")
    ]
    expenseID = forms.IntegerField(widget=forms.HiddenInput())
    expenseType = forms.ChoiceField(choices=EXPENSE_TYPE_CHOICES, label="Expense Type", widget=forms.Select(attrs={"class": "form-control"}))
    MaintenanceID = forms.ModelChoiceField(label="Maintenance Completed", help_text="Maintenance record associated with this Expense",queryset=Maintenance.objects.all(), widget=forms.Select(attrs={"class": "form-control"}), required=False)
    cost = forms.DecimalField(max_digits=10, decimal_places=2, label="Cost ($)", widget=forms.NumberInput(attrs={"class": "form-control"}))
    receiptNumber = forms.IntegerField(label="Receipt Number", widget=forms.NumberInput(attrs={"class": "form-control"}))
    expenseLodgedBy = forms.ModelChoiceField(label="Lodged By", queryset=UserProfile.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data    = super().clean()
        cost            = cleaned_data.get("cost")
        MaintenanceID   = cleaned_data.get("MaintenanceID")
        maintenanceType = cleaned_data.get("expenseType")
        receiptNumber   = cleaned_data.get("receiptNumber")

        if cost is None or cost <= 0:
            self._errors["cost"] = self.error_class(["Cost must be greater than 0"])

        if receiptNumber is None or receiptNumber < 0 :
            self._errors["receiptNumber"] = self.error_class(["Receipt Number must be greater than 0"])

        # User should not get this. However, this provides robustness in edge cases.
        if MaintenanceID is not None:
            maintenance = Maintenance.objects.get(pk=MaintenanceID.pk)
            if maintenance.deleted:
                self._errors["MaintenanceID"] = self.error_class(["Maintenance record has been deleted."])

        if maintenanceType == '1' and MaintenanceID is None :
            self._errors["MaintenanceID"] = self.error_class(["Maintenance record must be selected for Maintenance expense"])

        if maintenanceType != '1' and MaintenanceID is not None:
            self._errors["MaintenanceID"] = self.error_class(["Maintenance record can only be selected for Maintenance expense"])

        if not super().is_valid():
            raise forms.ValidationError("Please correct the errors below and resubmit the form.")

        return cleaned_data

    class Meta:
        model = Expense
        fields = [
            "expenseID",
            "expenseType", 
            "MaintenanceID", 
            "cost",
            "receiptNumber",
            "expenseLodgedBy"
        ]
