from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.urls import path

urlpatterns=[
    path('login/', TokenObtainPairView.as_view()),
    path('register/', RegisterView.as_view())
]