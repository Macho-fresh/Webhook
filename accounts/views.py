from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        return Response({
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)