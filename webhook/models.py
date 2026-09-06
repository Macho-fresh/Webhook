from django.db import models
from accounts.models import User

class Webhook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    secret = models.CharField()
    is_active = models.BooleanField(default=True)
    events = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField()
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class Deliveries(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("dead", "Dead"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    webhook = models.ForeignKey(
        Webhook,
        on_delete=models.CASCADE
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    response_status = models.IntegerField(
        null=True,
        blank=True
    )

    last_error = models.TextField(
        blank=True
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attempts = models.PositiveIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )