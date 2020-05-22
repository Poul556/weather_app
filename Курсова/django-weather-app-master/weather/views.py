import requests
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import CityForm
from .models import city
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
import datetime


def add_city(request, url):
    err_msg = ''
    message = ''
    message_class = ''
    new_city = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = city.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                err_msg = "City already exist in the database!"
        if err_msg :
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"
    return message, message_class, new_city

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1be6324f259e2d5ad5e3f216c7627890'

    message, message_class, new_city = add_city(request, url=url)

    form = CityForm()
    cities = city.objects.all()

    weather_data = []

    for city_ in cities:

        r = requests.get(url.format(city_)).json()
        print(r)
        city_weather  = {
            'city' : city_.name,
            'temperature' : r['main']['temp'],
            'wind_speed': r['wind']['speed'],
            'humidity': r['main']['humidity'],
            'feels_like': r['main']['feels_like'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather/weather.html',context)

def week_weather(request):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=7&appid=522d2982bc7b44a4f919e6ac7dc5b1f5'
    err_msg = ''
    city_name = None
    message = ''
    message_class = ''
    show_info = None

   # message, message_class, new_city = add_city(request, url=url)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_name = new_city
            existing_city_count = city.objects.filter(name=new_city)
            if not existing_city_count:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == '200':
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                r = requests.get(url.format(url.format(new_city)))
                err_msg = "City already exist in the database!"
                show_info = True
        if err_msg:
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            show_info = True
            message_class = "alert-success"


    r = requests.get(url.format(city_name))



    form = CityForm()

    j = r.json()
    print(j)
    n = 0
    weather_data = []
    while n < 7:
        udate = j["list"][n]["dt"]
        date = datetime.datetime.fromtimestamp(int(udate)).strftime('%Y-%m-%d')
        temp_min = int(j["list"][n]["temp"]["min"] - 274)
        temp_max = int(j["list"][n]["temp"]["max"] - 274)
        weather = j["list"][n]["weather"][0]["description"]
        feels_like_day = int(j["list"][n]['feels_like']['day'] - 274)
        feels_like_night = int(j["list"][n]['feels_like']['night'] - 274)
        humidity = j["list"][n]['humidity']
        wind_speed = j["list"][n]['speed']
        icon = j["list"][n]['weather'][0]['icon']
        city_weather = {
            'date': date,
            'temperature_min': str(temp_min),
            'temperature_max': str(temp_max),
            'description':weather,
            'feels_like_day': feels_like_day,
            'feels_like_night': feels_like_night,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'icon': icon,
        }
        n = n + 1
        weather_data.append(city_weather)

    context = {
        'show_info': show_info,
        'city': city_name,
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_class': message_class
    }
    return render(request, 'weather/week_weather.html', context)

def tomorrow_weather(request):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=7&appid=522d2982bc7b44a4f919e6ac7dc5b1f5'
    err_msg = ''
    city_name = None
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_name = new_city
            existing_city_count = city.objects.filter(name=new_city)
            if not existing_city_count:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == '200':
                    form.save()
                else:
                    err_msg = "City doesnt exist"
            else:
                r = requests.get(url.format(url.format(new_city)))
                err_msg = "City already exist in the database!"
        if err_msg:
            message = err_msg
            message_class = 'alert-danger'
        else:
            message = 'City added successfully!'
            message_class = "alert-success"

    form = CityForm()
    cities = city.objects.all()

    weather_data = []

    for city_ in cities:
        r = requests.get(url.format(city_.name))
        j = r.json()
        temp_min = int(j["list"][1]["temp"]["min"] - 274)
        temp_max = int(j["list"][1]["temp"]["max"] - 274)
        weather = j["list"][1]["weather"][0]["description"]
        feels_like_day = int(j["list"][1]['feels_like']['day'] - 274)
        feels_like_night = int(j["list"][1]['feels_like']['night'] - 274)
        humidity = j["list"][1]['humidity']
        wind_speed = j["list"][1]['speed']
        icon = j["list"][1]['weather'][0]['icon']
        city_weather = {
            'city': city_.name,
            'temperature_min': str(temp_min),
            'temperature_max': str(temp_max),
            'description': weather,
            'feels_like_day': feels_like_day,
            'feels_like_night': feels_like_night,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'icon': icon,
        }
        print(city_weather)
        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data,
        'form':form,
        'message':message,
        'message_class':message_class
    }

    return render(request, 'weather/tomorrow_weather.html',context)


def about(request) :
    return render(request,'weather/about.html')

    
def delete_city(request, city_name):
    city.objects.get(name=city_name).delete()
    return redirect('home')

def help(request):
    return render(request,'weather/help.html')
