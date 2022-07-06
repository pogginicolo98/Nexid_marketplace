import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from marketplace.tasks import purchase_nft
from redis import Redis
from utils.nfts_redis import get_nfts_from_redis


class PurchaseConsumer(WebsocketConsumer):
    token_id = None
    channel_group = None

    def connect(self):
        self.token_id = self.scope['url_route']['kwargs']['token_id']
        self.channel_group = f'purchase-{self.token_id}'
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        error = self.execute_purchase(token_id=int(self.token_id))
        if error:
            self.send(text_data=json.dumps({'error': error}))
        self.send(text_data=json.dumps({'error': 'null'}))

    def execute_purchase(self, token_id):
        values = get_nfts_from_redis()
        if values is not None:
            for value in values:
                nft = json.loads(value)
                if token_id == nft['token_id']:
                    redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
                    if not redis_client.exists(token_id):
                        purchase_nft.delay(token_id)
                        return None
        return "NFT not available."


class CheckStatusConsumer(WebsocketConsumer):
    token_id = None
    channel_group = None

    def connect(self):
        self.token_id = self.scope['url_route']['kwargs']['token_id']
        self.channel_group = f'status-{self.token_id}'
        async_to_sync(self.channel_layer.group_add)(
            self.channel_group,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_group,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        response = self.check_status(token_id=self.token_id)
        self.send(text_data=json.dumps({'response': response}))

    def check_status(self, token_id):
        """
        Check the status of a purchase.
        """

        redis_client = Redis(settings.REDIS_HOST, port=settings.REDIS_PORT)
        if redis_client.exists(token_id):
            return redis_client.get(token_id)
        else:
            return "NFT not available."
