from django.contrib import admin
from django.urls import path

import mainapp
from mainapp.views import *

app_name = 'mainapp'

urlpatterns = [
    path('', main, name='main'),
    path('mainapp/learning', learning, name='learning'),
    path('ajax', ajax, name='ajax'),
    path('mainapp/game', game, name='game'),
    path('mainapp/wordlist', wordlist, name='wordlist'),
    path('mainapp/delete/<int:id>', mainapp.views.delete, name='delete'),
    path('detectme', detectme, name="detectme"),
    path('detectme2', detectme2, name="detectme2"),
]