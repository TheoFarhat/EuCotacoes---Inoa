import json
import asyncio
import requests
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from core.models import Asset
from channels.db import database_sync_to_async


User = get_user_model()

class AssetConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print("WebSocket connected:", event)

        try:
            user_id = self.scope['url_route']['kwargs']['user_id']
            self.user = await sync_to_async(User.objects.get)(id_user=user_id)
            self.user_group_name = f"user_{self.user.id_user}"

            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )

            await self.accept()
            await self.run_periodic_updates()

        except Exception as e:
            print(f"Error in websocket_connect: {e}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def broadcast_update(self, asset_id):
        asset = await sync_to_async(Asset.objects.get)(id_asset=asset_id)


        await self.send(text_data=json.dumps({
            'type': 'update_asset',
            'id': asset.id_asset,
            'name': asset.name,
            'symbol': asset.symbol,
            'price': asset.price,
            'period': asset.period,
            'percentage_change': asset.percentage_change,
            'lower_tunnel_price': asset.lower_tunnel_price,
            'upper_tunnel_price': asset.upper_tunnel_price
        }))

    @database_sync_to_async
    def update_asset_price(self, asset):
        api_url = f'https://brapi.dev/api/quote/{asset.symbol}?interval={asset.period}&token=8rDXEbmSajqBqWekoG1rTh'
        api_response = requests.get(api_url)
        api_data = api_response.json()
        asset.price = api_data['results'][0]['regularMarketPrice']
        previous_close = api_data['results'][0]['regularMarketPreviousClose']
        asset.percentage_change = round((((asset.price - previous_close) / previous_close) * 100), 2)
        asset.save()

    async def run_periodic_updates(self):
        user_assets = await database_sync_to_async(list)(self.user.assets.all())

        for asset in user_assets:
            asyncio.create_task(self.update_asset_periodically(asset.id_asset))

    async def update_asset_periodically(self, asset_id):
        while True:
            asset = await sync_to_async(Asset.objects.get)(id_asset=asset_id)
            await self.update_asset_price(asset)
            asset.email_tunnel_limits(self.user)
            await self.broadcast_update(asset_id)

            sleep_duration_seconds = int(asset.period[:-1]) * 60
            await asyncio.sleep(sleep_duration_seconds)