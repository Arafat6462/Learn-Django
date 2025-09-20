from django.urls import path
from . import views

urlpatterns = [
    path('arafat/', views.say_hello),
]