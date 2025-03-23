"""
Dashboard forms.
"""


# Imports
from django import forms

# Widgets
WIDGET_CHOICES = [
    ('My Checkouts', 'My Checkouts'),
    ('My Tasks', 'My Tasks'),
    ('Weather (Small)', 'Weather (Small)'),
    ('Weekly Weather Forecast', 'Weekly Weather Forecast')
]


class addWidgetForm(forms.Form):
    """
    This form is used to add a new widget to the dashboard.
    """

    widget_name = forms.ChoiceField(choices=WIDGET_CHOICES, label="Widget Name")


class myTasksDateForm(forms.Form):
    """
    This form is used to filter the tasks by date.
    """

    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={'type': 'date'}))
