from django.forms import ModelForm, HiddenInput
from django import forms

from .models import FarmContacts, ContactInfo


# FarmContacts Forms
class createContactForm(ModelForm):

    contact_name = forms.CharField(label="Name", max_length=64)
    contact_desc = forms.CharField(
        label="Description",
        max_length=128,
        widget=forms.Textarea(attrs={"cols": 40, "rows": 6}),
        required=False
    )
    image = forms.ImageField(
        label="Image",
        required=False,widget=forms.FileInput(attrs={'class': 'form-control'}),
        initial="images/contact_images/defaultImage.png"
    )

    class Meta:
        model  = FarmContacts
        fields = ["contact_name", "contact_desc", "image"]

class updateContactForm(ModelForm):
    class Meta:
        model  = FarmContacts
        fields = ["farmContactID", "name", "desc", "image"]


# ContactInfo Forms
class createFieldForm(ModelForm):
    contact_method = forms.ChoiceField(label="Contact Method", choices=ContactInfo.FIELD_CHOICES)
    contact_info   = forms.CharField(label="Contact Information", max_length=64, required=True)

    class Meta:
        model  = ContactInfo
        fields = ["contact_method", "contact_info"]

class updateFieldForm(ModelForm):
    contact_method  = forms.ChoiceField(label="Contact Method", choices=ContactInfo.FIELD_CHOICES)
    contact_info    = forms.CharField(label="Contact Information", max_length=64)
    contact_info_id = forms.IntegerField(widget=HiddenInput())

    class Meta:
        model  = ContactInfo
        fields = ["contact_method", "contact_info", "contact_info_id"]
