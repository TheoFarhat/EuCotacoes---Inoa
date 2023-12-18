from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('assets/', views.assets, name='assets'),
    path('get-suggestions/', views.get_suggestions, name='get-suggestions'),
    path('user/<int:user_id>/assets/', views.user_assets_list, name='user_assets'),
    path('signup/', views.create_user, name='create_user'),
    path('create_asset/', views.create_asset, name='create_asset'),
    path('show_users/', views.show_users, name='show_users'),
]

