"""
Views for emergency contacts
"""

# Imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.forms import formset_factory
from django.contrib import messages

from .models import FarmContacts, ContactInfo
from .forms import createContactForm, updateContactForm, createFieldForm, updateFieldForm

from FarmAcc.models import FarmInfo


#Database queries
def createContactQuery(formData, farmID):
    newContact = FarmContacts(
        farmID = FarmInfo.objects.get(id=farmID)                               ,
        order  = len(FarmContacts.objects.filter(farmID=farmID, deleted=False)),
        name   = formData["contact_name"]                                      ,
        desc   = formData["contact_desc"]                                      ,
        image  = formData["image"       ]
    )

    newContact.save()
    return newContact


def updateContactQuery(formData, contactID):
    contact = FarmContacts.objects.get(farmContactID=contactID)

    # contact.order = contact.order # One day...
    contact.name  = formData["contact_name"]
    contact.desc  = formData["contact_desc"]
    contact.image = formData["image"       ]

    contact.save()
    return contact


def deleteContactQuery(contactID):
    contact = FarmContacts.objects.get(farmContactID=contactID)
    contactInfo = ContactInfo.objects.filter(farmContactID=contactID, deleted=False)

    for info in contactInfo:
        info.deleted = True
        info.save()

    contact.deleted = True
    contact.save()


def createFieldQuery(formData, contactObject):
    newField = ContactInfo(
        farmContactID = contactObject                                                              ,
        order         = len(ContactInfo.objects.filter(farmContactID=contactObject, deleted=False)),
        field         = formData["contact_method"]                                                 ,
        info          = formData["contact_info"  ]
    )

    newField.save()


def updateFieldQuery(formData, contactInfoID):
    field = ContactInfo.objects.get(contactInfoID=contactInfoID)

    # field.order = contact.order # One day...
    field.field = formData["contact_method"]
    field.info  = formData["contact_info"  ]

    field.save()


def deleteFieldQuery(contactInfoID):
    field = ContactInfo.objects.get(contactInfoID=contactInfoID)
    contactID = field.farmContactID_id
    field.deleted = True

    field.save()
    return contactID


# Emergency Contact List View
@login_required(login_url="login")
def emergencyContacts(request):
    """
    Page for the farms emergency contacts.
    """

    # Refactor the contacts_list code into a query function?
    contacts = FarmContacts.objects                                \
        .filter(farmID=request.user.currentFarm_id, deleted=False) \
        .order_by("order")

    contacts_list = []
    for contact in contacts:
        contact_info = ContactInfo.objects                              \
            .filter(farmContactID=contact.farmContactID, deleted=False) \
            .order_by("order")
        contacts_list.append([contact, contact_info])

    createContactContext  = createContactForm()
    updateContactContext  = updateContactForm()
    addContactInfoFormset = formset_factory(createFieldForm)
    contactInfoForm       = addContactInfoFormset(prefix="contactInfo")
    # Redirect to emergency table view with a message to add contacts
    noContacts            = len(contacts) == 0
    noContactsMessage     = "You have no emergency contacts yet. Add some!"

    context = {
        "CreateContact"    : createContactContext,
        "UpdateContact"    : updateContactContext,
        "contactInfoForm"  : contactInfoForm     ,
        "Contacts"         : contacts_list       ,
        "NoContacts"       : noContacts          ,
        "NoContactsMessage": noContactsMessage
    }

    if request.method == "POST":
        contact_form = createContactForm(request.POST, request.FILES)
        contact_info_form = addContactInfoFormset(request.POST, request.FILES, prefix="contactInfo")

        if contact_form.is_valid():
            new_contact = createContactQuery(contact_form.cleaned_data, request.user.currentFarm_id)
            if contact_info_form.is_valid():
                for form in contact_info_form:
                    createFieldQuery(form.cleaned_data, new_contact)

        return redirect("/emergency/contacts")

    return render(request, "Emergency/farmContacts.html", context)


# Update Contact View
@login_required(login_url="login")
def updateContact(request, contactID):
    addContactInfoFormset  = formset_factory(createFieldForm)
    current_contact = FarmContacts.objects.get(farmContactID=contactID)

    if request.method == "GET":
        contact = FarmContacts.objects.get(farmContactID=contactID)

        contacts_info = []
        contact_info = ContactInfo.objects                     \
            .filter(farmContactID_id=contactID, deleted=False) \
            .values()                                          \
            .order_by("order")
        for info in contact_info:
            contacts_info.append(info)

        contact_form = createContactForm(initial={
            "contact_name": contact.name ,
            "contact_desc": contact.desc ,
            "image"       : contact.image
        })

        contactInfoForm = addContactInfoFormset(prefix="contactInfo")

        context = {
            "Contact"           : contact          ,
            "ContactInfo"       : contacts_info    ,
            "UpdateContact"     : contact_form     ,
            "addContactInfoForm": contactInfoForm  ,
            "editContactInfo"   : updateFieldForm()
        }

        return render(request, "Emergency/viewContact.html", context)

    if request.method == "POST":
        contact_form        = createContactForm(    request.POST, request.FILES                      )
        editContactInfoForm = updateFieldForm(      request.POST, request.FILES                      )
        addContactInfoForm  = addContactInfoFormset(request.POST, request.FILES, prefix="contactInfo")
        successMessages     = set()

        if contact_form.is_valid():
            if contact_form["image"] == None:
                contact_form["image"] = "images/contact_images/defaultImage.jpg"
            updateContactQuery(contact_form.cleaned_data, current_contact.farmContactID)
            successMessages.add("Contact Details Updated")

        if addContactInfoForm.is_valid():
            for form in addContactInfoForm:
                createFieldQuery(form.cleaned_data, current_contact)
                successMessages.add("New Contact Information Added")

        if editContactInfoForm.is_valid():
            updateFieldQuery(editContactInfoForm.cleaned_data, editContactInfoForm.cleaned_data["contact_info_id"])
            successMessages.add("Contact Information Updated")

        for msg in successMessages:
            messages.add_message(request, messages.SUCCESS, msg)

        # Probably shouldn't have ID exposed in URL like this, at least not until we validate the farm
        return redirect(f"/emergency/contacts/{contactID}")

    return render(request, "Emergency/farmContacts.html")


# Deletion Endpoints
@login_required(login_url="login")
def deleteContact(request, contactID):
    if request.user.currentFarm_id == FarmContacts.objects.get(farmContactID=contactID).farmID.id:
        deleteContactQuery(contactID)
        messages.add_message(request, messages.WARNING, "Contact Deleted")

        return redirect("/emergency/contacts")


@login_required(login_url="login")
def deleteContactInfo(request, contactInfoID):
    if request.user.currentFarm_id == ContactInfo.objects.get(contactInfoID=contactInfoID).farmContactID.farmID.id:
        contactID = deleteFieldQuery(contactInfoID)
        messages.add_message(request, messages.WARNING, "Contact Info Deleted")

        return redirect(f"/emergency/contacts/{contactID}")
