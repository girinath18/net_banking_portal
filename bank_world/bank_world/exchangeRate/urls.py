from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('eur/', views.ExchangeRateView.as_view(), name='get_eur'),  # For DB-based rates
    path('eurraw/', views.ExchangeRateRawView.as_view(), name='get_eur_raw'),  # For API raw rates
]
