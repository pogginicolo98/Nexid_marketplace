from django.urls import path
from marketplace.views import IndexTemplateView

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='homepage'),
]
