from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Replace 'home' with your actual view
]
