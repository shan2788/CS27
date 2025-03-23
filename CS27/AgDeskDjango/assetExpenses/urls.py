from django.urls import path
from . import views

urlpatterns = [
    path("expenses",
         views.viewAllExpenses          , name="viewExpenses"),
    path("expenses/<int:expenseID>",
         views.expenseDetails           , name="viewSingleExpense"),
    path("asset/<str:assetCategory>/<int:assetID>/expenses",
         views.viewExpenseForSingleAsset, name="assetExpenses"),
    path("asset/<str:assetCategory>/<int:assetID>/expenses/<int:expenseID>/details",
         views.expenseDetails           , name="viewSingleAssetExpense"),
    path("getExpenseDetails/<int:expenseID>/",
         views.get_expense_details      , name="get_expense_details"),
    path("asset/<str:assetCategory>/<int:assetID>/expenses/<int:expenseID>/delete",
         views.deleteExpense            , name="deleteExpense")
]
