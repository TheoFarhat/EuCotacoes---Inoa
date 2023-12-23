from django.urls import path
from . import views
from . import consumers


urlpatterns = [
    path('', views.create_user, name='create_user'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('assets/', views.assets, name='assets'),
    path('profile/', views.profile, name='profile'),
    path('get-suggestions/', views.get_suggestions, name='get-suggestions'),
    path('create_asset/', views.create_asset, name='create_asset'),
    path('show_users/', views.show_users, name='show_users'),
    path('remove_asset/', views.remove_asset, name='remove_asset'),
    path('ws/asset/<int:user_id>/', consumers.AssetConsumer.as_asgi()),
]

