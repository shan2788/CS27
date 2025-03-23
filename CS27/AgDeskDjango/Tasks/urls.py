"""
The url paths for task functionality.

All paths are /task/...
"""

from django.urls import path

from . import views

urlpatterns = [
    path(""                       , views.taskTableManagement                         ),
    path("tableView"              , views.taskTableManagement, name="tableView"       ),
    path("updateTask/<int:taskID>", views.taskUpdatePage     , name="update_task"     ),
    path("updateTask/"            , views.nullTaskUpdatePage , name="update_task_noID"),
    path("kanbanTable"            , views.kanbanTable        , name="kanbanTable"     ),
    path("deleteKanban"           , views.deleteKanban       , name="deleteKanban"    ),
    path("kanbanView"             , views.kanbanBoard        , name="kanbanView"      ),
    path("updateKanban"           , views.updateKanban       , name="updateKanban"    ),
]
