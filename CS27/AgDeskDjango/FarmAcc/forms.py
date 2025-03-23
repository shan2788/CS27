"""
Forms for farms and files
"""

# Imports
from django import forms
from .models import FarmInfo, FileRecord, FileCategory
from django.forms import ModelForm


# Farms
class JoinFarmForm(forms.Form):

    linking_code = forms.CharField(
        label  = "Linking Code:"                                 ,
        widget = forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model  = FarmInfo
        fields = ["linking_code"]


class NewFarm(ModelForm):

    states = {
        "QLD": "QLD",
        "NSW": "NSW",
        "VIC": "VIC",
        "TAS": "TAS",
        "SA" : "SA" ,
        "WA" : "WA" ,
        "NT" : "NT" ,
        "ACT": "ACT"
    }

    farm_name     = forms.CharField(max_length=100, label="Farm Name:")
    farm_street   = forms.CharField(max_length=100, label="Farm Street:")
    farm_state    = forms.ChoiceField(choices=states, label="State:", required=False)
    farm_postcode = forms.CharField(max_length=6, label="Farm Postcode:")
    farm_bio      = forms.CharField(max_length=500, label="Farm Bio:", widget=forms.Textarea)
    farm_image    = forms.ImageField(label="Farm Image:")

    class Meta:
        model = FarmInfo
        fields = [
            "farm_name"    ,
            "farm_street"  ,
            "farm_state"   ,
            "farm_postcode",
            "farm_bio"     ,
            "farm_image"
        ]


# Files
class UploadDocument(ModelForm):
    """
    The UploadDocument form is used for uploading files within the 'fileView' and 'editFile' views.
    It defines the required attributes (which need to be filled in) when uploading files to the
    application.
    """

    def __init__(self, *args, **kwargs):
        super(UploadDocument, self).__init__(*args, **kwargs)
        self.fields["fileCategory"].required = False
        self.fields["reviewDate"  ].label    = "Review Date"

    # Form Attributes
    file         = forms.FileField(allow_empty_file=True)
    reviewDate   = forms.DateField(widget=forms.SelectDateWidget)
    fileCategory = forms.ModelChoiceField(required=False, queryset=FileCategory.objects.all(), label="File Category")
    fileName     = forms.CharField(max_length=100, label="File Name")

    class Meta:
        # The model the Upload Document Form is derived from
        model  = FileRecord
        fields = [
            "fileName"    ,
            "reviewDate"  ,
            "file"        ,
            "fileCategory"
        ]


class AddFileCategory(ModelForm):
    """
    The add file category form is used to create a new file category within the application.
    """

    fileCategoryName = forms.CharField(max_length=100, label="File Category Name")

    class Meta:
        model = FileCategory
        fields = [
            "fileCategoryName",
        ]
