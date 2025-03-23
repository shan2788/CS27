import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import aiohttp
from aiohttp import ClientSession, ClientTimeout
import logging
from concurrent.futures import ThreadPoolExecutor
from .models import Location, ForecastTable, RetrievalTimes
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import numpy as np

class WeatherManager:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        
    def convertFromKelvin(self, tempKelvin):
        """
        This function converts temperature from Kelvin to Celsius.
        
        :param tempKelvin: The temperature in Kelvin.
        """
        return round(tempKelvin - 273.15, 0)
        
    def convert_from_unix(self, unix_time):
        """
        Converts Unix time to a human-readable date in the format dd/mm/yyyy.

        :param unix_time: The time in Unix format (seconds since epoch).
        :return: A string representing the date in dd/mm/yyyy format.
        """
        # Convert Unix time to a datetime object in UTC
        dt = datetime.fromtimestamp(unix_time, tz=timezone.utc)
        # Format the datetime object to the desired format
        return dt.strftime('%d/%m/%Y')
    
    def currentWeatherWidget(self, geographicLocation):
        """
        This Function returns a heavily filtered version of the current weather data for the current weather widget.
        
        :param geographicLocation: The location of the farm
        """
        try:
            weatherData = ForecastTable.objects.get(geographicLocation=geographicLocation, forecastOffsetHours=0)
            retrievalTime = RetrievalTimes.objects.get(geographicLocation=geographicLocation).currentWeatherRetrieval
            return {
                'retrievalTime': retrievalTime.time().strftime("%I:%M %p"),
                'geographicLocation': weatherData.geographicLocation_id,
                'currentTemp': self.convertFromKelvin(weatherData.temperature),
                'feelsLike': self.convertFromKelvin(weatherData.feelsLike),
                'humidity': weatherData.humidity,
                'sunrise': datetime.fromtimestamp(weatherData.sunrise).time().strftime("%I:%M %p"),
                'sunset': datetime.fromtimestamp(weatherData.sunset).time().strftime("%I:%M %p"),
                'weather': weatherData.weather,
                'description': (weatherData.weatherDescription).title(),
                "weatherIcon": f"https://openweathermap.org/img/wn/{weatherData.weatherIcon}@2x.png",
            }
        #Enable Graceful Failure of Current Weather Widget when data cannot be obtained.
        except:
            {"error": "Current Weather Data could not be obtained at this time."}
    
    def fiveDayForecastWidget(self, geographicLocation):
        """
        This Function returns a heavily filtered version of the forecasted weather data for the five day forecast widget.
        
        :param geographicLocation: The location of the farm
        """
        try:
            today = datetime.today()
            days = {0: today.strftime("%a"), 1: (today + timedelta(days=1)).strftime("%a"), 2: (today + timedelta(days=2)).strftime("%a"), 3: (today + timedelta(days=3)).strftime("%a"), 4: (today + timedelta(days=4)).strftime("%a")}
            weatherData = []
            for day in range(5):
                minTemp = np.inf
                maxTemp = -(np.inf)
                start_hour = day * 24
                end_hour = (day + 1) * 24
                day_data = ForecastTable.objects.filter(
                geographicLocation=geographicLocation,
                forecastOffsetHours__gt=start_hour,
                forecastOffsetHours__lte=end_hour
                )
                for data in day_data:
                    if data.temperatureMax > maxTemp:
                        maxTemp = data.temperatureMax
                    if data.temperatureMin < minTemp:
                        minTemp = data.temperatureMin
                weatherData.append({'day':days[day], 'maxTemp': self.convertFromKelvin(maxTemp), 'minTemp': self.convertFromKelvin(minTemp), 'weatherIcon': f"https://openweathermap.org/img/wn/{day_data[4].weatherIcon}@2x.png"})
            return weatherData
        # To enabled graceful failure of widgets on Dashboard in the event no 
        except:
            return {"error": "Forecast Weather Data could not be obtained at this time."}

    
    
    #an improvement could be to make the default the capital city of the state the user farm is in.
    def getCurrLocation(self, location=["Bribie", "QLD", "AU"], limit=1):
        """
        This function allows a user to obtain their geogrpahical coordinates by using
        the name of their city, or area.
        
        :param city: A list containing the name of the city, state code, and country code.
        :param limit: The number of results to return.
        """
        URL = f"http://api.openweathermap.org/geo/1.0/direct?q={location[0]},{location[1]},{location[2]}&limit={limit}&appid={self.API_KEY}"
        
        locationCheck = Location.objects.filter(geographicLocation=location[0]).exists()
        
        #If the location exists, return the object from the database. Otherwise, make a request to the API.
        
        if locationCheck:
            locationData = Location.objects.get(geographicLocation = location[0])
            return model_to_dict(locationData)
        
        try:
            response = requests.get(URL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            response = response.json()
            # Construct Filtered JSON Object
            coords = {
                "geographicLocation": location[0],
                "lat": response[0]["lat"],
                "lon": response[0]["lon"],
                "validLocation": True
            }
            Location.objects.create(**coords)
            return coords
        except requests.RequestException as e:
            return {
                    "error": str(e),
                    "status": 500
                    }   
        
    def callWeatherEndpoints(self, location, currentWeather = True):
        """
        This function makes an HTTP request to the weather API to fetch the weather data.

        :param location: A dictionary containing the latitude and longitude of the location.
        :return: The HTTP response from the weather API.
        """
        if currentWeather == True:
            URL = f"http://api.openweathermap.org/data/2.5/weather?lat={location['lat']}&lon={location['lon']}&appid={self.API_KEY}"
        else:
            URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={location['lat']}&lon={location['lon']}&appid={self.API_KEY}"
            
        logging.info(f"Fetching weather data from URL: {URL}")

        try:
            response = requests.get(URL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            weather_data = response.json()
            return weather_data
        except requests.RequestException as e:
            return {
                    "error": str(e),
                    "status": 500
                    }       
            
                    
    def processCurrWeatherEndpoint(self, farmLocation, location = {"lat": -27.4698, "lon": 153.0251}):
        """
        This function allows a user to obtain the current weather conditions of a location.
        
        :param location: A dictionary containing the latitude and longitude of the location.
        """
        response = self.callWeatherEndpoints(location)
        if response:
            getFarmLocation = Location.objects.get(geographicLocation=farmLocation)
            # Construct Filtererd JSON Object
            currentWeather = {
                "geographicLocation": getFarmLocation,
                "weather": response["weather"][0]["main"],
                "weatherDescription": response["weather"][0]["description"],
                "temperature": response["main"]["temp"],
                "temperatureMin": response["main"]["temp_min"],
                "temperatureMax": response["main"]["temp_max"],
                "feelsLike": response["main"]["feels_like"],
                "humidity": response["main"]["humidity"],
                "cloudCoverage": response["clouds"]["all"],
                "sunrise": response["sys"]["sunrise"],
                "sunset": response["sys"]["sunset"],
                "weatherIcon": response["weather"][0]["icon"],
                "forecastOffsetHours": 0
            }
            retrievalData = {
                "geographicLocation": getFarmLocation,
                "currentWeatherRetrieval": timezone.make_aware(datetime.now()),
            }
            if not RetrievalTimes.objects.filter(geographicLocation=farmLocation).exists():
                RetrievalTimes.objects.create(**retrievalData)
            else:
                RetrievalTimes.objects.filter(geographicLocation=farmLocation).update(**retrievalData)
            # Save the weather data to the database
            return currentWeather, retrievalData
        else:
            raise Exception (response.status)

                    
    
    def getCurrentWeather(self, farmLocation):
        """
        This function allows a user to obtain the current weather conditions of a location.
        
        :param farmLocation: The location of the farm.
        :param user: The user requesting the weather data.
        :param location: A dictionary containing the latitude and longitude of the location.

        :return: The current weather data as a JSON object.
        """
        # Get the current farm location to query to database for it's weather data.
        # NOTE: The Farm Location MUST match the Weather location. Eg if the farm location is brisbanae,
        # that is the location that will be used for the weather API.
        weatherRetrieved = ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours=0).exists()
        
        if weatherRetrieved:
            retrievalTime = RetrievalTimes.objects.get(geographicLocation=farmLocation["geographicLocation"]).currentWeatherRetrieval
            dataUpToDate = (timezone.make_aware(datetime.now()) - retrievalTime < timedelta(hours=1))
            print("Weather data Found...")
            if retrievalTime != None and dataUpToDate:
                print("Weather data is up to date")
                weatherData = ForecastTable.objects.get(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours=0)
                return model_to_dict(weatherData)
            else:
                print("Weather data is outdated")
        else:
            print("Weather data not found")
            
        geoLocation = self.getCurrLocation([farmLocation["geographicLocation"], "QLD", "AU"])
        weatherData = self.processCurrWeatherEndpoint(farmLocation["geographicLocation"], {"lat": geoLocation["lat"], "lon": geoLocation["lon"]})
        
        if not ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours=0).exists():
            ForecastTable.objects.create(**weatherData[0])
        else:
            ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours=0).update(**weatherData[0])
            
        return weatherData[0]
    
    def processForecastEndpoint(self, farmLocation, location = {"lat": -27.4698, "lon": 153.0251}):
        """
        This function allows a user to obtain the forecasted weather over the next 5 days at 3 hour intervals.
        
        :param farmLocation: The location of the farm.
        :param location: A dictionary containing the latitude and longitude of the location.
        
        """
        foreCastData = []
        response = self.callWeatherEndpoints(location, False)
        print(response)
        if response:
            getFarmLocation = Location.objects.get(geographicLocation=farmLocation)
            # Construct Filtererd JSON Object
            for forecastOffset, data in enumerate(response["list"]):
                foreCastData.append({
                    "geographicLocation": getFarmLocation,
                    "weather": data["weather"][0]["main"],
                    "weatherDescription": data["weather"][0]["description"],
                    "temperature": data["main"]["temp"],
                    "temperatureMin": data["main"]["temp_min"],
                    "temperatureMax": data["main"]["temp_max"],
                    "feelsLike": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "cloudCoverage": data["clouds"]["all"],
                    "weatherIcon": data["weather"][0]["icon"],
                    "forecastOffsetHours": 3+forecastOffset*3
                })
            retrievalData = {
                "geographicLocation": getFarmLocation,  # Use the id of the Location object
                "forecastRetrieval": timezone.make_aware(datetime.now())
            }
            
            if not RetrievalTimes.objects.filter(geographicLocation=getFarmLocation).exists():
                RetrievalTimes.objects.create(**retrievalData)
            else:
                RetrievalTimes.objects.filter(geographicLocation=getFarmLocation).update(**retrievalData)
            
            return foreCastData
            
                
    def getForecastWeather(self, farmLocation):
        """
        This function allows a user to obtain the forecasted weather over the next 5 days at 3 hour intervals.
        
        :param farmLocation: The location of the farm.
        :param user: The user requesting the weather data.
        :param location: A dictionary containing the latitude and longitude of the location.

        :return: The forecasted weather data as a JSON object.
        """
        # Get the current farm location to query to database for it's weather data.
        # NOTE: The Farm Location MUST match the Weather location. Eg if the farm location is brisbanae,
        # that is the location that will be used for the weather API.
        try:
            weatherRetrieved = ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours__gte=3).exists()
            if weatherRetrieved:
                forecastTimestamp = RetrievalTimes.objects.get(geographicLocation=farmLocation["geographicLocation"]).forecastRetrieval
                dataUpToDate = (timezone.make_aware(datetime.now()) - forecastTimestamp < timedelta(hours=6))
                if forecastTimestamp != None and dataUpToDate: 
                    weatherData = ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours__gte=3)
                    return weatherData
                    
                else:
                    print("Weather data is outdated")
            else:
                print("Weather data not found")
            geoLocation = self.getCurrLocation([farmLocation["geographicLocation"], "QLD", "AU"])
            weatherData = self.processForecastEndpoint(farmLocation["geographicLocation"], {"lat": geoLocation["lat"], "lon": geoLocation["lon"]})
            if not ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours__gte=3).exists():
                for data in weatherData:
                    print(data)
                    ForecastTable.objects.create(**data)
            else:
                for data in ForecastTable.objects.filter(geographicLocation=farmLocation["geographicLocation"], forecastOffsetHours__gte=3):
                    setattr(data, **weatherData["geographicLocation"])
            return weatherData
        except Exception as e:
            print(e)
    
    
    def main(self, location = ["Bribie", "QLD", "AU"]):
        """
        This function provides a single entry and exit point for the WeatherManager class.
        The purpose of this function is to avoid event loop based errors that can stem from needing to run multiple event loops.
        
        :param location: A list containing the name of the city, state code, and country code.

        Location is hardcoded as Bribie at the moment. When the Google API address picker is implemented, update the location to the farm location.
        """
        location = self.getCurrLocation(location)
        if "error" in location:
            return {"error": "AgDesk encountered an error and couldn't obtain weather data, please try again later."}
        
        else:
            currWeather = self.getCurrentWeather(location)
            
            finalFore = self.getForecastWeather(location)

        return currWeather, finalFore
                
            
        
        

            
        
        

    

        


        

                    
    
        