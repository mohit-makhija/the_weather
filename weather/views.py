import requests
# To render templates
from django.shortcuts import render
from .models import City

# Create your views here.
def index(request):
    #Weather API from "https://openweathermap.org/current" and appid is got after signing up on the website
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5d9ed462326230269a392c17e455c0ed'
    #Static city input
    city = 'Mumbai'

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        # city name is pased to API request
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    # Data to be passed to template
    context = {'weather_data' : weather_data}

    return render(request, 'weather/weather.html', context)