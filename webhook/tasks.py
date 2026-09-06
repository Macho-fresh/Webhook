from celery import shared_task
from .models import *
import requests
import json
import hmac
import hashlib
from celery.exceptions import MaxRetriesExceededError

@shared_task(bind=True, max_retries=5)
def sendrequest(self, delivery_id):
    delivery = Deliveries.objects.get(id=delivery_id)
    events = delivery.event
    wh = delivery.webhook
    
    payload = payload = {
        "event": events.event_type,
        "data": events.payload
    }

    payload_string = json.dumps(
            payload,
            separators=(",", ":"),
            sort_keys=True
        )
    
    signature = hmac.new(
        wh.secret.encode(),
        payload_string.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Signature": signature
    }
    try:
        response = requests.post(url=wh.url, data=payload_string, headers=headers, timeout=10)

        delivery.attempts+=1
        delivery.response_status = response.status_code
        delivery.save()

        if 200 <= response.status_code < 300:
            delivery.status = 'success'
            delivery.save(update_fields=["status"])
        else:
            delivery.status = 'failed'
            delivery.last_error = (f"Webhook returned HTTP {response.status_code}")
            delivery.save(
            update_fields=[
                "status",
                "response_status",
                "last_error"
            ]
            )
            raise Exception(f"Webhook returned {response.status_code}")
    except requests.RequestException as exc:
        delivery.status = "failed"
        delivery.last_error = str(exc)

        delivery.save(
            update_fields=[
                "status",
                "last_error"
            ]
        )

        try:
            raise self.retry(
                exc=exc,
                countdown=60
            )

        except MaxRetriesExceededError:
            delivery.status = "dead"
            delivery.save(update_fields=["status"])

            # add that when one url is unreachable it should not hinder others
