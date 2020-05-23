from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="home"),
    path('week-weather', views.week_weather, name='week'),
    path('tomorrow-weather', views.tomorrow_weather, name='tommorrow'),
    path('about/',views.about,name="about"),
    path('help/',views.help,name="help"),
    path('delete/<city_name>/',views.delete_city,name="delete_city"),


]