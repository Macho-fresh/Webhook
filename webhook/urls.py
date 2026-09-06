from django.urls import path
from .views import *

urlpatterns=[
    path('webhook/', RegisterWebhook.as_view()),
    path('create-event/', CreateEvent.as_view())
]