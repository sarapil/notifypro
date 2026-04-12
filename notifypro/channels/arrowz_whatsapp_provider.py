# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Arrowz-backed WhatsApp Provider

Delegates WhatsApp messaging to Arrowz's WhatsAppCloudDriver instead of
calling the Meta API directly.  This avoids duplicate credentials and
lets Arrowz handle message logging, conversation sessions, and CDR.
"""
import frappe
from frappe import _
from notifypro.channels.base_provider import BaseChannelProvider


class ArrowzWhatsAppProvider(BaseChannelProvider):
    """WhatsApp provider that delegates to Arrowz omni-channel infrastructure."""

    def _get_driver(self):
        """Load the Arrowz WhatsApp driver for the configured AZ Omni Provider."""
        provider_name = self.channel.get("arrowz_provider")
        if not provider_name:
            frappe.throw(_("NP Channel must specify an Arrowz Provider name"))
        provider_doc = frappe.get_doc("AZ Omni Provider", provider_name)
        from arrowz.integrations.whatsapp import WhatsAppCloudDriver

        driver = WhatsAppCloudDriver(provider_doc)
        # Load the first active WhatsApp channel for the provider
        channel_name = frappe.db.get_value(
            "AZ Omni Channel",
            {"provider": provider_name, "channel_type": "WhatsApp", "enabled": 1},
            "name",
        )
        if channel_name:
            channel_doc = frappe.get_doc("AZ Omni Channel", channel_name)
            driver.set_channel(channel_doc)
        return driver

    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        driver = self._get_driver()
        result = driver.send_text_message(recipient, content)
        return {"message_id": result.get("message_id", "")}

    def check_delivery(self, message_id: str) -> dict:
        return {"status": "sent"}

    def validate_recipient(self, identifier: str) -> bool:
        return identifier.replace("+", "").replace(" ", "").isdigit()

    def health_check(self) -> bool:
        driver = self._get_driver()
        result = driver.test_connection()
        return result.get("status") == "success"

    def get_cost(self, message_type: str = "text", destination: str = "") -> float:
        return 0.005
