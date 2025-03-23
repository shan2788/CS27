from django.urls import path

from . import views

urlpatterns = [
    path("new"                             , views.newFarm     , name="newFarm"     ),
    path("join"                            , views.joinFarm    , name="joinFarm"    ),
    path("farm-files"                      , views.fileView    , name="fileView"    ),
    path("download-farm-file/<int:file_id>", views.downloadFile, name="fileDownload"),
    path("delete-file/<int:file_id>"       , views.deleteFile  , name="delete_file" ),
    path("file-details/<int:file_id>"      , views.editFile    , name="edit_file"   ),
    path("choose-farm"                     , views.chooseFarm  , name="chooseFarm"  )
]