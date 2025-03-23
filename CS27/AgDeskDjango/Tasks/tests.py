from django.test import TestCase
from utils.testing_data import generate_dataset_from_model
from utils.testing_data import FARM_SUPERSET, TASK_SUPERSET  # Import the testing data
from UserAuth.models import UserProfile
from FarmAcc.models import FarmInfo
from Tasks.models import Task
from Tasks.views import taskManager
from Tasks.forms import createTaskForm, taskForm
import datetime as dt
import random
from django.forms.models import model_to_dict
from django.db import transaction

# ------------------------------- TEST CLASS - BASE TASK TEST ------------------------------- #
class BaseTaskTest(TestCase):
    def setUp(self):
        # Create a user and a farm for testing
        VALID_FARMS = {
            "farm_name": FARM_SUPERSET["farm_name"][0],
            "farm_street": FARM_SUPERSET["farm_street"][0],
            "farm_state": FARM_SUPERSET["farm_state"][0],
            "farm_postcode": FARM_SUPERSET["farm_postcode"][0],
            "farm_bio": FARM_SUPERSET["farm_bio"][0],
            "farm_image": FARM_SUPERSET["farm_image"][0]
        }
        
        farmList = [FarmInfo(**farm_data) for farm_data in generate_dataset_from_model(VALID_FARMS, False, False, False)]
        self.farm = FarmInfo.objects.bulk_create(farmList)
        
        self.user = UserProfile(username='testuser', 
                                email='testuser@test.test',
                                password='12345',
                                currentFarm=self.farm[0])
        self.user.save()
        
        self.taskmanager = taskManager()

        self.generate_test_data()

    def generate_test_data(self):
        # Generate test data
        VALID_TASKS = {
            "farmID": self.farm,
            "assignedTo": [self.user],
            "name": TASK_SUPERSET["name"][0],
            "description": TASK_SUPERSET["description"][0],
            "timeStamp": TASK_SUPERSET["timeStamp"][0],
            "isCompleted": TASK_SUPERSET["isCompleted"][0],
            "isArchived": TASK_SUPERSET["isArchived"][0],
            "isDeleted": TASK_SUPERSET["isDeleted"][0],
            "dueDate": TASK_SUPERSET["dueDate"][0],
            "expiry": TASK_SUPERSET["expiry"][0],
            "status": TASK_SUPERSET["status"][0],
            "priority": TASK_SUPERSET["priority"][0]           
        }
        self.valid_tasks_list = generate_dataset_from_model(VALID_TASKS, False, False, False)

        INVALID_TASKS = {
            "farmID": self.farm,
            "assignedTo": [self.user],
            "name": TASK_SUPERSET["name"][1],
            "description": TASK_SUPERSET["description"][1],
            "timeStamp": TASK_SUPERSET["timeStamp"][1],
            "isCompleted": TASK_SUPERSET["isCompleted"][1],
            "isArchived": TASK_SUPERSET["isArchived"][1],
            "isDeleted": TASK_SUPERSET["isDeleted"][1],
            "dueDate": TASK_SUPERSET["dueDate"][1],
            "expiry": TASK_SUPERSET["expiry"][1],
            "status": TASK_SUPERSET["status"][1],
            "priority": TASK_SUPERSET["priority"][1]
        }
        self.invalid_tasks_list = generate_dataset_from_model(INVALID_TASKS, False, False, False)

        BOUNDARY_VALID_TASKS = {
            "farmID": self.farm,
            "assignedTo": [self.user],
            "name": TASK_SUPERSET["name"][2],
            "description": TASK_SUPERSET["description"][2],
            "timeStamp": TASK_SUPERSET["timeStamp"][2],
            "isCompleted": TASK_SUPERSET["isCompleted"][2],
            "isArchived": TASK_SUPERSET["isArchived"][2],
            "isDeleted": TASK_SUPERSET["isDeleted"][2],
            "dueDate": TASK_SUPERSET["dueDate"][2],
            "expiry": TASK_SUPERSET["expiry"][2],
            "status": TASK_SUPERSET["status"][2],
            "priority": TASK_SUPERSET["priority"][2]
        }
        self.boundary_valid_task_list = generate_dataset_from_model(BOUNDARY_VALID_TASKS, False, False, False)

        BOUNDARY_INVALID_TASKS = {
            "farmID": self.farm,
            "assignedTo": [self.user],
            "name": TASK_SUPERSET["name"][3],
            "description": TASK_SUPERSET["description"][3],
            "timeStamp": TASK_SUPERSET["timeStamp"][3],
            "isCompleted": TASK_SUPERSET["isCompleted"][3],
            "isArchived": TASK_SUPERSET["isArchived"][3],
            "isDeleted": TASK_SUPERSET["isDeleted"][3],
            "dueDate": TASK_SUPERSET["dueDate"][3],
            "expiry": TASK_SUPERSET["expiry"][3],
            "status": TASK_SUPERSET["status"][3],
            "priority": TASK_SUPERSET["priority"][3]
        }
        self.boundary_invalid_task_list = generate_dataset_from_model(BOUNDARY_INVALID_TASKS, False, False, False)
        
    def create_valid_tasks(self):
        tasks = Task.objects.bulk_create([Task(**task) for task in self.valid_tasks_list])
        return [task.taskID for task in tasks]

    def create_boundary_valid_tasks(self):
        tasks = Task.objects.bulk_create([Task(**task) for task in self.boundary_valid_task_list])
        return [task.taskID for task in tasks]
# ------------------------------- TEST CLASS - CREATE TASKS ------------------------------- #
class CreateTaskTest(BaseTaskTest):

# ------------------------------- TEST CASES - CREATE TASKS (MODELS) ------------------------------- #
    def test_create_valid_task(self):
        errors = []
        # Test the creation of a valid task
        for task in self.valid_tasks_list:
            try:
                createdTask = self.taskmanager.createTask(self, task)
                self.assertTrue(Task.objects.get(taskID=createdTask.taskID))
            except Exception as exception:
                errors.append([task, exception])
        self.assertEqual(errors, [])
        self.assertEqual(len(self.valid_tasks_list),len(Task.objects.all()))

    def test_create_valid_boundary_task(self):
        errors = []
        # Test the creation of a valid task
        for task in self.boundary_valid_task_list:
            try:
                createdTask = self.taskmanager.createTask(self, task)
                self.assertTrue(Task.objects.get(taskID=createdTask.taskID))
            except Exception as exception:
                errors.append([task, exception])

        self.assertEqual(errors, [])
        self.assertEqual(len(self.boundary_valid_task_list),len(Task.objects.all()))

    def test_create_invalid_task(self):
        errors = []
        added = False
        # Test the creation of a valid task
        for task in self.invalid_tasks_list:
            try:
                self.taskmanager.createTask(self, task)
                added = True
                errors.append([task])
            except:
                pass
        #Assert that the invalid tasks were not added to the database.
        self.assertEqual(added, False)      
        self.assertEqual(errors, [])

    def test_create_invalid_boundary_task(self):
        errors = []
        added = False
        # Test the creation of a valid task
        for task in self.boundary_invalid_task_list:
            try:
                self.taskmanager.createTask(self, task)
                added = True
                errors.append([task])
            except:
                pass
        #Assert that the invalid tasks were not added to the database.
        self.assertEqual(added, False)      
        self.assertEqual(errors, [])

# ------------------------------- TEST CASES - CREATE TASKS (FORMS) ------------------------------- #
    def test_create_valid_task_form(self):
        # Tasks created with the form must have a due date in the future in the format dd/mm/yyyy
        errors = []
        # Test the creation of a valid task form
        for task in self.valid_tasks_list:
            #Task form expects date in dd/mm/yyyy format
            task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            try:
                form = createTaskForm(user=self.user, data=task)
                self.assertTrue(form.is_valid())
            except:
                errors.append([task, form.errors])
        self.assertEqual(errors, [])     
   
    def test_create_invalid_task_form(self):
        errors = []
        added = False
        # Test the creation of an invalid task form
        for task in self.invalid_tasks_list:
            try:
                #Task form expects date in dd/mm/yyyy format
                task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                # If the input cannot be converted to datetime, pass
                pass
            try:
                form = createTaskForm(user=self.user, data=task)
                self.assertFalse(form.is_valid())
            except:
                added = True
                errors.append([task, form.errors])
        
        self.assertEqual(added, False)
        self.assertEqual(errors, [])

    def test_create_boundary_valid_task_form(self):
        # Tasks created with the form must have a due date in the future in the format dd/mm/yyyy
        errors = []
        # Test the creation of a valid task form
        for task in self.boundary_valid_task_list:
            #Task form expects date in dd/mm/yyyy format
            task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            try:
                form = createTaskForm(user=self.user, data=task)
                self.assertTrue(form.is_valid())
            except:
                errors.append([task, form.errors])
        self.assertEqual(errors, [])
    
    def test_create_boundary_invalid_task_form(self):
        errors = []
        added = False
        # Test the creation of an invalid task form
        for task in self.boundary_invalid_task_list:
            try:
                #Task form expects date in dd/mm/yyyy format
                task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                # If the input cannot be converted to datetime, pass
                pass
            try:
                form = createTaskForm(user=self.user, data=task)
                self.assertFalse(form.is_valid())
            except:
                added = True
                errors.append([task, form.errors])
        
        self.assertEqual(added, False)
        self.assertEqual(errors, [])


# ------------------------------- TEST CLASS - UPDATE TASKS ------------------------------- #
class UpdateTaskTest(BaseTaskTest):

# ------------------------------- TEST CASES - UPDATE TASKS (MODELS) ------------------------------- #
    def test_update_valid_task(self):
        # Get all valid task IDs
        valid_task_ids = self.create_valid_tasks()

        random.seed(12)
        
        # Choose 5 random tasks to update
        tasks_to_update = random.sample(valid_task_ids, 5)
        
        # Choose 5 random tasks to use as new data
        new_data_tasks = random.sample(valid_task_ids, 5)
        
        errors = []
        for update_id, new_data_id in zip(tasks_to_update, new_data_tasks):
            try:
                # Get the task to update
                task_to_update = Task.objects.get(taskID=update_id)
                
                # Get the new data
                new_data_task = Task.objects.get(taskID=new_data_id)
                
                # Convert the new data task to a dictionary
                new_data = model_to_dict(new_data_task)
                
                # Remove the 'taskID' from new_data as we don't want to update this field
                new_data.pop('taskID', None)
                
                # Handle ForeignKey fields
                new_data['farmID'] = new_data_task.farmID
                new_data['assignedTo'] = new_data_task.assignedTo
                
                # Update the task
                updated_task = self.taskmanager.updateTask(update_id, new_data)
                
                # Refresh the task from the database
                task_to_update.refresh_from_db()

                # Check if the updated task is different from the initial task
                self.assertNotEqual(model_to_dict(task_to_update), model_to_dict(new_data_task))

                # Check if the updated task is the same as the new data
                self.assertEqual(model_to_dict(task_to_update), model_to_dict(updated_task))
                
            except Exception as exception:
                errors.append([update_id, exception])
        
        self.assertEqual(errors, [])

    def test_update_boundary_valid_task(self):
        # Get all valid task IDs
        boundary_valid_task_ids = self.create_boundary_valid_tasks()

        random.seed(12)
        
        # Choose 5 random tasks to update
        tasks_to_update = random.sample(boundary_valid_task_ids, 5)
        
        # Choose 5 random tasks to use as new data
        new_data_tasks = random.sample(boundary_valid_task_ids, 5)
        
        errors = []
        for update_id, new_data_id in zip(tasks_to_update, new_data_tasks):
            try:
                # Get the task to update
                task_to_update = Task.objects.get(taskID=update_id)
                
                # Get the new data
                new_data_task = Task.objects.get(taskID=new_data_id)
                
                # Convert the new data task to a dictionary
                new_data = model_to_dict(new_data_task)
                
                # Remove the 'taskID' from new_data as we don't want to update this field
                new_data.pop('taskID', None)
                
                # Handle ForeignKey fields
                new_data['farmID'] = new_data_task.farmID
                new_data['assignedTo'] = new_data_task.assignedTo
                
                # Update the task
                updated_task = self.taskmanager.updateTask(update_id, new_data)
                
                # Refresh the task from the database
                task_to_update.refresh_from_db()

                # Check if the updated task is different from the initial task
                self.assertNotEqual(model_to_dict(task_to_update), model_to_dict(new_data_task))

                # Check if the updated task is the same as the new data
                self.assertEqual(model_to_dict(task_to_update), model_to_dict(updated_task))
                
            except Exception as exception:
                errors.append([update_id, exception])
        
        self.assertEqual(errors, [])

    def test_update_invalid_task(self):
        # Get all valid task IDs
        valid_task_ids = self.create_valid_tasks()

        # Get all invalid data
        invalid_task_data = self.invalid_tasks_list

        random.seed(12)
        
        # Choose 5 random tasks to update
        tasks_to_update = random.sample(valid_task_ids, 5)
        
        # Choose 5 random tasks to use as new data
        new_data_tasks = random.sample(invalid_task_data, 5)
        
        errors = []
        added = False
        for update_id, new_task_data in zip(tasks_to_update, new_data_tasks):
            # Get the task to update
            task_to_update = Task.objects.get(taskID=update_id)

            try:
                with transaction.atomic(): # Rollback the transaction in case of an error
                    # Update the task
                    updated_task = self.taskmanager.updateTask(update_id, new_task_data)
                    
                    # Refresh the task from the database
                    task_to_update.refresh_from_db()

                    # Check if the updated task is different from the initial task
                    self.assertNotEqual(model_to_dict(task_to_update), model_to_dict(new_task_data))

                    # Check if the updated task is the same as the new data
                    self.assertEqual(model_to_dict(task_to_update), model_to_dict(updated_task))

                    # If the task was updated, set added to True
                    added = False
                    errors.append([task_to_update, new_task_data])
            except:
                pass
        #Assert that the invalid tasks were not added to the database.
        self.assertEqual(added, False)      
        self.assertEqual(errors, [])

    def test_update_boundary_invalid_task(self):
        # Get all valid task IDs
        valid_task_ids = self.create_valid_tasks()

        # Get all invalid data
        invalid_task_data = self.boundary_invalid_task_list

        random.seed(12)
        
        # Choose 5 random tasks to update
        tasks_to_update = random.sample(valid_task_ids, 5)
        
        # Choose 5 random tasks to use as new data
        new_data_tasks = random.sample(invalid_task_data, 5)
        
        errors = []
        added = False
        for update_id, new_task_data in zip(tasks_to_update, new_data_tasks):
            # Get the task to update
            task_to_update = Task.objects.get(taskID=update_id)

            try:
                with transaction.atomic(): # Rollback the transaction in case of an error
                    # Update the task
                    updated_task = self.taskmanager.updateTask(update_id, new_task_data)
                    
                    # Refresh the task from the database
                    task_to_update.refresh_from_db()

                    # Check if the updated task is different from the initial task
                    self.assertNotEqual(model_to_dict(task_to_update), model_to_dict(new_task_data))

                    # Check if the updated task is the same as the new data
                    self.assertEqual(model_to_dict(task_to_update), model_to_dict(updated_task))

                    # If the task was updated, set added to True
                    added = False
                    errors.append([task_to_update, new_task_data])
            except:
                pass
        #Assert that the invalid tasks were not added to the database.
        self.assertEqual(added, False)      
        self.assertEqual(errors, [])

# ------------------------------- TEST CASES - UPDATE TASKS (FORMS) ------------------------------- #
    def test_update_valid_task_form(self):
        # Confirm that the task update form is valid when given valid data
        errors = []
        # Test the creation of a valid task form
        for task in self.valid_tasks_list:
            #Task form expects date in dd/mm/yyyy format
            task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            try:
                form = taskForm(user=self.user, data=task)
                self.assertTrue(form.is_valid())
            except:
                errors.append([task, form.errors])
        self.assertEqual(errors, [])  

    def test_update_invalid_task_form(self):
        # Confirm that the task update form is invalid when given invalid data
        errors = []
        added = False
        # Test the creation of an invalid task form
        for task in self.invalid_tasks_list:
            try:
                #Task form expects date in dd/mm/yyyy format
                task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                # If the input cannot be converted to datetime, pass
                pass
            try:
                form = taskForm(user=self.user, data=task)
                self.assertFalse(form.is_valid())
            except:
                added = True
                errors.append([task, form.errors])
        
        self.assertEqual(added, False)
        self.assertEqual(errors, [])

    def test_update_boundary_valid_task_form(self):
        # Confirm that the task update form is valid when given valid boundary data
        errors = []
        # Test the creation of a valid task form
        for task in self.boundary_valid_task_list:
            #Task form expects date in dd/mm/yyyy format
            task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            try:
                form = createTaskForm(user=self.user, data=task)
                self.assertTrue(form.is_valid())
            except:
                errors.append([task, form.errors])
        self.assertEqual(errors, [])
    
    def test_update_boundary_invalid_task_form(self):
        # Confirm that the task update form is invalid when given invalid boundary data
        errors = []
        added = False
        # Test the creation of an invalid task form
        for task in self.boundary_invalid_task_list:
            try:
                #Task form expects date in dd/mm/yyyy format
                task["dueDate"] = dt.datetime.strptime(task["dueDate"], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                # If the input cannot be converted to datetime, pass
                pass
            try:
                form = createTaskForm(user=self.user, data=task)
                self.assertFalse(form.is_valid())
            except:
                added = True
                errors.append([task, form.errors])
        
        self.assertEqual(added, False)
        self.assertEqual(errors, [])  

# ------------------------------- TEST CLASS - DELETE TASKS ------------------------------- #
class DeleteTaskTest(BaseTaskTest):

# ------------------------------- TEST CASES - DELETE TASKS (MODELS) ------------------------------- #
    def test_delete_valid_task(self):
        # Get all valid task IDs
        valid_task_ids = self.create_valid_tasks()

        random.seed(12)
        
        # Choose 5 random tasks to delete
        tasks_to_delete = random.sample(valid_task_ids, 5)
        
        errors = []
        for task_id in tasks_to_delete:
            try:
                task_to_delete = Task.objects.get(taskID=task_id)

                # Delete the task - deleteTask completes a soft delete
                self.taskmanager.deleteTask(task_id)
                
                # Check if the task was deleted
                self.assertTrue(task_to_delete.isDeleted == True)
                
            except Exception as exception:
                errors.append([task_id, exception])
        
        self.assertEqual(errors, [])
    
    def test_delete_boundary_valid_task(self):
        # Get all valid task IDs
        boundary_valid_task_ids = self.create_boundary_valid_tasks()

        random.seed(12)
        
        # Choose 5 random tasks to delete
        tasks_to_delete = random.sample(boundary_valid_task_ids, 5)
        
        errors = []
        for task_id in tasks_to_delete:
            try:
                task_to_delete = Task.objects.get(taskID=task_id)

                # Delete the task - deleteTask completes a soft delete
                self.taskmanager.deleteTask(task_id)
                
                # Check if the task was deleted
                self.assertTrue(task_to_delete.isDeleted == True)
                
            except Exception as exception:
                errors.append([task_id, exception])
        
        self.assertEqual(errors, [])

    def test_delete_deleted_task(self):
        # Get all valid task IDs
        valid_task_ids = self.create_valid_tasks()

        random.seed(12)
        
        # Choose 5 random tasks to delete
        tasks_to_delete = random.sample(valid_task_ids, 5)
        
        errors = []
        for task_id in tasks_to_delete:
            task_to_delete = Task.objects.get(taskID=task_id)
            task_to_delete.isDeleted = True # Set the task to deleted            
            try: # Try to delete the task

                # Delete the task - deleteTask completes a soft delete
                self.taskmanager.deleteTask(task_id)
                
                # Check if the task was deleted
                self.assertTrue(task_to_delete.isDeleted == True)
                
            except Exception as exception:
                errors.append([task_id, exception])
        
        self.assertEqual(errors, [])
    
    def test_delete_nonexistent_task(self):
        # Get all valid task IDs
        valid_task_ids = self.create_valid_tasks()

        invalid_id = max(valid_task_ids) + 1
        try:
            self.taskmanager.deleteTask(invalid_id)
        except:
            self.fail("Exception Raised. Error not handled gracefully.")