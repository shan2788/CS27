"""
Models for tasks and kanban boards.
"""


# Imports
from datetime import datetime
from django.db import models
from FarmAcc.models import FarmInfo
from UserAuth.models import UserProfile


# Tasks
class Task(models.Model):
    """
    The tasks that need to be completed on the farm.
    """

    taskID      = models.AutoField(primary_key=True)
    farmID      = models.ForeignKey(FarmInfo, on_delete=models.CASCADE)
    assignedTo  = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name        = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, default="")
    timeStamp   = models.DateTimeField(default=datetime.now)
    # Pass function instead of value. Also, default done by django, not postgres.

    isCompleted = models.BooleanField(default=False)
    isArchived  = models.BooleanField(default=False)
    isDeleted   = models.BooleanField(default=False)

    dueDate = models.DateField(null=True, blank=True)
    expiry  = models.DateField(null=True, blank=True)

    TASK_STATUS_CHOICES = [ # Database stores status as int so we can iterate over buckets later.
        (0, "Not Started"),
        (1, "In Progress"),
        (2, "Blocked"    ),
        (3, "Review"     ),
        (4, "Complete"   ),
        (5, "Archived"   )
    ]
    status = models.PositiveSmallIntegerField(choices=TASK_STATUS_CHOICES, default=0)

    TASK_PRIORITY_CHOICES = [
        (0, "Low"   ),
        (1, "Medium"),
        (2, "High"  ),
        (3, "Urgent")
    ]
    priority = models.PositiveSmallIntegerField(choices=TASK_PRIORITY_CHOICES, default=0)


# Kanbans
class Kanban(models.Model):
    """
    A farm can have multiple kanban boards.
    """

    kanbanID = models.AutoField(primary_key=True)
    farmID   = models.ForeignKey(FarmInfo, on_delete=models.CASCADE)
    name     = models.CharField(max_length=100)
    deleted  = models.BooleanField(default=False)


class KanbanContents(models.Model):
    """
    Maps the tasks inside of a kanban.
    """

    kanbanContentsID = models.AutoField(primary_key=True)
    kanbanID         = models.ForeignKey(Kanban, on_delete=models.CASCADE)
    taskID           = models.ForeignKey(Task, on_delete=models.CASCADE)
    order            = models.PositiveSmallIntegerField()
