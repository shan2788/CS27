"""
Forms for the settings functionality.
"""

# Imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.utils import timezone, dateformat

from crispy_forms.helper import FormHelper

from .models import orgSettingsModel, internalTeamsModel

from FarmAcc.models import FarmInfo, LinkingCode
from UserAuth.models import UserProfile, SecurityGroup, user_farm


# Class
class orgSettingsForm(ModelForm):
    current_time = timezone.localtime(timezone.now())

    common_timezones = (
        ("Australia/Brisbane" , "Brisbane" ),
        ("Australia/Canberra" , "Canberra" ),
        ("Australia/Adelaide" , "Adelaide" ),
        ("Australia/Darwin"   , "Darwin"   ),
        ("Australia/Hobart"   , "Hobart"   ),
        ("Australia/Melbourne", "Melbourne"),
        ("Australia/Perth"    , "Perth"    ),
        ("Australia/Sydney"   , "Sydney"   ),
        ("Europe/Amsterdam"   , "Amsterdam")
    )

    #("F  j, Y, P", dateformat.format(current_time, "F  j, Y, P"))
    datetime_options = (
        ("F  j, Y, P" , "January 1, 2024, 12:00 p.m."        ),
        ("l jS, F Y P", "Saturday 1st, January 2024 12:00 PM"),
        ("l, jS F"    , "Saturday, 1st January"              ),
        ("jS F"       , "1st January"                        )
    )

    temperature_options = (
        ("Celsius"   , "Celsius (°C)"   ),
        ("Fahrenheit", "Fahrenheit (°F)"),
        ("Kelvin"    , "Kelvin (K)"     )
    )

    mass_options = (
        ("t" , "Tonnes (t)"    ),
        ("kg", "Kilograms (kg)"),
        ("g" , "Grams (g)"     )
    )

    area_options = (
        ("ha", "Hectares (ha)"     ),
        ("ac", "Acres (ac)"        ),
        ("m2", "Square Metres (m²)")
    )

    length_options = (
        ("km", "Kilometres (km)" ),
        ("m" , "Metres (m)"      ),
        ("cm", "Centimetres (cm)"),
        ("mm", "Millimetres (mm)")
    )

    timezone          = forms.ChoiceField(choices = common_timezones   , label = "Time zone"       , required = False)
    datetime_format   = forms.ChoiceField(choices = datetime_options   , label = "Date/Time format", required = False)
    temperature_label = forms.ChoiceField(choices = temperature_options, label = "Temperature"     , required = False)
    mass_label        = forms.ChoiceField(choices = mass_options       , label = "Mass"            , required = False)
    area_label        = forms.ChoiceField(choices = area_options       , label = "Area"            , required = False)
    length_label      = forms.ChoiceField(choices = length_options     , label = "Length"          , required = False)

    class Meta:
        model = orgSettingsModel
        fields = [
            "timezone"         ,
            "datetime_format"  ,
            "temperature_label",
            "mass_label"       ,
            "area_label"       ,
            "length_label"
        ]


class farmSettingsUpdate(ModelForm):
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

    farm_name     = forms.CharField(label = "Farm Name:", required = True)
    farm_street   = forms.CharField(label = "Street:", required = True)
    farm_state    = forms.ChoiceField(choices = states, label = "State:", required = True)
    farm_postcode = forms.CharField(label = "Postcode:", required = True)
    farm_bio      = forms.CharField(max_length=500, label="Farm Bio:", widget=forms.Textarea, required=False)
    farm_image    = forms.ImageField(label = "Image:")

    class Meta:
        model  = FarmInfo
        fields = [
            "farm_name"    ,
            "farm_street"  ,
            "farm_state"   ,
            "farm_postcode",
            "farm_bio"     ,
            "farm_image"
        ]


class UpdateProfileDetails(forms.ModelForm):
    first_name  = forms.CharField(max_length=150, label="First Name:"  )
    last_name   = forms.CharField(max_length=150, label="Last Name:"   )
    phoneNumber = forms.CharField(max_length=15 , label="Phone Number:")

    class Meta:
        model  = UserProfile
        fields = ["first_name", "last_name", "phoneNumber"]


class teamSettingsForm(ModelForm):
    """
    This form defines the attributes of a form which needs to be filled in
    within the context of an 'internalTeams' model.
    """

    # Override the ModelForm's '__init__' function to redefine the attributes of the
    # widget when injecting them into the Django Template
    def __init__(self, *args, **kwargs):

        queryset = kwargs.pop("queryset", None)

        super(teamSettingsForm, self).__init__(*args, **kwargs)

        if queryset is not None:
            self.fields["userList"].queryset = queryset

        # Update the attributes of the Fields to align with BootStrap's classes
        self.fields["teamName"       ].widget.attrs.update({"class": "form-control"})
        self.fields["teamDescription"].widget.attrs.update({"class": "form-control"})
        self.fields["active"         ].widget.attrs.update({"class": "form-check"  })
        self.fields["teamImage"      ].widget.attrs.update({"class": "custom-file" })

    # -- DEFINE ADDITIONAL FORM ATTRIBUTES -- #
    # Define a user list to enable users to be assigned to an internalTeam
    userList        = forms.ModelMultipleChoiceField(
        queryset = UserProfile.objects.none()  ,
        widget   = forms.CheckboxSelectMultiple,
        required = False, label="User List"
    )
    teamName        = forms.CharField(max_length=100 , label="Team Name"       )
    teamDescription = forms.CharField(max_length=1000, label="Team Description")
    active          = forms.BooleanField(label="Active")
    teamImage       = forms.FileInput()

    class Meta:
        model  = internalTeamsModel
        fields = ["teamName", "teamDescription", "active", "teamImage"]


class userDetailsForm(ModelForm):
    """
    This form defines the editable User Details which can be modified by a System Administrator.
    """

    # Override the ModelForm's '__init__' function to redefine the attributes of the
    # widget when injecting them into the Django Template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update the attributes of the Fields
        self.fields["jobTitle"       ].widget.attrs.update({"class": "form-control"})
        self.fields["workingLocation"].widget.attrs.update({"class": "form-control"})
        self.fields["role"           ].widget.attrs.update({"class": "form-control"})
        self.fields["is_active"      ].widget.attrs.update({"class": "form-check"  })

    # -- DEFINE ADDITIONAL FORM ATTRIBUTES -- #
    # Define a list to enable users to be ascribed to a specific security group
    groups          = forms.ModelMultipleChoiceField(
        queryset = SecurityGroup.objects.all()   ,
        widget   = forms.CheckboxSelectMultiple  ,
        required = False, label="Security Groups"
    )
    jobTitle        = forms.CharField(max_length=30 , label="Job Title"       , required=False)
    workingLocation = forms.CharField(max_length=300, label="Working Location", required=False)
    role            = forms.CharField(max_length=200, label="Role"            , required=False)
    is_active       = forms.BooleanField(             label="Active?"         , required=False)

    class Meta:
        model  = user_farm
        fields = [
            "jobTitle"       ,
            "workingLocation",
            "role"           ,
            "is_active"
        ]


class linkingCodeForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["linkingCode"].widget.attrs.update({"class": "form-control"})

    linkingCode = forms.CharField(max_length=15, label="Linking Code")

    class Meta:
        model  = LinkingCode
        fields = ["linkingCode"]
