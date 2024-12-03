from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^random/$', views.getRandomData, name='random'),  # Use the standalone function
]
