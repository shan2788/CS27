"""
Forms required for the check out check in system, the operation logs, and the performance metrics.
"""

# Imports
from django.forms import ModelForm, HiddenInput
from django import forms

from .models import OperationLog#, PerformanceMetric, OperationLogMetric
from .models import LOG_LOCATION_LENGTH, LOG_NOTES_LENGTH


# Constants
LOG_NOTES_LABEL = "Notes (Optional)" # Change once, change everywhere


# Check Out Check In Forms
class checkOutForm(ModelForm):
    """
    Form for checking out an asset.
    assetID/Prefix to map to the correct foreign key.
    The view will also populate userID and startDateTime.
    """

    class Meta:
        model  = OperationLog
        fields = ["assetID", "location", "notes"]

    assetID     = forms.IntegerField(label="assetID"   , widget=HiddenInput())
    location    = forms.CharField(   label="Location"  , widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=LOG_LOCATION_LENGTH)
    notes       = forms.CharField(   label=LOG_NOTES_LABEL , widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}), required=False, max_length=LOG_NOTES_LENGTH)


class checkInForm(ModelForm):
    """
    Form for checking back in an asset.
    logID to update the correct log to its final state.
    The view will also populate endDateTime.
    """

    class Meta:
        model  = OperationLog
        fields = ["logID", "notes"]

    logID = forms.IntegerField(widget=HiddenInput())
    notes = forms.CharField(label=LOG_NOTES_LABEL, widget=forms.Textarea(attrs={"cols": 40, "rows": 6, 'class': 'form-control'}), required=False, max_length=LOG_NOTES_LENGTH)


# Operation Log Forms
# later


# Performance Metric Forms
# later
