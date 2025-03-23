import datetime
from django import forms
from django.forms import ModelForm
from .models import *
from UserAuth.models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit,Row, Column, Div, HTML
from crispy_forms.bootstrap import Modal,StrictButton,PrependedText


# These class fields still need to get the currently logged in user.
class createSmallAssetForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'assetName'   ,
            Row(
                Column('Manufacturer'    , css_class='form-group col-md-6 mb-0'),
                Column('assetImage'      , css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column('dateManufactured', css_class='form-group col-md-6 mb-0'),
                Column('datePurchased'   , css_class='form-group col-md-6 mb-0')
            ),
            'Location'    ,
            'serialNumber',
            'partsList'   ,
            StrictButton("Close"         , css_class="btn btn-secondary float-left" , data_bs_dismiss="modal", onclick="closeModal()"),
            StrictButton("Create Asset"  , css_class="btn custom-button float-right", type="submit")
        )

        if user is not None:
            self.fields["assetName"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"   ].widget.attrs.update({"class": "form-control"})
            self.fields["serialNumber"    ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"    ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"       ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"        ].widget.attrs.update({"class": "form-control"})
            self.fields["assetImage"      ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    serialNumber = forms.CharField(max_length=100, label="Serial Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    assetImage = forms.ImageField(label="Image", required=False, initial=r"images/asset_images/defaultImage.jpg")

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')
                
        if datePurchased != None and datePurchased > datetime.date.today():
                self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')


        return cleaned_data

    class Meta:
        model = SmallEquipment
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'serialNumber',
            'Manufacturer',
            'partsList',
            'Location',
            'assetImage'
        ]


class createLargeAssetForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'assetName',
            Row(
                Column('Manufacturer'    , css_class='form-group col-md-6 mb-0'),
                Column('assetImage'      , css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column('dateManufactured', css_class='form-group col-md-6 mb-0'),
                Column('datePurchased'   , css_class='form-group col-md-6 mb-0')
            ),
            'Location' ,
            'vin'      ,
            'partsList',
            StrictButton("Close"         , css_class="btn btn-secondary float-left" , data_bs_dismiss="modal", onclick="closeModal()"),
            StrictButton("Create Asset"  , css_class="btn custom-button float-right", type="submit")
        )

        if user is not None:
            self.fields["assetName"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"   ].widget.attrs.update({"class": "form-control"})
            self.fields["vin"             ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"    ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"       ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"        ].widget.attrs.update({"class": "form-control"})
            self.fields["assetImage"      ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    vin = forms.CharField(max_length=17, min_length=17,label="VIN Number", widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'invalid': 'Enter a valid VIN number'})
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    assetImage = forms.ImageField(label="Image", required=False, initial=r"images/asset_images/defaultImage.jpg")

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')
                
        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')


        return cleaned_data

    class Meta:
        model = LargeEquipment
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'vin',
            'Manufacturer',
            'partsList',
            'Location',
            'assetImage'
        ]

class createLightVehicleForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'assetName'     ,
            Row(
                Column('Manufacturer'    , css_class='form-group col-md-6 mb-0'),
                Column('assetImage'      , css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column('dateManufactured', css_class='form-group col-md-6 mb-0'),
                Column('datePurchased'   , css_class='form-group col-md-6 mb-0')
            ),
            'Location'      ,
            Row(
                Column('vin'             , css_class='form-group col-md-6 mb-0'),
                Column('Registration'    , css_class='form-group col-md-6 mb-0')
            ),
            'partsList'     ,
            'currentlyInUse',
            StrictButton("Close"         , css_class="btn btn-secondary float-left" , data_bs_dismiss="modal", onclick="closeModal()"),
            StrictButton("Create Asset"  , css_class="btn custom-button float-right", type="submit")
        )

        if user is not None:
            self.fields["assetName"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"   ].widget.attrs.update({"class": "form-control"})
            self.fields["vin"             ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"    ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"       ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"        ].widget.attrs.update({"class": "form-control"})
            self.fields["currentlyInUse"  ].widget.attrs.update({"class": "form-control"})
            self.fields["assetImage"      ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    vin = forms.CharField(max_length=17, min_length=17,label="VIN Number", widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'invalid': 'Enter a valid VIN number'})
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Registration = forms.CharField(max_length=100, label="Registration", widget=forms.TextInput(attrs={'class': 'form-control'}))
    currentlyInUse = forms.BooleanField(label="Currently In Use", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    assetImage = forms.ImageField(label="Image", required=False, initial=r"images/asset_images/defaultImage.jpg")

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')

        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')


        return cleaned_data

    class Meta:
        model = lightVehicle
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'vin',
            'Manufacturer',
            'partsList',
            'Location',
            'Registration',
            'currentlyInUse',
            'assetImage'
        ]


class createHeavyVehicleForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'assetName',
            Row(
                Column('Manufacturer'      , css_class='form-group col-md-6 mb-0'),
                Column('assetImage'        , css_class='form-group col-md-6 mb-0')
            ),
            Row(
                Column('dateManufactured'  , css_class='form-group col-md-6 mb-0'),
                Column('datePurchased'     , css_class='form-group col-md-6 mb-0')
            ),
            'Location' ,
            Row(
                Column('vin'               , css_class='form-group col-md-6 mb-0'),
                Column('Registration'      , css_class='form-group col-md-6 mb-0')
            ),
            'partsList',
            Row(
                Column('inTransport'       , css_class='form-group col-md-6 mb-0'),
                Column('interFarmTransport', css_class='form-group col-md-6 mb-0')
            ),
            StrictButton("Close"           , css_class="btn btn-secondary float-left" , data_bs_dismiss="modal", onclick="closeModal()"),
            StrictButton("Create Asset"    , css_class="btn custom-button float-right", type="submit")
        )

        if user is not None:
            self.fields["assetName"         ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"  ].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"     ].widget.attrs.update({"class": "form-control"})
            self.fields["vin"               ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"      ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"         ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"          ].widget.attrs.update({"class": "form-control"})
            self.fields["inTransport"       ].widget.attrs.update({"class": "form-check"})
            self.fields["interFarmTransport"].widget.attrs.update({"class": "form-check"})
            self.fields["assetImage"        ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    vin = forms.CharField(max_length=17, min_length=17,label="VIN Number", widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'invalid': 'Enter a valid VIN number'})
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Registration = forms.CharField(max_length=100, label="Registration", widget=forms.TextInput(attrs={'class': 'form-control'}))
    inTransport = forms.BooleanField(label="Currently In Use", required=False)
    interFarmTransport = forms.BooleanField(label="Inter-Farm Transport", required=False)
    assetImage = forms.ImageField(label="Image", required=False, initial=r"images/asset_images/defaultImage.jpg")

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')

        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')

        return cleaned_data

    class Meta:
        model = heavyVehicle
        fields = [
            'assetName',
            'dateManufactured',
            'dateManufactured',
            'datePurchased',
            'vin',
            'Manufacturer',
            'partsList',
            'Location',
            'Registration',
            'inTransport',
            'interFarmTransport',
            'assetImage'
        ]


# The below are editing forms - I don't believe these are needed at the moment however writing them now and not using them saves
# writing them later.

class editSmallAssetForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'assetName','Manufacturer', 'serialNumber', 'dateManufactured', 'datePurchased', 'Location',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    css_class='form-group col-md-2 mb-0'),
                Column(
                    Div(HTML('<img src="{{ currentAsset.assetImage.url }}" style="width: 200px; height: 200px;">'), css_class='text-right'),
                    Div('assetImage', 'partsList'),
                    css_class='form-group col-md-4 mb-0')
            ),
            StrictButton("Update", type="submit", name='Update', css_class="btn custom-button"),
            StrictButton("Delete", type="submit", name='delete', css_class="btn btn-danger"   )
        )

        if user is not None:
            self.fields["assetName"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"   ].widget.attrs.update({"class": "form-control"})
            self.fields["serialNumber"    ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"    ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"       ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"        ].widget.attrs.update({"class": "form-control"})
            self.fields["assetImage"      ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    serialNumber = forms.CharField(max_length=100, label="Serial Number", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    assetImage = forms.ImageField(label="Update Image", required=False)

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')

        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')


        return cleaned_data

    class Meta:
        model = SmallEquipment
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'serialNumber',
            'Manufacturer',
            'partsList',
            'Location',
            'assetImage'
        ]

class editLargeAssetForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'assetName','Manufacturer', 'vin', 'dateManufactured','datePurchased', 'Location',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    css_class='form-group col-md-2 mb-0'),
                Column(
                    Div(HTML('<img src="{{ currentAsset.assetImage.url }}" style="width: 200px; height: 200px;">'), css_class='text-right'),
                    Div('assetImage', 'partsList'),
                    css_class='form-group col-md-4 mb-0')
            ),
            StrictButton("Update", type="submit", name='Update', css_class="btn custom-button"),
            StrictButton("Delete", type="submit", name='delete', css_class="btn btn-danger"   )
        )

        if user is not None:
            self.fields["assetName"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"   ].widget.attrs.update({"class": "form-control"})
            self.fields["vin"             ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"    ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"       ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"        ].widget.attrs.update({"class": "form-control"})
            self.fields["assetImage"      ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    vin = forms.CharField(max_length=17, min_length=17,label="VIN Number", widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'invalid': 'Enter a valid VIN number'})
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    assetImage = forms.ImageField(label="Update Image", required=False)

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')
                
        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')

        return cleaned_data

    class Meta:
        model = LargeEquipment
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'vin',
            'Manufacturer',
            'partsList',
            'Location',
            'assetImage'
        ]


class editLightVehicleForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'assetName','Manufacturer', 'vin', 'Registration','dateManufactured', 'datePurchased', 'Location',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    css_class='form-group col-md-2 mb-0 text-center'),
                Column(
                    Div(HTML('<img src="{{ currentAsset.assetImage.url }}" style="width: 200px; height: 200px;">'), css_class='text-right'),
                    Div('assetImage', 'partsList','currentlyInUse'),                      
                    css_class='form-group col-md-4 mb-0')
            ),
            StrictButton("Update", type="submit" ,name='Update', css_class="btn custom-button"),
            StrictButton("Delete", type="submit", name='delete', css_class="btn btn-danger"   )
        )

        if user is not None:
            currentlyLoggedIn = UserProfile.objects.get(username = user)
            currentFarmID = currentlyLoggedIn.currentFarm_id
            self.fields["assetName"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"   ].widget.attrs.update({"class": "form-control"})
            self.fields["vin"             ].widget.attrs.update({"class": "form-control"})
            self.fields["Registration"    ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"    ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"       ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"        ].widget.attrs.update({"class": "form-control"})
            self.fields["currentlyInUse"  ].widget.attrs.update({"class": "form-check"  })
            self.fields["assetImage"      ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    vin = forms.CharField(max_length=17, min_length=17,label="VIN Number", widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'invalid': 'Enter a valid VIN number'})
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Registration = forms.CharField(max_length=100, label="Registration", widget=forms.TextInput(attrs={'class': 'form-control'}))
    currentlyInUse = forms.BooleanField(label="Currently In Use", required=False)
    assetImage = forms.ImageField(label="Update Image", required=False)

    def clean(self):
        cleaned_data = super().clean()
        dateManufactured = cleaned_data.get('dateManufactured')
        datePurchased = cleaned_data.get('datePurchased')
                
        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')


        return cleaned_data

    class Meta:
        model = lightVehicle
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'vin',
            'Manufacturer',
            'partsList',
            'Location',
            'Registration',
            'currentlyInUse',
            'assetImage'
        ]


class editHeavyVehicleForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    'assetName','Manufacturer', 'Registration','vin','dateManufactured', 'datePurchased', 'Location',
                    css_class='form-group col-md-6 mb-0'),
                Column(
                    css_class='form-group col-md-2 mb-0'),
                Column(
                    Div(HTML('<img src="{{ currentAsset.assetImage.url }}" style="width: 200px; height: 200px;">'), css_class='text-right'),
                    Div('assetImage', 'partsList','inTransport','interFarmTransport'),
                    css_class='form-group col-md-4 mb-0')
            ),
            StrictButton("Update", type="submit", name='Update', css_class="btn custom-button"),
            StrictButton("Delete", type="submit", name='delete', css_class="btn btn-danger"   )
        )

        if user is not None:
            currentlyLoggedIn = UserProfile.objects.get(username = user)
            currentFarmID = currentlyLoggedIn.currentFarm_id
            self.fields["assetName"         ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["dateManufactured"  ].widget.attrs.update({"class": "form-control"})
            self.fields["datePurchased"     ].widget.attrs.update({"class": "form-control"})
            self.fields["vin"               ].widget.attrs.update({"class": "form-control"})
            self.fields["Registration"      ].widget.attrs.update({"class": "form-control"})
            self.fields["Manufacturer"      ].widget.attrs.update({"class": "form-control"})
            self.fields["partsList"         ].widget.attrs.update({"class": "form-control"})
            self.fields["Location"          ].widget.attrs.update({"class": "form-control"})
            self.fields["inTransport"       ].widget.attrs.update({"class": "form-check"  })
            self.fields["interFarmTransport"].widget.attrs.update({"class": "form-check"  })
            self.fields["assetImage"        ].widget.attrs.update({"class": "form-control"})

    assetName = forms.CharField(max_length=100, label="Asset Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateManufactured = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Manufactured", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                       error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    datePurchased = forms.DateField(input_formats=["%d/%m/%Y"], label="Date Purchased", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}),
                                    error_messages={'invalid': 'Enter a valid date in the format DD/MM/YYYY'})
    vin = forms.CharField(max_length=17, min_length=17, label="VIN Number", widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={'invalid': 'Enter a valid VIN number'})
    Manufacturer = forms.CharField(max_length=100, label="Manufacturer", widget=forms.TextInput(attrs={'class': 'form-control'}))
    partsList = forms.CharField(max_length=255, label="Parts List", widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}))
    Location = forms.CharField(max_length=100, label="Location", widget=forms.TextInput(attrs={'class': 'form-control'}))
    Registration = forms.CharField(max_length=100, label="Registration", widget=forms.TextInput(attrs={'class': 'form-control'}))
    inTransport = forms.BooleanField(label="Currently In Use", required=False),
    interFarmTransport = forms.BooleanField(label="Currently In Use", required=False)
    assetImage = forms.ImageField(label="Update Image", required=False)

    def clean(self):
        cleaned_data = super().clean()
        datePurchased = cleaned_data.get('datePurchased')
        
        if datePurchased != None and datePurchased > datetime.date.today():
            self._errors["datePurchased"] = ["Date Purchased cannot be in the future."]

        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')

        return cleaned_data

    class Meta:
        model = heavyVehicle
        fields = [
            'assetName',
            'dateManufactured',
            'datePurchased',
            'vin',
            'Manufacturer',
            'partsList',
            'Location',
            'Registration',
            'inTransport',
            'interFarmTransport',
            'assetImage'
        ]
