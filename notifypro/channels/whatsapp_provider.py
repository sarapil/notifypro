# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — WhatsApp Cloud API Provider
"""
import frappe
import requests
from notifypro.channels.base_provider import BaseChannelProvider


class WhatsAppProvider(BaseChannelProvider):
    def _get_config(self):
        provider = frappe.get_doc("NP Channel Provider", self.channel.provider)
        return {
            "api_url": provider.api_url or "https://graph.facebook.com/v18.0",
            "phone_number_id": provider.phone_number_id,
            "access_token": provider.get_password("access_token"),
        }

    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        config = self._get_config()
        url = f"{config['api_url']}/{config['phone_number_id']}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "text",
            "text": {"body": content},
        }
        response = requests.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {config['access_token']}"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return {"message_id": data.get("messages", [{}])[0].get("id", "")}

    def check_delivery(self, message_id: str) -> dict:
        return {"status": "sent"}

    def validate_recipient(self, identifier: str) -> bool:
        return identifier.replace("+", "").replace(" ", "").isdigit()

    def health_check(self) -> bool:
        config = self._get_config()
        resp = requests.get(
            f"{config['api_url']}/{config['phone_number_id']}",
            headers={"Authorization": f"Bearer {config['access_token']}"},
            timeout=10,
        )
        return resp.status_code == 200

    def get_cost(self, message_type="text", destination="") -> float:
        return 0.005
