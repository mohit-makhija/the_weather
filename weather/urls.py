from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # [\w\s]* means space seperated words for city name
    re_path(r'^deleteCity/(?P<cityname>[\w\s]*)/$', views.deleteCity, name='deleteCity'),
    # path('deleteCity/<city>/', views.deleteCity),
]