from django.test import TestCase
import random
from utils.testing_data import FARMCONTACTS_SUPERSET, CONTACTINFO_SUPERSET, FARM_SUPERSET
from utils.testing_data import generate_dataset_from_model
from UserAuth.models import UserProfile  # Import the custom user model
from Emergency.models import FarmContacts, ContactInfo
from FarmAcc.models import FarmInfo
from Emergency.views import *
from Emergency.forms import *

class BaseTestCase(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        self.user = UserProfile.objects.create_user(username='testuser', 
                                                    email='testuser@test.test',
                                                    password='12345',
                                                    currentFarm=self.farm[0])
        
        VALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][0],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][0],
            "image"                         : FARMCONTACTS_SUPERSET["image"][0],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        validContactList = generate_dataset_from_model(VALID_CONTACTS, False, False, False)
        
        VALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][2],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][2],
            "image"                         : FARMCONTACTS_SUPERSET["image"][2],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][2],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }

        validBoundaryContactList = generate_dataset_from_model(VALID_BOUNDARY_CONTACTS, False, False, False)
        
        INVALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][1],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][1],
            "image"                         : FARMCONTACTS_SUPERSET["image"][1],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][1],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        invalidContactList = generate_dataset_from_model(INVALID_CONTACTS, False, False, False)
        
        INVALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][3],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][3],
            "image"                         : FARMCONTACTS_SUPERSET["image"][3],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][3],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        invalidBoundaryContactList = generate_dataset_from_model(INVALID_BOUNDARY_CONTACTS, False, False, False)
        
        VALID_FIELDS = {
            "farmContactID" : self.contactList,
            "order"         : CONTACTINFO_SUPERSET["order"][0],
            "field"         : CONTACTINFO_SUPERSET["field"][0],
            "info"          : CONTACTINFO_SUPERSET["info"][0],
            "deleted"       : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        validContactFieldList = generate_dataset_from_model(VALID_FIELDS, False, False, False)
        
        VALID_BOUNDARY_FIELDS = {
            "farmContactID" : self.contactList,
            "order"         : CONTACTINFO_SUPERSET["order"][2],
            "field"         : CONTACTINFO_SUPERSET["field"][2],
            "info"          : CONTACTINFO_SUPERSET["info"][2],
            "deleted"       : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        validBoundaryContactFieldList = generate_dataset_from_model(VALID_BOUNDARY_FIELDS, False, False, False)
        
        INVALID_FIELDS = {
            "farmContactID" : self.contactList,
            "order"         : CONTACTINFO_SUPERSET["order"][1],
            "field"         : CONTACTINFO_SUPERSET["field"][1],
            "info"          : CONTACTINFO_SUPERSET["info"][1],
            "deleted"       : CONTACTINFO_SUPERSET["deleted"][1]
        }
        
        invalidContactFieldList = generate_dataset_from_model(INVALID_FIELDS, False, False, False)
        
        INVALID_BOUNDARY_FIELDS = {
            "farmContactID" : self.contactList,
            "order"         : CONTACTINFO_SUPERSET["order"][3],
            "field"         : CONTACTINFO_SUPERSET["field"][3],
            "info"          : CONTACTINFO_SUPERSET["info"][3],
            "deleted"       : CONTACTINFO_SUPERSET["deleted"][1]
        }
        
        invalidBoundaryContactFieldList = generate_dataset_from_model(INVALID_BOUNDARY_FIELDS, False, False, False)
        
        


class CreateContactQueryTest(BaseTestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        self.user = UserProfile.objects.create_user(username='testuser', 
                                                    email='testuser@test.test',
                                                    password='12345',
                                                    currentFarm=self.farm[0])
        
    # ------------------------------- TEST CASES - CREATE CONTACT ------------------------------- #    
    def test_create_contact_query(self):
        formData = {
            "contact_name": "John Doe",
            "contact_desc": "Emergency Contact",
            "image": "path/to/image.jpg"
        }
        
        # first created farm object.       
        farmID = self.farm[0].id

        # Call the function to create a new contact
        new_contact = createContactQuery(formData, farmID)

        # Fetch the contact from the database
        created_contact = FarmContacts.objects.get(farmContactID=new_contact.farmContactID)

         # Assertions to check if the contact was created correctly
        self.assertEqual(created_contact.farmID.id, farmID)
        self.assertEqual(created_contact.name, formData["contact_name"])
        self.assertEqual(created_contact.desc, formData["contact_desc"])
        self.assertEqual(created_contact.image, formData["image"])
        self.assertEqual(created_contact.order, 0)  # Since it's the first contact, order should be 0

        # Extra assertions
        self.assertFalse(created_contact.deleted)  # Ensure the contact is not marked as deleted
        self.assertIsInstance(created_contact, FarmContacts)  # Ensure the created object is an instance of FarmContacts
        self.assertEqual(created_contact.farmID.farm_name, self.farm[0].farm_name)  # Check farm name
        self.assertEqual(created_contact.farmID.farm_state, self.farm[0].farm_state)  # Check farm state

    def test_create_contact_query_with_multiple_contacts(self):
        formData1 = {
        "contact_name": "John Doe",
        "contact_desc": "Emergency Contact",
        "image": "path/to/image.jpg"
        }
    
        formData2 = {
            "contact_name": "Jane Doe",
            "contact_desc": "Secondary Contact",
            "image": "path/to/another_image.jpg"
        }
        
        # first created farm object.       
        farmID = self.farm[0].id

        # Call the function to create new contacts
        new_contact1 = createContactQuery(formData1, farmID)
        new_contact2 = createContactQuery(formData2, farmID)

        # Fetch the contacts from the database
        created_contact1 = FarmContacts.objects.get(farmContactID=new_contact1.farmContactID)
        created_contact2 = FarmContacts.objects.get(farmContactID=new_contact2.farmContactID)

        # Assertions to check if the contacts were created correctly
        self.assertEqual(created_contact1.farmID.id, farmID)
        self.assertEqual(created_contact1.name, formData1["contact_name"])
        self.assertEqual(created_contact1.desc, formData1["contact_desc"])
        self.assertEqual(created_contact1.image, formData1["image"])
        self.assertEqual(created_contact1.order, 0)  # Since it's the first contact, order should be 0

        self.assertEqual(created_contact2.farmID.id, farmID)
        self.assertEqual(created_contact2.name, formData2["contact_name"])
        self.assertEqual(created_contact2.desc, formData2["contact_desc"])
        self.assertEqual(created_contact2.image, formData2["image"])
        self.assertEqual(created_contact2.order, 1)  # Since it's the second contact, order should be 1

        # Extra assertions
        self.assertFalse(created_contact1.deleted)  # Ensure the first contact is not marked as deleted
        self.assertFalse(created_contact2.deleted)  # Ensure the second contact is not marked as deleted
        self.assertIsInstance(created_contact1, FarmContacts)  # Ensure the first created object is an instance of FarmContacts
        self.assertIsInstance(created_contact2, FarmContacts)  # Ensure the second created object is an instance of FarmContacts
        self.assertEqual(FarmContacts.objects.filter(farmID=farmID).count(), 2)  # Ensure there are exactly 2 contacts for the farm
        
    def test_create_multiple_valid_contacts(self):
        # Create multiple contacts
        farm_ids = FarmInfo.objects.all().values_list("id", flat=True) # Get all the farm IDs created in setup
        
        VALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][0],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][0],
            "image"                         : FARMCONTACTS_SUPERSET["image"][0],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        contactList = generate_dataset_from_model(VALID_CONTACTS, False, False, False)
        incorrectlyMissed = []
        # Create the contacts
        for contact in contactList:
            try:
                farmid = random.choice(farm_ids)
                createContactQuery(contact, farmid)
            except:
                incorrectlyMissed.append(contact.values())
                continue
            
        # Execute Assertion Checks - insert checks as needed
        contacts = FarmContacts.objects.all()
        self.assertEqual(len(contacts), len(contactList))
        
        for contact in contacts:
            self.assertIn(contact.farmID.id, farm_ids)
            self.assertIn(contact.name, VALID_CONTACTS["contact_name"])
            self.assertIn(contact.desc, VALID_CONTACTS["contact_desc"])
            self.assertIn(contact.image, VALID_CONTACTS["image"])
            self.assertFalse(contact.deleted)
            self.assertIsInstance(contact, FarmContacts)

    def test_create_multiple_valid_boundary_contacts(self):
        # Create multiple contacts
        farm_ids = FarmInfo.objects.all().values_list("id", flat=True) # Get all the farm IDs created in setup
        
        VALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][2],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][2],
            "image"                         : FARMCONTACTS_SUPERSET["image"][2],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][2],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }

        contactList = generate_dataset_from_model(VALID_BOUNDARY_CONTACTS, False, False, False)
        incorrectlyMissed = []
        # Create the contacts
        for contact in contactList:
            try:
                farmid = random.choice(farm_ids)
                createContactQuery(contact, farmid)
            except:
                incorrectlyMissed.append(contact.values())
                continue
        
        # Execute Assertion Checks - insert checks as needed
        contacts = FarmContacts.objects.all()
        self.assertEqual(len(contacts), len(contactList))

    def test_create_multiple_invalid_contacts(self):
        # Create multiple invalid contacts
        farmID = FarmInfo.objects.all().values("id")

        INVALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][1],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][1],
            "image"                         : FARMCONTACTS_SUPERSET["image"][1],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][1],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        contactList = generate_dataset_from_model(INVALID_CONTACTS, False, False, False)

        added = False
        incorrectlyAdded = []
        for contact in contactList:
            try:
                createContactQuery(contact, farmID)
                added = True
                incorrectlyAdded.append(contact.values())
            except:
                # If an exception is raised, the contacts were not added to the database
                # This should definitely be improved - could check if exception is handled gracefully in main app.
                pass

        #Assert that the contacts were not added to the database.
        self.assertEqual(added, False)

    def test_create_multiple_invalid_boundary_contacts(self):
        # Create multiple invalid contacts
        farmID = FarmInfo.objects.all().values("id")

        INVALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][3],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][3],
            "image"                         : FARMCONTACTS_SUPERSET["image"][3],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][3],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        contactList = generate_dataset_from_model(INVALID_BOUNDARY_CONTACTS, False, False, False)

        added = False
        incorrectlyAdded = []
        try:
            for contact in contactList:
                createContactQuery(contact, farmID)
                added = True
                incorrectlyAdded.append(contact.values())
        except:
            pass
        
        #Assert that the contacts were not added to the database.
        self.assertEqual(added, False)
        
        
class updateContactQueryTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        self.farm_ids = FarmInfo.objects.all().values_list("id", flat=True)
        
        self.user = UserProfile.objects.create_user(username='testuser', 
                                                    email='testuser@test.test',
                                                    password='12345',
                                                    currentFarm=self.farm[0])
        
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
        self.contactList = FarmContacts.objects.bulk_create(contactList)
        
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
        
        
        # ------------------------------- TEST CASES - UPDATE CONTACT ------------------------------- #
        
    def test_update_single_contact(self):
        # Select a random contact ID
        contactID = random.choice(self.contact_ids)
        
        formData = {
            "contact_name": "Jane Doe",
            "contact_desc": "Another Emergency Contact",
            "image": "path/to/another_image.jpg"
        }
        
        # Call the function to update the contact
        updated_contact = updateContactQuery(formData, contactID)
        
        # Fetch the contact from the database
        updated_contact = FarmContacts.objects.get(farmContactID=contactID)
        
        # Assertions to check if the contact was updated correctly
        self.assertEqual(updated_contact.name, formData["contact_name"])
        self.assertEqual(updated_contact.desc, formData["contact_desc"])
        self.assertEqual(updated_contact.image, formData["image"])
        
    def test_update_multiple_valid_contacts(self):
        initial_count = FarmContacts.objects.count()
        
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "contact_name"  : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "contact_desc"  : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        contactList = generate_dataset_from_model(VALID_CONTACTS, False, False, False)
        updatedCount = 0
        failedUpdates = []
        # Create the contacts
        for contact in contactList:
            try:
                contactID = random.choice(self.contact_ids)
                updateContactQuery(contact, contactID)
                updatedCount += 1
            except:
                # If an exception is raised, the contacts were not added to the database
                failedUpdates.append(contact.values())
            
        # Execute Assertion Checks - insert checks as needed
        contacts = FarmContacts.objects.all()
        # Check that no new contacts were created
        self.assertEqual(FarmContacts.objects.count(), initial_count)
        self.assertEqual(updatedCount, len(contactList) - len(failedUpdates))
        
    def test_update_multiple_valid_boundary_contacts(self):
        initial_count = FarmContacts.objects.count()
        
        VALID_BOUNDARY_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][2],
            "contact_name"  : FARMCONTACTS_SUPERSET["name"][2],
            "image"         : FARMCONTACTS_SUPERSET["image"][2],
            "contact_desc"  : FARMCONTACTS_SUPERSET["desc"][2],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }

        contactList = generate_dataset_from_model(VALID_BOUNDARY_CONTACTS, False, False, False)
        failedUpdates = []
        updatedCount = 0
        for contact in contactList:
            try:
                contactID = random.choice(self.contact_ids)
                updateContactQuery(contact, contactID)
                updatedCount += 1
            except:
                failedUpdates.append(contact)

        # Check that no new contacts were created
        self.assertEqual(FarmContacts.objects.count(), initial_count)
        self.assertEqual(updatedCount, len(contactList) - len(failedUpdates))
        


class DeleteContactQueryTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        self.farm_ids = FarmInfo.objects.all().values_list("id", flat=True)
        
        self.user = UserProfile.objects.create_user(username='testuser', 
                                                    email='testuser@test.test',
                                                    password='12345',
                                                    currentFarm=self.farm[0])
        
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
        self.contactList = FarmContacts.objects.bulk_create(contactList)
        
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
        
        
    # ------------------------------- TEST CASES - DELETE CONTACT ------------------------------- #
        

    def test_delete_single_contact(self):
        # Select a random contact ID
        contactID = self.contact_ids[0]
        
        # Call the function to delete the contact
        deleteContactQuery(contactID)
        deleted_contact = FarmContacts.objects.get(farmContactID=contactID)
        
        self.assertEqual(FarmContacts.objects.get(farmContactID=contactID).deleted, True)
        self.assertIsInstance(deleted_contact, FarmContacts)  # Ensure the deleted object is an instance of FarmContacts
        self.assertEqual(deleted_contact.farmID.id, self.farm[0].id)  # Check farm ID
        
    def test_delete_multiple_valid_contacts(self):
        
        for contact in self.contact_ids:
            deleteContactQuery(contact)
        
        # Check if all contacts were deleted
        self.assertEqual(FarmContacts.objects.filter(deleted=False).count(), 0)
        for contact in self.contact_ids:
            deleted_contact = FarmContacts.objects.get(farmContactID=contact)
            self.assertEqual(deleted_contact.deleted, True)  # Ensure each contact is marked as deleted
            self.assertIsInstance(deleted_contact, FarmContacts)  # Ensure each deleted object is an instance of FarmContacts
        
    def test_delete_deleted_contact(self):
        # Select a random contact ID
        contactID = random.choice(self.contact_ids)
        
        # Call the function to delete the contact
        deleteContactQuery(contactID)
        
        # Call the function to delete the contact again
        deleteContactQuery(contactID)
        
        self.assertEqual(FarmContacts.objects.get(farmContactID=contactID).deleted, True)
    
    def test_delete_non_existent_contact(self):        
        # Select a random contact ID
        contactID = random.choice(self.contact_ids)
        
        FarmContacts.objects.filter(farmContactID=contactID).delete()
        
        self.assertEqual(FarmContacts.objects.filter(farmContactID=contactID).count(), 0)  # Ensure the contact does not exist
        # Call the function to delete the contact
        with self.assertRaises(FarmContacts.DoesNotExist):
            deleteContactQuery(contactID)
        
        
        
# ------------------------------- TEST CASES - CREATE CONTACTINFO ------------------------------- #

class createFieldQueryTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
      
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
      
        self.farm = FarmInfo.objects.bulk_create(farmList)
       
        self.farm_ids = FarmInfo.objects.all().values_list("id", flat=True)
                                                    
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
       
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
       
        self.contactList = FarmContacts.objects.bulk_create(contactList)
       
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
        
     # ------------------------------- TEST CASES - CREATE ContactInfo ------------------------------- #
    
    def test_create_field_query(self):
        # create multiple valid contacts
        VALID_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][0],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][0],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][0],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        contactFieldList = generate_dataset_from_model(VALID_FIELDS, False, False, False)
        incorrectlyMissed = []
        
        # Create the contacts
        for field in contactFieldList:
            try:
                contactID = random.choice(self.contactList)
                createFieldQuery(field, contactID)
            except Exception as e:
                incorrectlyMissed.append((field.values(), e))
        
        # Execute Assertion Checks
        contacts = ContactInfo.objects.all()
        self.assertEqual(incorrectlyMissed, [])
        self.assertEqual(len(contacts), len(contactFieldList))
        
    def test_create_field_query_boundary_valid(self):
        
        VALID_BOUNDARY_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][2],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][2],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][2],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        contactFieldList = generate_dataset_from_model(VALID_BOUNDARY_FIELDS, False, False, False)
        incorrectlyMissed = []
        
        # Create the contacts
        for field in contactFieldList:
            try:
                contactID = random.choice(self.contactList)
                createFieldQuery(field, contactID)
            except:
                incorrectlyMissed.append(field.values())

        contacts = ContactInfo.objects.all()
        self.assertEqual(len(contacts), len(contactFieldList))
        
        
    def test_create_field_query_boundary_invalid(self):
        # create multiple invalid contacts
        INVALID_BOUNDARY_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][3],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][3],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][3],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][1]
        }
        
        contactFieldList = generate_dataset_from_model(INVALID_BOUNDARY_FIELDS, False, False, False)
        
        added = False
        incorrectlyAdded = []
        for field in contactFieldList:
            try:
                contactID = random.choice(self.contactList)
                createContactQuery(field, contactID)
                added = True
                incorrectlyAdded.append(field.values())
            except:
                pass
        
        self.assertEqual(added, False)
        
class updateFieldQueryTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
      
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
      
        self.farm = FarmInfo.objects.bulk_create(farmList)
       
        self.farm_ids = FarmInfo.objects.all().values_list("id", flat=True)
                                                    
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
       
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
       
        self.contactList = FarmContacts.objects.bulk_create(contactList)
       
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
        
        # create multiple valid contacts
        VALID_FIELDS = {
            "farmContactID" : self.contactList,
            "order"         : CONTACTINFO_SUPERSET["order"][0],
            "field"         : CONTACTINFO_SUPERSET["field"][0],
            "info"          : CONTACTINFO_SUPERSET["info"][0],
            "deleted"       : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        contactFieldList = [ContactInfo(**contact_field_data) for contact_field_data in generate_dataset_from_model(VALID_FIELDS, False, False, False)]
        
        self.cntact_fields = ContactInfo.objects.bulk_create(contactFieldList)
        
        self.contact_field_ids = ContactInfo.objects.all().values_list("contactInfoID", flat=True)
        
    def test_update_field_query(self):
        initial_count = ContactInfo.objects.count()
        
        VALID_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][0],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][0],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][0],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        contactFieldList = generate_dataset_from_model(VALID_FIELDS, False, False, False)
        updatedCount = 0
        failedUpdates = []
        
        for contactField in contactFieldList:
            try:
                contactFieldID = random.choice(self.contact_field_ids)
                updateFieldQuery(contactField, contactFieldID)
                updatedCount += 1
            except:
                failedUpdates.append(contactField)
        
        self.assertEqual(ContactInfo.objects.count(), initial_count)
        self.assertEqual(updatedCount, len(contactFieldList) - len(failedUpdates))
        
    def test_update_field_query_boundary_valid(self):
        
        VALID_BOUNDARY_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][2],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][2],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][2],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        contactFieldList = generate_dataset_from_model(VALID_BOUNDARY_FIELDS, False, False, False)
        failedUpdates = []
        updatedCount = 0
        for contactField in contactFieldList:
            try:
                contactFieldID = random.choice(self.contact_field_ids)
                updateFieldQuery(contactField, contactFieldID)
                updatedCount += 1
            except:
                failedUpdates.append(contactField)
                
        self.assertEqual(updatedCount, len(contactFieldList) - len(failedUpdates))
        
    class deleteFieldQueryTest(TestCase):
        def setUp(self):
            # Create a user and a farm for testing
            VALID_FARMS = {
                "farm_name"     : FARM_SUPERSET["farm_name"][0],
                "farm_street"   : FARM_SUPERSET["farm_street"][0],
                "farm_state"    : FARM_SUPERSET["farm_state"][0],
                "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
                "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
                "farm_image"    : FARM_SUPERSET["farm_image"][0]
            }
        
            farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        
            self.farm = FarmInfo.objects.bulk_create(farmList)
        
            self.farm_ids = FarmInfo.objects.all().values_list("id", flat=True)
                                                        
            # Create a list of contacts to test the delete function
            VALID_CONTACTS = {
                "farmID"        : self.farm,
                "order"         : FARMCONTACTS_SUPERSET["order"][0],
                "name"          : FARMCONTACTS_SUPERSET["name"][0],
                "image"         : FARMCONTACTS_SUPERSET["image"][0],
                "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
                "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
            }
        
            contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
        
            self.contactList = FarmContacts.objects.bulk_create(contactList)
        
            # Get List of valid contact IDs
            self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
            
            # create multiple valid contacts
            VALID_FIELDS = {
                "farmContactID" : self.contactList,
                "order"         : CONTACTINFO_SUPERSET["order"][0],
                "field"         : CONTACTINFO_SUPERSET["field"][0],
                "info"          : CONTACTINFO_SUPERSET["info"][0],
                "deleted"       : CONTACTINFO_SUPERSET["deleted"][0]
            }
            
            contactFieldList = [ContactInfo(**contact_field_data) for contact_field_data in generate_dataset_from_model(VALID_FIELDS, False, False, False)]
            
            self.cntact_fields = ContactInfo.objects.bulk_create(contactFieldList)
            
            self.contact_field_ids = ContactInfo.objects.all().values_list("contactInfoID", flat=True)
        
    def test_delete_field_query(self):
        
        for field in self.contact_field_ids:
            deleteFieldQuery(field)
            
        # Check if all contacts were deleted
        self.assertEqual(ContactInfo.objects.filter(deleted=False).count(), 0)
        for field in self.contact_field_ids:
            deleted_field = ContactInfo.objects.get(contactInfoID=field)
            self.assertEqual(deleted_field.deleted, True)
            self.assertIsInstance(deleted_field, ContactInfo)
            
    def test_delete_field_query_deleted_field(self):
        # Select a random field ID
        fieldID = random.choice(self.contact_field_ids)
        
        # Call the function to delete the field
        deleteFieldQuery(fieldID)
        
        # Call the function to delete the field again
        deleteFieldQuery(fieldID)
        
        self.assertEqual(ContactInfo.objects.get(contactInfoID=fieldID).deleted, True)
        
    def test_delete_field_query_non_existent_field(self):
        # Select a random field ID
        fieldID = random.choice(self.contact_field_ids)
        
        ContactInfo.objects.filter(contactInfoID=fieldID).delete()
        
        self.assertEqual(ContactInfo.objects.filter(contactInfoID=fieldID).count(), 0)
        # Call the function to delete the field
        with self.assertRaises(ContactInfo.DoesNotExist):
            deleteFieldQuery(fieldID)
            
class createContactFormTest(TestCase):
    
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
    
    # ------------------------------- TEST CASES - CREATE CONTACT FORM ------------------------------- #
    
    def test_create_contact_form(self):
        VALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][0],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][0],
            "image"                         : FARMCONTACTS_SUPERSET["image"][0],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        validContactList = generate_dataset_from_model(VALID_CONTACTS, False, False, False)
        
        errors = []
        
        for contact in validContactList:
            try:
                form = createContactForm(data = contact)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((contact, e))
                
        self.assertEqual(errors, [])
        
    def test_create_contact_form_boundary_Valid(self):
        VALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][2],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][2],
            "image"                         : FARMCONTACTS_SUPERSET["image"][2],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][2],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }

        validBoundaryContactList = generate_dataset_from_model(VALID_BOUNDARY_CONTACTS, False, False, False)
        
        errors = []
        
        for contact in validBoundaryContactList:
            try:
                form = createContactForm(data = contact)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((contact, e))
                
        self.assertEqual(errors, [])
        
        
    def test_create_contact_form_boundary_invalid(self):
        INVALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][3],
            "contact_name"                  : FARMCONTACTS_SUPERSET["name"][3],
            "image"                         : FARMCONTACTS_SUPERSET["image"][3],
            "contact_desc"                  : FARMCONTACTS_SUPERSET["desc"][3],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        invalidBoundaryContactList = generate_dataset_from_model(INVALID_BOUNDARY_CONTACTS, False, False, False)
        
        errors = []
        added = False
        for contact in invalidBoundaryContactList:
            try:
                form = createContactForm(data = contact)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((contact, e))

        self.assertEqual(errors, [])
        self.assertEqual(added, False)
        
        
class updateContactFormTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
        self.contactList = FarmContacts.objects.bulk_create(contactList)
        
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)

    # ------------------------------- TEST CASES - UPDATE CONTACT FORM ------------------------------- #

    def test_update_contact_form(self):
        VALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][0],
            "name"                          : FARMCONTACTS_SUPERSET["name"][0],
            "image"                         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"                          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        validContactList = generate_dataset_from_model(VALID_CONTACTS, False, False, False)
        
        errors = []
        
        for contact in validContactList:
            try:
                form = updateContactForm(data = contact)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((contact, form.errors))
                
        self.assertEqual(errors, [])

    def test_update_contact_form_boundary_valid(self):
        VALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][2],
            "name"                          : FARMCONTACTS_SUPERSET["name"][2],
            "image"                         : FARMCONTACTS_SUPERSET["image"][2],
            "desc"                          : FARMCONTACTS_SUPERSET["desc"][2],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][0]
        }

        validBoundaryContactList = generate_dataset_from_model(VALID_BOUNDARY_CONTACTS, False, False, False)
        
        errors = []
        
        for contact in validBoundaryContactList:
            try:
                form = updateContactForm(data = contact)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((contact, form.errors))
                
        self.assertEqual(errors, [])

    def test_update_contact_form_invalid(self):
        INVALID_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][1],
            "name"                          : FARMCONTACTS_SUPERSET["name"][1],
            "image"                         : FARMCONTACTS_SUPERSET["image"][1],
            "desc"                          : FARMCONTACTS_SUPERSET["desc"][1],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        invalidContactList = generate_dataset_from_model(INVALID_CONTACTS, False, False, False)
        
        errors = []
        added = False
        for contact in invalidContactList:
            try:
                form = updateContactForm(data = contact)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((contact, e))

        self.assertEqual(errors, [])
        self.assertEqual(added, False)
        

    def test_update_contact_form_boundary_invalid(self):
        INVALID_BOUNDARY_CONTACTS = {
            "order"                         : FARMCONTACTS_SUPERSET["order"][3],
            "name"                          : FARMCONTACTS_SUPERSET["name"][3],
            "image"                         : FARMCONTACTS_SUPERSET["image"][3],
            "desc"                          : FARMCONTACTS_SUPERSET["desc"][3],
            "deleted"                       : FARMCONTACTS_SUPERSET["deleted"][1]
        }

        invalidBoundaryContactList = generate_dataset_from_model(INVALID_BOUNDARY_CONTACTS, False, False, False)
        
        errors = []
        added = False
        for contact in invalidBoundaryContactList:
            try:
                form = updateContactForm(data = contact)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((contact, e))
                
        self.assertEqual(errors, [])
        self.assertEqual(added, False)

class createFieldFormTest(TestCase):

    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
        
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
        self.contactList = FarmContacts.objects.bulk_create(contactList)
        
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
        
    # ------------------------------- TEST CASES - CREATE FIELD FORM ------------------------------- #
    
    def test_create_field_form(self):
        VALID_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][0],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][0],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][0],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        validFieldList = generate_dataset_from_model(VALID_FIELDS, False, False, False)
        
        errors = []
        
        for field in validFieldList:
            try:
                form = createFieldForm(data = field)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((field, form.errors))

        self.assertEqual(errors, [])

    def test_create_field_form_boundary_valid(self):
        VALID_BOUNDARY_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][2],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][2],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][2],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][0]
        }

        validBoundaryFieldList = generate_dataset_from_model(VALID_BOUNDARY_FIELDS, False, False, False)
        
        errors = []
        
        for field in validBoundaryFieldList:
            try:
                form = createFieldForm(data = field)
                self.assertTrue(form.is_valid())
            except:
                errors.append((field, form.errors))
                
        self.assertEqual(errors, [])

    def test_create_field_form_invalid(self):
        INVALID_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][1],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][1],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][1],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][1]
        }

        invalidFieldList = generate_dataset_from_model(INVALID_FIELDS, False, False, False)
        
        errors = []
        added = False
        for field in invalidFieldList:
            try:
                form = createFieldForm(data = field)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((field, e))
                
        self.assertEqual(errors, [])
        self.assertEqual(added, False)
        

    def test_create_field_form_boundary_invalid(self):
        INVALID_BOUNDARY_FIELDS = {
            "farmContactID"     : self.contactList,
            "order"             : CONTACTINFO_SUPERSET["order"][3],
            "contact_method"    : CONTACTINFO_SUPERSET["field"][3],
            "contact_info"      : CONTACTINFO_SUPERSET["info"][3],
            "deleted"           : CONTACTINFO_SUPERSET["deleted"][1]
        }

        invalidBoundaryFieldList = generate_dataset_from_model(INVALID_BOUNDARY_FIELDS, False, False, False)
        
        errors = []
        added = False
        for field in invalidBoundaryFieldList:
            try:
                form = createFieldForm(data = field)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((field, e))
                
        self.assertEqual(errors, [])     
        self.assertEqual(added, False)

class updateFieldFormTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name"     : FARM_SUPERSET["farm_name"][0],
            "farm_street"   : FARM_SUPERSET["farm_street"][0],
            "farm_state"    : FARM_SUPERSET["farm_state"][0],
            "farm_postcode" : FARM_SUPERSET["farm_postcode"][0],
            "farm_bio"      : FARM_SUPERSET["farm_bio"][0],
            "farm_image"    : FARM_SUPERSET["farm_image"][0]
        }
      
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
      
        self.farm = FarmInfo.objects.bulk_create(farmList)
       
        self.farm_ids = FarmInfo.objects.all().values_list("id", flat=True)
                                                    
        # Create a list of contacts to test the delete function
        VALID_CONTACTS = {
            "farmID"        : self.farm,
            "order"         : FARMCONTACTS_SUPERSET["order"][0],
            "name"          : FARMCONTACTS_SUPERSET["name"][0],
            "image"         : FARMCONTACTS_SUPERSET["image"][0],
            "desc"          : FARMCONTACTS_SUPERSET["desc"][0],
            "deleted"       : FARMCONTACTS_SUPERSET["deleted"][0]
        }
       
        contactList = [FarmContacts(**contact_data) for contact_data in generate_dataset_from_model(VALID_CONTACTS, False, False, False)]
       
        self.contactList = FarmContacts.objects.bulk_create(contactList)
       
        # Get List of valid contact IDs
        self.contact_ids = FarmContacts.objects.all().values_list("farmContactID", flat=True)
        
        # create multiple valid contacts
        VALID_FIELDS = {
            "farmContactID" : self.contactList,
            "order"         : CONTACTINFO_SUPERSET["order"][0],
            "field"         : CONTACTINFO_SUPERSET["field"][0],
            "info"          : CONTACTINFO_SUPERSET["info"][0],
            "deleted"       : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        contactFieldList = [ContactInfo(**contact_field_data) for contact_field_data in generate_dataset_from_model(VALID_FIELDS, False, False, False)]
        
        self.contact_fields = ContactInfo.objects.bulk_create(contactFieldList)
        
        self.contact_field_ids = ContactInfo.objects.all().values_list("contactInfoID", flat=True)

    # ------------------------------- TEST CASES - UPDATE FIELD FORM ------------------------------- #

    def test_update_field_form(self):
        VALID_FIELDS = {
            "contact_info_id"       : self.contact_field_ids,
            "order"                 : CONTACTINFO_SUPERSET["order"][0],
            "contact_method"        : CONTACTINFO_SUPERSET["field"][0],
            "contact_info"          : CONTACTINFO_SUPERSET["info"][0],
            "deleted"               : CONTACTINFO_SUPERSET["deleted"][0]
        }
        
        validFieldList = generate_dataset_from_model(VALID_FIELDS, False, False, False)
        
        errors = []
        
        for field in validFieldList:
            try:
                form = updateFieldForm(data = field)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((field, form.errors))
                
        self.assertEqual(errors, [])

    def test_update_field_form_boundary_valid(self):
        VALID_BOUNDARY_FIELDS = {
            "contact_info_id"       : self.contact_field_ids,
            "order"                 : CONTACTINFO_SUPERSET["order"][2],
            "contact_method"        : CONTACTINFO_SUPERSET["field"][2],
            "contact_info"          : CONTACTINFO_SUPERSET["info"][2],
            "deleted"               : CONTACTINFO_SUPERSET["deleted"][0]
        }

        validBoundaryFieldList = generate_dataset_from_model(VALID_BOUNDARY_FIELDS, False, False, False)
        
        errors = []
        
        for field in validBoundaryFieldList:
            try:
                form = updateFieldForm(data = field)
                self.assertTrue(form.is_valid())
            except Exception as e:
                errors.append((field, form.errors))
                
        self.assertEqual(errors, [])

    def test_update_field_form_invalid(self):
        INVALID_FIELDS = {
            "contact_info_id"       : self.contact_field_ids,
            "order"                 : CONTACTINFO_SUPERSET["order"][1],
            "contact_method"        : CONTACTINFO_SUPERSET["field"][1],
            "contact_info"          : CONTACTINFO_SUPERSET["info"][1],
            "deleted"               : CONTACTINFO_SUPERSET["deleted"][1]
        }

        invalidFieldList = generate_dataset_from_model(INVALID_FIELDS, False, False, False)
        
        errors = []
        added = False
        for field in invalidFieldList:
            try:
                form = updateFieldForm(data = field)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((field, e))
        
        self.assertEqual(errors, [])  
        self.assertEqual(added, False)
        

    def test_update_field_form_boundary_invalid(self):
        INVALID_BOUNDARY_FIELDS = {
            "contact_info_id"       : self.contact_field_ids,
            "order"                 : CONTACTINFO_SUPERSET["order"][3],
            "contact_method"        : CONTACTINFO_SUPERSET["field"][3],
            "contact_info"          : CONTACTINFO_SUPERSET["info"][3],
            "deleted"               : CONTACTINFO_SUPERSET["deleted"][1]
        }

        invalidBoundaryFieldList = generate_dataset_from_model(INVALID_BOUNDARY_FIELDS, False, False, False)
        
        errors = []
        added = False
        for field in invalidBoundaryFieldList:
            try:
                form = updateFieldForm(data = field)
                self.assertFalse(form.is_valid())
            except Exception as e:
                added = True
                errors.append((field, e))
           
        self.assertEqual(errors, [])     
        self.assertEqual(added, False)
        





                

        

        
        
        
        
        
            
        
        
            
        
    
        
        
    