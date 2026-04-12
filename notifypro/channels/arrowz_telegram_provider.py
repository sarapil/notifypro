# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Arrowz-backed Telegram Provider

Delegates Telegram messaging to Arrowz's TelegramDriver instead of
calling the Bot API directly.
"""
import frappe
from frappe import _
from notifypro.channels.base_provider import BaseChannelProvider


class ArrowzTelegramProvider(BaseChannelProvider):
    """Telegram provider that delegates to Arrowz omni-channel infrastructure."""

    def _get_driver(self):
        """Load the Arrowz Telegram driver for the configured AZ Omni Provider."""
        provider_name = self.channel.get("arrowz_provider")
        if not provider_name:
            frappe.throw(_("NP Channel must specify an Arrowz Provider name"))
        provider_doc = frappe.get_doc("AZ Omni Provider", provider_name)
        from arrowz.integrations.telegram import TelegramDriver

        driver = TelegramDriver(provider_doc)
        channel_name = frappe.db.get_value(
            "AZ Omni Channel",
            {"provider": provider_name, "channel_type": "Telegram", "enabled": 1},
            "name",
        )
        if channel_name:
            channel_doc = frappe.get_doc("AZ Omni Channel", channel_name)
            driver.set_channel(channel_doc)
        return driver

    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        driver = self._get_driver()
        result = driver.send_text_message(recipient, content)
        return {"message_id": str(result.get("message_id", ""))}

    def check_delivery(self, message_id: str) -> dict:
        return {"status": "sent"}

    def validate_recipient(self, identifier: str) -> bool:
        # Telegram chat IDs are numeric (possibly negative for groups)
        cleaned = identifier.lstrip("-")
        return cleaned.isdigit()

    def health_check(self) -> bool:
        driver = self._get_driver()
        result = driver.test_connection()
        return result.get("status") == "success"

    def get_cost(self, message_type: str = "text", destination: str = "") -> float:
        return 0.0
