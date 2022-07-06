from django.urls import re_path
from marketplace.consumers import CheckStatusConsumer, PurchaseConsumer

websocket_urlpatterns = [
    re_path(r'ws/marketplace/(?P<token_id>[-\w]+)/purchase/$', PurchaseConsumer.as_asgi()),
    re_path(r'ws/marketplace/(?P<token_id>[-\w]+)/status/$', CheckStatusConsumer.as_asgi()),
]
