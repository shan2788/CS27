from django.db import models
from assetManagement.models import asset
from assetMaintenance.models import Maintenance
from UserAuth.models import UserProfile

expenseChoices = {
    0: "Fuel",
    1: "Maintenance",
    2: "Insurance",
    3: "Registration",
    4: "Other"
}

class Expense(models.Model):
    expenseID       = models.AutoField(primary_key=True)
    assetID         = models.ForeignKey(asset, on_delete=models.CASCADE, null=False) # Definitely should not be CASCADE
    expenseType     = models.SmallIntegerField(choices=expenseChoices, default=0)
    MaintenanceID   = models.ForeignKey(Maintenance, on_delete=models.CASCADE, null=True)
    cost            = models.DecimalField(max_digits=10, decimal_places=2)
    receiptNumber   = models.PositiveIntegerField(null=False)
    expenseLodgedBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    deleted         = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.expenseID)} - {self.expenseType}"
