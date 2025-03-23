"""
Views for the task and kanban board functionality.
"""

# Imports
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from UserAuth.models import UserProfile

from .forms import createTaskForm, taskForm, createKanbanForm, deleteKanbanForm, createKanbanContentForm, updateKanbanContentForm
from .models import Task, Kanban, KanbanContents

import json


# Task Manager
class taskManager():
    """
    Enables a user to manage tasks, including creation, updating and deletion.
    implements various task Forms
    """

    def getTasks(self, user):
        """
        Returns the tasks assigned to the current user
        """

        tasks = Task.objects                                                      \
            .filter(assignedTo=user.id, isDeleted=False, farmID=user.currentFarm) \
            .values()                                                             \
            .order_by("dueDate")

        if len(tasks) == 0:
            return ""

        for i, t in enumerate(tasks):
            try:
                tasks[i]["status" ] = Task.TASK_STATUS_CHOICES[t["status"]][1]
                tasks[i]["dueDate"] = tasks[i]["dueDate"].strftime("%d/%m/%Y")
            except IndexError as err:
                print(err)
                return ""

        return tasks

    def getTasksByDate(self, user, date):
        """
        Returns the tasks assigned to the current user
        """

        tasks = Task.objects                                                                    \
            .filter(assignedTo=user.id, isDeleted=False, farmID=user.currentFarm, dueDate=date) \
            .values()                                                                           \
            .order_by("dueDate")

        if len(tasks) == 0:
            return ""

        for i, t in enumerate(tasks):
            try:
                tasks[i]["status" ] = Task.TASK_STATUS_CHOICES[t["status"]][1]
                tasks[i]["dueDate"] = tasks[i]["dueDate"].strftime("%d/%m/%Y")
            except IndexError as err:
                print(err)
                return ""

        return tasks

    def createTask(self, request, taskData):
        """
        creates a new task entry in the database.

        (docstring needed rewrite, sorry.)
        """

        taskData["farmID"] = request.user.currentFarm
        if taskData["assignedTo"] == "":
            taskData["assignedTo"] = request.user.id

        task = Task.objects.create(**taskData)
        # .save() seemed to want to have a taskID provided, even though this is a new entry and
        # therefore is supposed to be auto incremented, so using create here instead.
        return task

    def updateTask(self, taskID: int, taskData: dict):
        """
        Updates a specific single task in the database.

        (Docstring needed rewrite, sorry.)
        """

        if not (Task.objects.filter(taskID=taskID).exists()):
            return {"err": "This task does not exist"}

        targetTask = Task.objects.get(taskID=taskID)

        # Update all provided fields
        for key, val in taskData.items():
            setattr(targetTask, key, val)
        targetTask.save()

        return targetTask

    def deleteTask(self, taskID):
        """
        Soft deletes a task from the database by setting `isDelete = True`
        """

        if not Task.objects.filter(taskID=taskID).exists():
            return {"err": "This task does not exist"}

        targetTask = Task.objects.get(taskID=taskID)
        targetTask.isDeleted = True
        targetTask.save()

        # Remove the task from kanban boards
        kanbanContents = KanbanContents.objects.filter(taskID=taskID).delete()


# Task Views
@login_required(login_url="login")
def taskTableManagement(request):
    taskManagement = taskManager()
    creationForm   = createTaskForm(request.user)
    tasks          = taskManagement.getTasks(request.user)

    if request.method == "POST":
        creationFormPost = createTaskForm(request.user, request.POST)
        if "createTask" in request.POST:
            if creationFormPost.is_valid():
                taskManagement.createTask(request, creationFormPost.cleaned_data)
                messages.add_message(request, messages.SUCCESS, "New Task Added.")
                return redirect("/tasks/tableView")
            else:
                print(creationFormPost.errors)
                context = {
                    "creationForm": creationFormPost       ,
                    "error"       : creationFormPost.errors,
                    "TaskData"    : tasks
                }

                return render(request, "Tasks/taskTable.html", context)

    context = {
        "creationForm": creationForm,
        "TaskData"    : tasks
    }

    return render(request, "Tasks/taskTable.html", context)

@login_required(login_url="login")
def taskUpdatePage(request, taskID: int):
    targetTask          = Task.objects.get(taskID=taskID)
    targetTask.dueDate  = targetTask.dueDate.strftime("%d/%m/%Y")
    updateTask          = taskForm(request.user, initial=model_to_dict(targetTask))

    context = {
        "updateForm": updateTask,
        "targTask"  : targetTask
    }

    if not Task.objects.filter(taskID=taskID).exists():
        return HttpResponseRedirect(request.session["http_referer"])

    if request.method == "POST":
        taskManagement = taskManager()
        updateTaskPost = taskForm(request.user, request.POST)

        if "updateTask" in request.POST:
            if updateTaskPost.is_valid():
                targetTask = taskManagement.updateTask(taskID, updateTaskPost.cleaned_data)
                messages.add_message(request, messages.SUCCESS, "Task Details Updated.")
                return redirect(f"/tasks/updateTask/{taskID}")
            else:
                context = {
                    "updateForm": updateTaskPost,
                    "error"     : updateTaskPost.errors,
                }

                return render(request, "Tasks/updateTask.html", context)
        elif "deleteTask" in request.POST:
            taskManagement.deleteTask(taskID)
            messages.add_message(request, messages.WARNING, "Task Deleted.")
            return redirect("/tasks/tableView")

    return render(request, "Tasks/updateTask.html", context=context)


def nullTaskUpdatePage(request):
    return redirect("/tasks/tableView")


# Kanbans
@login_required(login_url="login")
def kanbanTable(request):
    """
    A page containing a table of all the kanban boards.
    """

    if request.method =="POST":
        kanbanForm = createKanbanForm(request.POST)

        if kanbanForm.is_valid():
            newKanban           = kanbanForm.cleaned_data
            newKanban["farmID"] = request.user.currentFarm

            Kanban.objects.create(**newKanban)

            messages.add_message(request, messages.SUCCESS, "New Kanban board created.")

    # Query the database
    kanbanQuerySet = Kanban.objects.filter(
        farmID  = request.user.currentFarm_id,
        deleted = False
    )
    kanbanContentsQuerySet = KanbanContents.objects.all()

    # Initialise all the counters
    statuses = {}
    for kanban in kanbanQuerySet:
        statuses[kanban.kanbanID] = [0] * 5

    # Count the number of tasks of each status per kanban board
    for content in kanbanContentsQuerySet:
        if not content.kanbanID.deleted:
            statuses[content.kanbanID.kanbanID][content.taskID.status] += 1

    # Pull the data together
    kanbans = [
        tuple([kanban.kanbanID, kanban.name] + statuses[kanban.kanbanID])
        for kanban in kanbanQuerySet
    ]

    # Render page with the data
    context = {
        "Kanbans"         : kanbans         ,
        "createKanbanForm": createKanbanForm
    }

    return render(request, "Tasks/kanbanTable.html", context)


@login_required(login_url="login")
def kanbanBoard(request):
    """
    A page viewing a singular kanban board.
    """

    curKanbanID = request.COOKIES.get("curKanbanID") # Omitting URL params, for better or worse
    # Should really add an error message if the cookie doesn't exist

    kanban                 = Kanban.objects.get(kanbanID=curKanbanID)
    kanbanContentsQuerySet = KanbanContents.objects.filter(kanbanID=curKanbanID)
    name                   = kanban.name

    bucketNames = {
        "Not Started": "notStarted",
        "In Progress": "inProgress",
        "Blocked"    : "blocked"   ,
        "Review"     : "review"    ,
        "Complete"   : "complete"
    }

    cardInfoList = [
        (
            content.taskID.status             ,
            content.order                     ,
            content.taskID.taskID             ,
            content.taskID.assignedTo.username,
        str(content.taskID.dueDate)           ,
            content.taskID.name               ,
            content.taskID.description
        )
        for content
        in  kanbanContentsQuerySet
        if  content.taskID.status < 5
    ]
    cardInfoList = sorted(cardInfoList, key = lambda x: (x[0], x[1]))

    # Get the unused tasks
    kanbanTaskIDs = [content.taskID.taskID for content in kanbanContentsQuerySet]
    taskQuerySet  = Task.objects.filter(
        isDeleted=False, farmID=request.user.currentFarm
    ).values(
        "taskID"     ,
        "status"     ,
        "name"       ,
        "description",
        "assignedTo" ,
        "dueDate"
    )
    tasks = list(taskQuerySet)
    # Filter out already present tasks
    utasks = [task for task in tasks if task["taskID"] not in kanbanTaskIDs]

    # Clean the unused tasks
    for idx, task in enumerate(utasks):
        utasks[idx]["assignedTo" ] = UserProfile.objects.get(id=task["assignedTo"]).username
        utasks[idx]["dueDate"    ] = str(utasks[idx]["dueDate"])
        utasks[idx]["displayText"] = \
            f"{utasks[idx]['name']} - {utasks[idx]['assignedTo']} - {utasks[idx]['dueDate']}"

    # Sort the utasks by dueDate then assignedTo, so they're grouped by user
    utasks = sorted(utasks, key=lambda x: x["dueDate"   ])
    utasks = sorted(utasks, key=lambda x: x["assignedTo"])

    # Build context
    context = {
        "Name"        : name        ,
        "UTasks"      : utasks      ,
        "BucketNames" : bucketNames ,
        "CardInfoList": cardInfoList
    }

    return render(request, "Tasks/kanbanView.html", context)


@login_required(login_url="login")
def deleteKanban(request):
    if request.method == "POST":
        # Form + .is_valid() didn't work
        deleteKanbanByID(int(request.POST["kanbanID"]))

        messages.add_message(request, messages.SUCCESS, "Kanban board deleted.")

        return redirect("/tasks/kanbanTable")


@login_required(login_url="login")
def updateKanban(request):
    """
    Updating the kanban board.

    Desired format
        cards: [
            {
                taskID:int,
                order :int,
                status:int
            }
        ]
    """

    if request.method == "POST":
        try:
            # Get the json asap, no point processing anything else if this is going to fail
            # Should probably do validation here, everything just needs to be a integer
            #   (taskID > 0 and order >= 0 and status >= 0)
            try:
                newKanbanContentsList = json.loads(request.POST.get("cards"))
            except json.JSONDecodeError:
                print("updateKanban failed during json load")
                return JsonResponse({
                    "status" : "error"       ,
                    "message": "Invalid data"
                }, status=400)
            newKanbanContentsList = sorted(newKanbanContentsList, key=lambda x: x["taskID"])

            curKanbanID            = request.COOKIES.get("curKanbanID")
            kanbanContentsQuerySet = KanbanContents.objects \
                .filter(kanbanID=curKanbanID).order_by("taskID")
            oldKanbanContentsList  = list(kanbanContentsQuerySet)

            # Update the state of the kanban, content by content
            while len(newKanbanContentsList) + len(oldKanbanContentsList) > 0:
                # Explicit conditions, could be refactored shorter
                if   len(oldKanbanContentsList) == 0:
                    createKanbanContents(newKanbanContentsList, oldKanbanContentsList, curKanbanID)
                elif len(newKanbanContentsList) == 0:
                    deleteKanbanContents(newKanbanContentsList, oldKanbanContentsList)
                elif newKanbanContentsList[0]["taskID"] <  oldKanbanContentsList[0].taskID.taskID:
                    createKanbanContents(newKanbanContentsList, oldKanbanContentsList, curKanbanID)
                elif newKanbanContentsList[0]["taskID"] >  oldKanbanContentsList[0].taskID.taskID:
                    deleteKanbanContents(newKanbanContentsList, oldKanbanContentsList)
                elif newKanbanContentsList[0]["taskID"] == oldKanbanContentsList[0].taskID.taskID:
                    updateKanbanContents(newKanbanContentsList, oldKanbanContentsList)
                else:
                    print("updateKanban failed during the save loop")
                    return JsonResponse({
                        "status" : "error"                                                             ,
                        "message": "Something has gone horrifically wrong in Tasks.views.updateKanban."
                    }, status=400)

            return JsonResponse({
                "status" : "success"                        ,
                "message": "Kanban board saved successfully",
                "success": True
            }, status=200)

        except Exception as err:
            print(f"updateKanban failed with {err = }")
            return JsonResponse({
                "status" : "error"              ,
                "message": "Save attempt failed"
            }, status=400)

    return JsonResponse({
        "status" : "error"               ,
        "message": "Invalid request type"
    }, status=400)


# Move these into a manager classes?
def deleteKanbanByID(kanbanID):
    kanban         = Kanban.objects.get(kanbanID=kanbanID)
    kanban.deleted = True
    kanban.save()


def createKanbanContents(newKanbanContentsList, _, curKanbanID):
    """
    Create a new kanbanContents, a relation between a task and a Kanban board.
    """

    newKanbanContent = newKanbanContentsList.pop(0)

    # Form + .is_valid() didn't work here
    newKanbanContentInstance = KanbanContents(
        kanbanID = Kanban.objects.get(kanbanID=curKanbanID)           ,
        taskID   = Task.objects.get(taskID=newKanbanContent["taskID"]),
        order    = newKanbanContent["order" ]
    )
    newKanbanContentInstance.save()

    task = Task.objects.get(
        taskID = newKanbanContent["taskID"]
    )
    task.status = newKanbanContent["status"]
    task.save()


def updateKanbanContents(newKanbanContentsList, oldKanbanContentsList):
    """
    Update an already existing kanbanContents.
    """

    oldKanbanContent = oldKanbanContentsList.pop(0)
    newKanbanContent = newKanbanContentsList.pop(0)

    # Form + .is_valid() didn't work here
    content       = KanbanContents.objects.get(kanbanContentsID=oldKanbanContent.kanbanContentsID)
    content.order = newKanbanContent["order"]
    content.save()

    task        = Task.objects.get(taskID=content.taskID.taskID)
    task.status = newKanbanContent["status"]
    task.save()


def deleteKanbanContents(_, oldKanbanContentsList):
    """
    Delete a kanbanContents permanently. Uses hard deleted instead of soft delete since this a
    relation rather than new data.

    No form validation, the data handled here comes from the database instead of the client.
    """

    oldKanbanContent = oldKanbanContentsList.pop(0)

    KanbanContents.objects.get(kanbanContentsID=oldKanbanContent.kanbanContentsID).delete()
