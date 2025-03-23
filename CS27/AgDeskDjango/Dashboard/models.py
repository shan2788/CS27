"""
Dashboard models.
"""

# Imports
from django.db import models
from FarmAcc.models import FarmInfo

#Weather API Models.

#Loation Model
class Location(models.Model):
    """
    This model defines the attributes of a location object, which enables users to obtain their
    geographical coordinates by using the name of their city, or area.
    """

    geographicLocation = models.CharField(max_length=50, primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    validLocation = models.BooleanField()
    

#Current Weather Model
class ForecastTable(models.Model):
    """
    This model defines the attributes of a current weather object, which enables users to obtain the current
    weather conditions of a location.
    """
    Forecast_ID         = models.AutoField(primary_key=True)
    geographicLocation  = models.ForeignKey(Location, on_delete=models.CASCADE)
    weather             = models.CharField(max_length=50)
    weatherDescription  = models.CharField(max_length=255)
    temperature         = models.FloatField()
    temperatureMin      = models.FloatField()
    temperatureMax      = models.FloatField()
    feelsLike           = models.FloatField()
    humidity            = models.FloatField()
    cloudCoverage       = models.FloatField()
    sunrise             = models.IntegerField(null=True)
    sunset              = models.IntegerField(null=True)
    weatherIcon         = models.CharField()
    forecastOffsetHours = models.IntegerField()

class RetrievalTimes(models.Model):
    """
    This model defines the attributes of a retrieval times object, which enables users to obtain the time
    that the weather data was last retrieved.
    """
    geographicLocation      = models.ForeignKey(Location, on_delete=models.CASCADE)
    currentWeatherRetrieval = models.DateTimeField(null=True)
    forecastRetrieval       = models.DateTimeField(null=True)


# Models for Dashboard Configuration
class Widget(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    scope = models.JSONField(default=dict)
    col = models.IntegerField(default=1)
    row = models.IntegerField(default=1)
    sizex = models.IntegerField(default=1)
    sizey = models.IntegerField(default=1)
    saved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DashboardLayout(models.Model):
    farm = models.OneToOneField(FarmInfo, on_delete=models.CASCADE)
    layout_data = models.JSONField(default=list)
    widgets = models.ManyToManyField(Widget)

    def __str__(self):
        return f"Dashboard for {self.farm}"
