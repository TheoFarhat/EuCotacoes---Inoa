from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('assets/', views.assets, name='assets'),
    path('get-suggestions/', views.get_suggestions, name='get-suggestions'),
]

