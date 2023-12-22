from django.urls import path
from .consumers import AssetConsumer

websocket_urlpatterns = [
    path('ws/asset/<int:user_id>/', AssetConsumer.as_asgi()),
]
