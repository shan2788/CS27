"""
Forms for working with tasks and kanban boards.
"""

# Imports
from django import forms
from django.forms import ModelForm, Form, formset_factory
from UserAuth.models import UserProfile
from .models import Task, Kanban, KanbanContents
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit,Row, Column, Div, HTML
from crispy_forms.bootstrap import Modal,StrictButton,PrependedText
import datetime



# Tasks
# TODO: Rewrite
class createTaskForm(ModelForm):
    """
    Enables the User to add a new task to the database.
    New Tasks are automatically assigned to the user that creates them.
    The Status is set to not started by default.
    """

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("name",         css_class='form-group col-12')),
            Row(Column("description",  css_class='form-group col-12')),
            Row(Column("assignedTo",   css_class='form-group col-12')),
            Row(Column("status",       css_class='form-group col-12')),
            Row(Column("priority",     css_class='form-group col-12')),
            Row(Column("dueDate",      css_class='form-group col-12')),
            StrictButton("Create Task", type="submit", name='createTask',css_class="btn custom-button float-left")
        )
            
        
        if user is not None:
            currentlyLoggedIn = UserProfile.objects.get(username = user)
            currentFarmID = currentlyLoggedIn.currentFarm_id

            self.fields["name"       ].widget.attrs.update({"class": "form-control"})
            self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 3})
            self.fields["assignedTo" ].queryset = UserProfile.objects.filter(currentFarm = currentFarmID, is_active = True)
            self.fields["status"     ].widget.attrs.update({"class": "form-control"})
            self.fields["priority"   ].widget.attrs.update({"class": "form-control"})
            self.fields["dueDate"    ].widget.attrs.update({"class": "form-control"})

    TASK_STATUS_CHOICES = [ # Database stores status as int so we can iterate over buckets later.
        (0, "Not Started"),
        (1, "In Progress"),
        (2, "Blocked"    ),
        (3, "Review"     ),
        (4, "Complete"   ),
        (5, "Archived"   )
    ]

    TASK_PRIORITY_CHOICES = [
        (0,"Low"),
        (1,"Medium"),
        (2,"High"),
        (3,"Urgent"),
    ]

    name        = forms.CharField(max_length=100, label="Task Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=200, label="Task Description", required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    assignedTo  = forms.ModelChoiceField(label="Assigned To", queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    status      = forms.ChoiceField(choices = TASK_STATUS_CHOICES, label="Task Status",  widget=forms.Select(attrs={'class': 'form-control'}))
    priority    = forms.ChoiceField(choices = TASK_PRIORITY_CHOICES, label="Task Priority", widget=forms.Select(attrs={'class': 'form-control'}))
    dueDate     = forms.DateField(input_formats=["%d/%m/%Y"], label="Task Due Date", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}))

    def clean(self):
        cleaned_data = super().clean()
        dueDate = cleaned_data.get('dueDate')

        if dueDate != None and dueDate < datetime.date.today():
            self._errors["dueDate"] = ["Due Date cannot be in the past."]
            
        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')

        return cleaned_data

    class Meta:
        model = Task
        fields = [
            'name'       ,
            'description',
            'assignedTo' ,
            'status'     ,
            'priority'   ,
            'dueDate'
        ]


class taskForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column("name",         css_class='form-group col-12')),
            Row(Column("description",  css_class='form-group col-12')),
            Row(Column("assignedTo",   css_class='form-group col-12')),
            Row(Column("status",       css_class='form-group col-12')),
            Row(Column("priority",     css_class='form-group col-12')),
            Row(Column("dueDate",      css_class='form-group col-12')),
            StrictButton("Update Task", type="submit", name='updateTask',css_class="btn custom-button float-left"),
            StrictButton("Delete Task", type="submit", name='deleteTask',css_class="btn btn-danger float-right")

        )
        
        if user is not None:
            currentlyLoggedIn = UserProfile.objects.get(username = user)
            currentFarmID = currentlyLoggedIn.currentFarm_id

            self.fields["name"       ].widget.attrs.update({"class": "form-control", "width": 25})
            self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 3})
            self.fields["assignedTo" ].queryset = UserProfile.objects.filter(currentFarm=currentFarmID)
            self.fields["status"     ].widget.attrs.update({"class": "form-control"})
            self.fields["priority"   ].widget.attrs.update({"class": "form-control"})
            self.fields["dueDate"    ].widget.attrs.update({"class": "form-control"})

    TASK_STATUS_CHOICES = [ # Database stores status as int so we can iterate over buckets later.
        (0, "Not Started"),
        (1, "In Progress"),
        (2, "Blocked"    ),
        (3, "Review"     ),
        (4, "Complete"   ),
        (5, "Archived"   )
    ]

    TASK_PRIORITY_CHOICES = [
        (0, "Low"   ),
        (1, "Medium"),
        (2, "High"  ),
        (3, "Urgent")
    ]

    name        = forms.CharField(max_length=100, label="Task Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length= 200, label="Task Description", required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    assignedTo  = forms.ModelChoiceField(label="Task Assignment", queryset=UserProfile.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    status      = forms.ChoiceField(choices = TASK_STATUS_CHOICES, label="Task Status",  widget=forms.Select(attrs={'class': 'form-control'}))
    priority    = forms.ChoiceField(choices = TASK_PRIORITY_CHOICES, label="Task Priority", widget=forms.Select(attrs={'class': 'form-control'}))
    dueDate     = forms.DateField(input_formats=["%d/%m/%Y"], label="Task Due Date", widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Format - DD/MM/YYYY'}))

    def clean(self):
        cleaned_data = super().clean()
        dueDate = cleaned_data.get('dueDate')

        if dueDate != None and dueDate < datetime.date.today():
            self._errors["dueDate"] = ["Due Date cannot be in the past."]
            
        if not super().is_valid():
            raise forms.ValidationError('Please correct the errors below and resubmit the form.')

        return cleaned_data
    
    class Meta:
        model = Task
        fields = [
            'taskID'     ,
            'name'       ,
            'description',
            'assignedTo' ,
            'status'     ,
            'priority'   ,
            'dueDate'
        ]


class deleteTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ["taskID"]


# Kanbans
class createKanbanForm(ModelForm):
    class Meta:
        model  = Kanban
        fields = ["name"]

    name = forms.CharField(label="Name")


class deleteKanbanForm(ModelForm):

    class Meta:
        model = Kanban
        fields = ["kanbanID"]


# Kanban Contents
class createKanbanContentForm(ModelForm):
    class Meta:
        model  = KanbanContents
        fields = ["taskID", "order", "status"]

    status = forms.IntegerField() # Would need to update this if custom statuses made


class updateKanbanContentForm(Form):
    class Meta:
        fields = ["kanbanContentsID", "order", "status"]

    kanbanContentsID = forms.IntegerField()
    order            = forms.IntegerField()
    status           = forms.IntegerField() # Would need to update this if custom statuses made
