from django.urls import path

from . import views

urlpatterns = [
    path("contacts"                                       , views.emergencyContacts, name="emergencyContacts"),
    path("contacts/<int:contactID>"                       , views.updateContact    , name="updateContact"    ),

    path("contacts/<int:contactID>/delete"                , views.deleteContact    , name="deleteContact"    ),
    path("contacts/contactInfo/<int:contactInfoID>/delete", views.deleteContactInfo, name="deleteContactInfo")
]
