"""
Widgets for the dashboard.
"""

# Imports
from dashing.widgets import Widget
from assetOperation.views import get_user_current_checkouts_oldest
from Tasks.views import taskManager
from .weatherAPI import WeatherManager
import datetime as dt


# Classes
class MyCheckouts(Widget):
    title     = 'My Checkouts'
    more_info = 'All assets that I have currently checked out'
    type      = 'myCheckouts'
    col       = 2
    row       = 1

    def set_data(self, user, date = None):
        checkouts = get_user_current_checkouts_oldest(user)
        self.data = [
            {
                'label': checkout.assetID.assetName,
                'value': {
                    'startTime': checkout.startDateTime.strftime("%d/%m/%y %I:%M %p"),
                    'location'   : checkout.location,
                    'notes': checkout.notes
                    }  
            }
            for checkout in checkouts
        ]

        return self.data

    def get_context(self):
        return {
            'title'    : self.title,
            'more_info': self.more_info,
            'type'     : self.type,
            'data'     : self.data
        }


class MyTasks(Widget):
    title     = "My Tasks"
    more_info = "Tasks I have been assigned"
    type      = "myTasks"
    col       = 1
    row       = 2

    priority_colours = {
        0: "low"   ,
        1: "medium",
        2: "high"  ,
        3: "urgent"
    }

    def set_data(self, user, date = None):
        taskController = taskManager()
        if date:
            allTasks = taskController.getTasksByDate(user, date)[:12]
        else:
            date = dt.date.today()
            allTasks = taskController.getTasksByDate(user, date)[:12]

        self.data = [
            {
                'label': task['name'],
                'value': {
                    'status'  : task['status'],
                    'priority': self.priority_colours.get(task['priority'])
                }
            }
            for task in allTasks
        ]

        return self.data

    def get_context(self):
        return {
            'title'    : self.title,
            'more_info': self.more_info,
            'type'     : self.type,
            'data'     : self.data
        }


class weatherWidgetSmall(Widget):
    title     = "Weather (Small)"
    more_info = "Current weather information"
    type      = "weatherWidgetSmall"
    col       = 1
    row       = 1

    def set_data(self, user = None, weatherData = None):
        if weatherData:

            self.data = [
                {'label': 'Weather Data',
                'value': 
                    {
                        'retreivalTime': weatherData['retrievalTime'],
                        'location': weatherData['geographicLocation'],
                        'currentTemp': weatherData['currentTemp'],
                        'feelsLike': weatherData['feelsLike'],
                        'humidity': weatherData['humidity'],
                        'sunrise': weatherData['sunrise'],
                        'sunset': weatherData['sunset'],
                        'weather': weatherData['weather'],
                        'description': weatherData['description'],
                        'weatherIcon': weatherData['weatherIcon']
                    }
                }
            ]
        return self.data

    def get_context(self):
        return {
            'title'    : self.title,
            'more_info': self.more_info,
            'type'     : self.type,
            'data'     : self.data
        }

class weatherWidgetWeek(Widget):
    title     = "Weekly Weather Forecast"
    more_info = "Weekly weather forecast"
    type      = "weatherWidgetWeek"
    col       = 2
    row       = 1

    def set_data(self, user = None, weatherData = None):
        if weatherData != None:
            self.data = [
                {'label': day_data['day'], 
                 'value': 
                 {
                    'maxTemp': day_data['maxTemp'],
                    'minTemp': day_data['minTemp'],
                    'weatherIcon': day_data['weatherIcon']
                }}
                for day_data in weatherData
            ]
            return self.data
        else:
            self.data = [
                {'label': "Could Not Obtain Weather Data", 
                 'value': 
                 {
                    'maxTemp': "N/A",
                    'minTemp': "N/A",
                    'weatherIcon': "N/A"
                }}
            ]

    def get_context(self):
        return {
            'title'    : self.title,
            'more_info': self.more_info,
            'type'     : self.type,
            'data'     : self.data
        }
    
# Functions
def get_widget_instance(widget_name):
    widget_classes = {
        'My Checkouts': MyCheckouts,
        'My Tasks'    : MyTasks,
        'Weather (Small)': weatherWidgetSmall,
        'Weekly Weather Forecast': weatherWidgetWeek
    }
    widget_class = widget_classes.get(widget_name)

    return widget_class() if widget_class else None


def get_widget_class(widget_type):
    widget_classes = {
        'myCheckouts'  : MyCheckouts,
        'myTasks'      : MyTasks,
        'weatherWidgetSmall': weatherWidgetSmall,
        'weatherWidgetWeek': weatherWidgetWeek
    }

    return widget_classes.get(widget_type)


def get_updated_scope(scope, user, widget_instance):
    weatherManager = WeatherManager()
    locationData = weatherManager.getCurrLocation()
    if widget_instance.type == weatherWidgetSmall.type:
        updatedWeatherData = weatherManager.currentWeatherWidget(locationData['geographicLocation'])
        inputData = widget_instance.set_data(user, weatherData = updatedWeatherData)
    elif widget_instance.type == weatherWidgetWeek.type:
        updatedWeatherData = weatherManager.fiveDayForecastWidget(locationData['geographicLocation'])
        inputData = widget_instance.set_data(user, weatherData = updatedWeatherData)
    else:
        inputData = widget_instance.set_data(user)
    
    scope['data'] = inputData
    return scope
