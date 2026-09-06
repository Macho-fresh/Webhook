from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
import secrets
from .serializers import *
import requests
from .tasks import *

class RegisterWebhook(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        url = request.data.get('url')
        secret = secrets.token_hex(8)
        user_id = request.user.id
        events = request.data.get('events')

        user = User.objects.get(id=user_id)

        webhook = Webhook.objects.create(
            user = user,
            secret = secret,
            url = url,
            events = events
        )

        serializer = WebhookSerializer(webhook)
        return Response({
            'message': serializer.data
        }, status=status.HTTP_201_CREATED)


class CreateEvent(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id = user_id)

        event = Event.objects.create(
            user = user,
            payload = {
                'amount': 500,
                'product': 'shoe'
            },
            event_type = 'payment.confirmed'
        )

        for wh in Webhook.objects.filter(user=event.user, is_active=True):
            if event.event_type not in wh.events:
                continue
            delivery = Deliveries.objects.create(
                event = event,
                webhook = wh,
                attempts = 0    
            )

            sendrequest.delay(delivery.id)

        return Response({
            'message': 'in queue'
        },status=status.HTTP_201_CREATED)
