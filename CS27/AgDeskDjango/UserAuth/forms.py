"""
Forms for UserAuth.
"""

# Imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from UserAuth.models import UserProfile


class SignUserUpForm(UserCreationForm):
    """
    The SignUserUpForm is used to create a new user within the Django application.
    """

    # Override the ModelForm's '__init__' function to redefine the attributes of the
    # widget when injecting them into the Django Template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update the attributes of the Fields
        self.fields["username"   ].widget.attrs.update({"class": "form-control"})
        self.fields["email"      ].widget.attrs.update({"class": "form-control"})
        self.fields["password1"  ].widget.attrs.update({"class": "form-control"})
        self.fields["password2"  ].widget.attrs.update({"class": "form-control"})
        self.fields["first_name" ].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"  ].widget.attrs.update({"class": "form-control"})
        self.fields["phoneNumber"].widget.attrs.update({"class": "form-control"})

    username    = forms.CharField( max_length=150,                           widget=forms.TextInput(    attrs={"class": "form-control"}))
    email       = forms.EmailField(max_length=254,                           widget=forms.EmailInput(   attrs={"class": "form-control"}))
    password1   = forms.CharField( max_length=128, label="Password"        , widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2   = forms.CharField( max_length=128, label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name  = forms.CharField( max_length=30 , label="First Name"      , widget=forms.TextInput(    attrs={"class": "form-control"}))
    last_name   = forms.CharField( max_length=150, label="Last Name"       , widget=forms.TextInput(    attrs={"class": "form-control"}))
    phoneNumber = forms.CharField( max_length=10 , label="Phone Number"    , widget=forms.TextInput(    attrs={"class": "form-control"}))

    class Meta:
        model  = UserProfile
        fields = [
            "username"   ,
            "email"      ,
            "password1"  ,
            "password2"  ,
            "first_name" ,
            "last_name"  ,
            "phoneNumber"
        ]


class UserLoginForm(forms.Form):
    """
    Define the UserLoginForm users fill out when being authenticated with the application.
    """

    username = forms.CharField(max_length=150, widget=forms.TextInput(    attrs={"class": "form-control"}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={"class": "form-control"}))
