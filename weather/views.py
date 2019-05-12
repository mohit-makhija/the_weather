import requests
# render to render templates, redirect for redirecting to a url
from django.shortcuts import render, redirect
from .models import City
#Use or city form
from .forms import CityForm
#For displayig messages
from django.contrib import messages

# Create your views here.
def index(request):
    #Weather API from "https://openweathermap.org/current" and appid is got after signing up on the website
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5d9ed462326230269a392c17e455c0ed'
    #Static city input
    #city = 'Mumbai'

    # Case 1 : When user is submitting a city name - we save the city name
    if request.method == 'POST':
        thiscity = requests.get(url.format(request.POST['name'])).json()
        checkcity = City.objects.filter(name__iexact = request.POST['name'])
        # print("This city - {} is already present in database".format(checkcity))
        # print(thiscity)
        
        # Checking if city name entered really exists and also if it already exists in database or not
        if(thiscity['cod'] != '404' and not checkcity.exists()):
            form = CityForm(request.POST)
            form.save()
        elif(thiscity['cod'] == '404'):
            messages.error(request, 'There is no such city named - "{}"'.format(request.POST['name']))
        elif(checkcity.exists):
            messages.success(request, 'You have already added this city')
            # print("City not found darling")
        # print(thiscity)
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