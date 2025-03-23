# Standard library imports
from datetime import datetime
import json

# Django imports
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder

# Local imports
from .forms import addWidgetForm, myTasksDateForm
from .models import DashboardLayout, Widget
from .widgets import get_widget_instance, get_widget_class, get_updated_scope, MyTasks
from FarmAcc.views import FarmManager
from assetOperation.views import get_user_current_checkouts_oldest
from assetOperation.models import OperationLog
from .weatherAPI import WeatherManager

# This view is responsible for rendering the main dashboard page and handling the addition of new widgets.
@login_required(login_url='login')
def mainDash(request, farm_id):

    #WeatherAPI configured on GET request
    weather = WeatherManager()
    try:
        weather.main()
    except:
        print("Error Getting Weather Data")
    
    # Initialise the farmManager and set the current farm for the user (this is done after login when the user is redirected to the dashboard)
    farmManager = FarmManager()
    current_user = request.user
    farmManager.set_user_current_farm_by_id(current_user, farm_id)

    # Get the dashboard layout for the current farm or create a new one if it doesn't exist
    dashboard, created = DashboardLayout.objects.get_or_create(farm=current_user.currentFarm)

    # Add the default dashboard layout to the farm dashboard if it was just created
    if created:
        create_default_dashboard(request.user, dashboard)

    # Handle the addition of a new widget
    if request.method == "POST":
        newWidgetForm = addWidgetForm(request.POST)

        if newWidgetForm.is_valid():
            # Get the widget instance based on the widget name. Returns the class instance of the widget.
            widget_name = newWidgetForm.cleaned_data['widget_name']
            widget_instance = get_widget_instance(widget_name)

            if widget_instance:
                # The weather widget requires the weather data to be set before creating the widget using specific methods
                # This does not fail gracefully if the weather data is not available - However it does not break the dashboard or result in the server crashing.
                if widget_instance.type == "weatherWidgetSmall":
                    try: 
                        weatherData = weather.currentWeatherWidget(weather.getCurrLocation()['geographicLocation'])
                        widget_instance.set_data(request.user, weatherData = weatherData)
                    except:
                        weatherData = {
                            'retrievalTime': "N/A",
                            'geographicLocation': "Error Obtaining Data",
                            'currentTemp': "N/A",
                            'feelsLike': "N/A",
                            'humidity': "N/A",
                            'sunrise': "N/A",
                            'sunset': "N/A",
                            'weather': "N/A",
                            'description': "N/A",
                            "weatherIcon": "N/A",
                        }
                        widget_instance.set_data(request.user, weatherData = weatherData)

                elif widget_instance.type == "weatherWidgetWeek":
                    try:
                        weatherData = weather.fiveDayForecastWidget(weather.getCurrLocation()['geographicLocation'])
                        widget_instance.set_data(request.user, weatherData = weatherData)
                    except:
                        widget_instance.set_data(request.user, weatherData = None)
                else:
                    # For other widgets, set the data using the default method
                    widget_instance.set_data(request.user)
                
                # Create the widget object and add it to the dashboard object in the database
                widget = Widget.objects.create(
                    name=widget_name,
                    type=widget_instance.type,
                    sizex = widget_instance.col,
                    sizey = widget_instance.row,
                    scope=widget_instance.get_context()
                )
                dashboard.widgets.add(widget)

                # Return the widget data in JSON format to be rendered in the frontend (through dashing-config.js)
                return JsonResponse({
                    'success': True,
                    'widget': {
                        'id': widget.id,
                        'name': widget.name,
                        'type': widget.type,
                        'sizex': widget.sizex,
                        'sizey': widget.sizey,
                        'scope': widget.scope,
                    }
                }, encoder=DjangoJSONEncoder)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid widget type'}, status=400)
        return JsonResponse({'success': False, 'errors': newWidgetForm.errors}, status=400)

    context = {
        "addWidgetForm": addWidgetForm(),
        "myTasksDateForm": myTasksDateForm(),
        "dashboard": dashboard,
    }
    return render(request, "Dashboard/baseDash.html", context)


# This view is responsible for creating the default dashboard layout for a new farm.
def create_default_dashboard(user, dashboard):
    default_widgets = ['My Tasks'] # Add the default widgets here

    for widget_name in default_widgets:
        widget_instance = get_widget_instance(widget_name)

        if widget_instance:
            widget_instance.set_data(user) 
            #If weather widgets are added as the default, the weather data will need to be set differently.
            # Refer to the mainDash view for an example of how to set the weather data for the weather widgets.

            widget = Widget.objects.create(
                name=widget_name,
                type=widget_instance.type,
                sizex = widget_instance.col,
                sizey = widget_instance.row,
                scope=widget_instance.get_context(),
                saved=True
            )
            dashboard.widgets.add(widget)

    dashboard.save()


# This view is responsible for saving the layout of the dashboard when the save button is clicked.
@csrf_exempt
def save_layout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            layout_data = data.get('layout', [])
            widget_data = data.get('widgets', [])

            # Update the layout data in the database
            dashboard = DashboardLayout.objects.get(farm=request.user.currentFarm)
            dashboard.layout_data = layout_data
            dashboard.save()

            # Update the widget positions in the database
            for widget in widget_data:
                Widget.objects.filter(id=widget['id']).update(
                    col=widget['col'],
                    row=widget['row'],
                    sizex=widget['sizex'],
                    sizey=widget['sizey'],
                    saved=True
                )

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({
                'status' : 'error',
                'message': 'Invalid data'
            }, status=400)
    return JsonResponse({
        'status' : 'error',
        'message': 'Invalid request'
    }, status=400)


# This view is responsible for getting the layout of the dashboard when the page is loaded.
@csrf_exempt
def get_layout(request):
    if request.method == 'GET':
        try:
            # Get the layout and widgets for the current farm
            dashboard = DashboardLayout.objects.get(farm=request.user.currentFarm)
            widgets = []
            
            # Get the saved widgets from the database. If a widget is not saved, it is removed from the dashboard and deleted.
            for widget in dashboard.widgets.all():
                if widget.saved:
                    widgets.append(widget)
                else:
                    dashboard.widgets.remove(widget)
                    widget.delete()

            widget_data = []
            for widget in widgets:
                widget_class = get_widget_class(widget.type)
                if widget_class:
                    widget_instance = widget_class()

                    # Everytime the dashboard page is loaded, the data displayed in the widgets is updated.
                    updated_scope = get_updated_scope(widget.scope, request.user, widget_instance)

                    # Widget data is sent to the frontend via a JSON response (handled by dashing-config.js)
                    widget_data.append({
                        'id'   : widget.id    ,
                        'name' : widget.name  ,
                        'type' : widget.type  ,
                        'scope': updated_scope,
                        'col'  : widget.col   ,
                        'row'  : widget.row   ,
                        'sizex': widget.sizex ,
                        'sizey': widget.sizey
                    })

            return JsonResponse({
                'layout' : dashboard.layout_data,
                'widgets': widget_data
            })
        except DashboardLayout.DoesNotExist:
            return JsonResponse({
                "layout" : None,
                "widgets": None,
                "message": "Layout does not exist"
            })
    return JsonResponse({
        'status' : 'error',
        'message': 'Invalid request'
    }, status=400)


# This view is responsible for deleting a widget from the dashboard.
@login_required(login_url="login")
@require_POST
@csrf_exempt
def delete_widget(request):
    # Get the unique widget id from the request
    widget_id = request.POST.get('widget_id')
    try:
        # Using the widget id, get the widget object and the dashboard object
        widget = Widget.objects.get(id=widget_id)
        dashboard = DashboardLayout.objects.get(farm=request.user.currentFarm)

        # Remove the widget from the dashboard
        dashboard.widgets.remove(widget)

        # Delete the widget
        widget.delete()

        # Save the dashboard to update its configuration
        dashboard.save()

        return JsonResponse({'success': True})
    except Widget.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Widget not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# This view is responsible for updating the data in the My Tasks widget when the date is changed.
@login_required(login_url="login")
@require_POST
def update_my_tasks(request):
    # Get the date and widget id from the request
    date_str = request.POST.get('date')
    widgetId = request.POST.get('id')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        widgetInstance = Widget.objects.get(id=widgetId)

        # Create a new MyTasks widget instance and update the data based on the date.
        my_tasks_widget = MyTasks()
        updated_data = my_tasks_widget.set_data(request.user, date)

        # Update the existing widget scope with the new data
        widgetInstance.scope['data'] = updated_data
        widgetInstance.save()

        # Return the updated data in JSON format to be rendered in the frontend (through dashing-config.js)
        return JsonResponse({'success': True, 'data': updated_data})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)

# This view is responsible for getting the current checkouts of the user to dynamically display in the My Checkouts widget.   
@login_required(login_url="login")
def get_my_checkouts(request):
    # Get the current checkouts of the user, ordered by the oldest checkout first
    checkouts = get_user_current_checkouts_oldest(request.user)

    # Format the data to be displayed in the My Checkouts widget
    data = [
        {
            'label': checkout.assetID.assetName,
            'value': {
                'startTime': checkout.startDateTime.strftime("%d/%m/%y %I:%M %p"),
                'logID': checkout.logID,
                'logNotes': checkout.notes
            }
        }
        for checkout in checkouts
    ]

    # Return the data in JSON format to be rendered in the frontend (through dashing-config.js)
    return JsonResponse({'success': True, 'data': data})
    
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)