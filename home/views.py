from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=c6df3c8d9cbe6ae4c3fe98b05237b3c0';
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist!'
            else:
                err_msg = 'City already exists!'
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added Successfully!'
            message_class = 'is-primary'
    
    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city.name,
            'temperature' : int(r['main']['temp'] -273),
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
        }
    return render(request,'index.html', context)
def delete_city(requests, city_name):
      City.objects.filter(name=city_name).delete()
      return redirect('/')