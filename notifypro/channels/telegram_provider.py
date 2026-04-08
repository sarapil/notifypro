# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Telegram Bot API Provider
"""
import frappe
import requests
from notifypro.channels.base_provider import BaseChannelProvider


class TelegramProvider(BaseChannelProvider):
    def _get_config(self):
        provider = frappe.get_doc("NP Channel Provider", self.channel.provider)
        return {"bot_token": provider.get_password("bot_token")}

    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        config = self._get_config()
        url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
        response = requests.post(url, json={"chat_id": recipient, "text": content}, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {"message_id": str(data.get("result", {}).get("message_id", ""))}

    def check_delivery(self, message_id: str) -> dict:
        return {"status": "delivered"}

    def validate_recipient(self, identifier: str) -> bool:
        return bool(identifier)

    def health_check(self) -> bool:
        config = self._get_config()
        resp = requests.get(f"https://api.telegram.org/bot{config['bot_token']}/getMe", timeout=10)
        return resp.status_code == 200

    def get_cost(self, message_type="text", destination="") -> float:
        return 0.0
