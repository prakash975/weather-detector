from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Location, WeatherData

def home(request):
    if request.method == 'POST':
        city = request.POST['city']
        country = request.POST['country']

        # connect to weather API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=metric&appid=63035d301bd6bd675ef18acdb7341985'
        response = requests.get(url)

        # parse the JSON response
        data = response.json()
        temperature = data['main']['temp']
        condition = data['weather'][0]['description']

        # create or update the location and weather data
        location, created = Location.objects.get_or_create(city=city, country=country)
        weather_data = WeatherData.objects.create(location=location, temperature=temperature, condition=condition)

    # get the last updated weather data for each location
    locations = Location.objects.all()
    weather_data = []
    for location in locations:
        data = WeatherData.objects.filter(location=location).order_by('-updated_at').first()
        weather_data.append(data)

    context = {
        'weather_data': weather_data
    }
    return render(request, 'home.html', context)


