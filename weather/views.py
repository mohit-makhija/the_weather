import requests
# render to render templates, redirect for redirecting to a url
from django.shortcuts import render, redirect
from .models import City
#Use or city form
from .forms import CityForm

# Create your views here.
def index(request):
    #Weather API from "https://openweathermap.org/current" and appid is got after signing up on the website
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5d9ed462326230269a392c17e455c0ed'
    #Static city input
    #city = 'Mumbai'

    # Case 1 : When user is submitting a city name - we save the city name
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        # pass
        # print(request.POST)

    # Case 2 : When user is not submitting a city name - The form is made blank again
    form = CityForm()

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
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/weather.html', context)

def deleteCity(request,cityname):
    city_to_delete = City.objects.filter(name__iexact=cityname)
    # print(city_to_delete)
    for city in city_to_delete:
        city.delete()
    return redirect('index')
    #return render(request, 'weather/weather.html')