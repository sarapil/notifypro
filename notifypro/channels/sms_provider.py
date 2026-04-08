# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — SMS Provider (Twilio / MessageBird abstraction)
"""
import frappe
import requests
from notifypro.channels.base_provider import BaseChannelProvider


class SMSProvider(BaseChannelProvider):
    def _get_config(self):
        provider = frappe.get_doc("NP Channel Provider", self.channel.provider)
        return {
            "provider_type": provider.provider_type,
            "account_sid": provider.account_sid,
            "auth_token": provider.get_password("auth_token"),
            "from_number": provider.from_number,
        }

    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        config = self._get_config()
        if config["provider_type"] == "Twilio":
            return self._send_twilio(config, recipient, content)
        frappe.throw(f"Unsupported SMS provider: {config['provider_type']}")

    def _send_twilio(self, config, recipient, content):
        url = f"https://api.twilio.com/2010-04-01/Accounts/{config['account_sid']}/Messages.json"
        response = requests.post(
            url,
            data={"To": recipient, "From": config["from_number"], "Body": content},
            auth=(config["account_sid"], config["auth_token"]),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return {"message_id": data.get("sid", "")}

    def check_delivery(self, message_id: str) -> dict:
        return {"status": "sent"}

    def validate_recipient(self, identifier: str) -> bool:
        return identifier.replace("+", "").replace(" ", "").isdigit()

    def health_check(self) -> bool:
        return True

    def get_cost(self, message_type="text", destination="") -> float:
        return 0.01
