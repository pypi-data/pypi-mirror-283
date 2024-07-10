import logging

from django.conf import settings

from django.apps import apps
from django.urls import reverse
from requests import request

logger = logging.getLogger(__name__)


def update_shop_webhooks(shop):
    deactivate_webhooks(shop)
    activate_webhooks(shop)


def activate_webhooks(shop):
    config = apps.get_app_config("shopify_app")
    webhooks_path = reverse("shopify_app:webhooks")
    webhooks_address = f"{config.WEBHOOK_HOST}{webhooks_path}"
    for topic in settings.SHOPIFY_WEBHOOK_TOPICS:
        data = {
            "webhook": {
                "topic": topic,
                "address": webhooks_address,
                "format": "json",
            }
        }
        response = shop.post("/admin/api/api_version/webhooks.json", data)
        response.raise_for_status()


def deactivate_webhooks(shop):
    response = shop.get("/admin/api/api_version/webhooks.json")
    response.raise_for_status()
    webhooks = response.json()["webhooks"]
    for webhook in webhooks:
        shop.delete_request(f"/admin/api/api_version/webhooks/{webhook['id']}.json")
