"""
Views for UserAuth.
"""

# Imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # This indicates that logging in is required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import SignUserUpForm, UserLoginForm

from FarmAcc.views import FarmManager
from UserAuth.models import UserProfile


def signup(request: HttpRequest):
    """
    This view renders the sign up page which allows users to signup and create a new farming tenant.
    """
    farmManager = FarmManager()

    # Disallow users to visit the signup page if they are already authenticated. Redirects them to
    # the dashboard straight away.
    if request.user.is_authenticated:
        return render(request, "Dashboard/baseDash.html")

    # Handle 'POST' requests
    if request.method == "POST":
        submittedForm = SignUserUpForm(request.POST)

        if submittedForm.is_valid():
            submittedForm.save()
            messages.success(
                request,
                f"Account was generated for {submittedForm.cleaned_data.get('username')}"
            )

            # Sign in the user and redirect them to the create/join farm page
            user = authenticate(username=submittedForm.cleaned_data.get('username'), password=submittedForm.cleaned_data.get('password1'))
            login(request, user)
            return redirect("/farm/join")
        
        else: #Signup is invalid

            # I didn't understand the point of the following code, so I simplified it
            error_messages = [error for _, errors in submittedForm.errors.items() for error in errors]

            # Add collected error messages to the messages framework
            for error in error_messages:
                messages.error(request, error)

            context = {
                "form": submittedForm
            }

            return render(request, "UserAuth/signup.html", context)
        
    # Handle 'GET' Requests
    form = SignUserUpForm()

    context = {
        "form": form
    }

    return render(request, "UserAuth/signup.html", context)


def logoutUser(request: HttpRequest):
    """
    This view allows a givn user to log out from the application and redirects
    them to the login page.
    """

    logout(request)

    return redirect("login")

def loginPage(request: HttpRequest):
    """
    This view renders the login page, allowing users to authenticate themselves and login to the
    platform.
    """
    farmManager = FarmManager()

    # Handle 'POST' requests
    
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            # Extract the username and password from the form
            userName     = form.cleaned_data["username"]
            userPassword = form.cleaned_data["password"]

        # If a user with the given username exists, authenticate the password.
        if UserProfile.objects.filter(username=userName).exists():

            # If the user exists and is not active, activate the user so they can create or join a
            # new farm. This happens when the user has been deactivated from all their farms.
            if UserProfile.objects.get(username=userName).is_active is False:
                inactive_user = UserProfile.objects.get(username=userName)
                inactive_user.is_active = True
                inactive_user.save()

            # If the password is correct, log the user in and redirect them to the appropriate page.
            user = authenticate(username=userName, password=userPassword)

            if user is not None:

                # Get the user's active farms
                user_farms = farmManager.get_user_active_farms(user)
                login(request, user)

                match len(user_farms):
                    case 0: # If the user has no active farms, redirect them to the join farm page.
                        return redirect("farm/join")
                    case 1: # If the user has one active farm, redirect them to the dashboard of that farm.
                        return redirect("home", farm_id = user_farms[0].id)
                    case _: # If the user has multiple active farms, redirect them to the choose farm page.
                        return redirect("farm/choose-farm")

            # If the password is incorrect, provide an error message to the user.
            messages.add_message(
                request                                      ,
                level=messages.ERROR                         ,
                message="Password or username was incorrect.",
                extra_tags="error"
            )

        else:
            # If the user does not exist, provide an error message to the user.
            messages.add_message(
                request                                      ,
                level=messages.ERROR                         ,
                message="Password or username was incorrect.",
                extra_tags="error"
            )

        return redirect("login")
    
    # Handle 'GET' Requests
    form = UserLoginForm()
    
    context = {
        "form": form
    }

    return render(request, "UserAuth/login.html", context)
