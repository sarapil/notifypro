# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Channel Service
Manages notification channels and provider health.
"""
import frappe
from frappe import _


def check_channel_health():
    """Module-level wrapper for scheduler."""
    ChannelService.check_channel_health()


class ChannelService:
    @staticmethod
    def get_active_channels() -> list[dict]:
        """Return all active channels."""
        return frappe.get_all(
            "NP Channel",
            filters={"enabled": 1},
            fields=["name", "channel_type", "provider", "is_default", "priority"],
            order_by="priority asc",
        )

    @staticmethod
    def get_channel_provider(channel_name: str):
        """Load the channel provider adapter for a given channel.

        If the NP Channel has an ``arrowz_provider`` field set and Arrowz is
        installed, the Arrowz-backed provider is used for WhatsApp / Telegram
        so that credentials and message logging are centralised in Arrowz.
        """
        channel = frappe.get_cached_doc("NP Channel", channel_name)

        # Arrowz-backed providers — preferred when available
        arrowz_installed = "arrowz" in frappe.get_installed_apps()
        use_arrowz = arrowz_installed and channel.get("arrowz_provider")

        provider_map = {
            "WhatsApp": (
                "notifypro.channels.arrowz_whatsapp_provider.ArrowzWhatsAppProvider"
                if use_arrowz
                else "notifypro.channels.whatsapp_provider.WhatsAppProvider"
            ),
            "Telegram": (
                "notifypro.channels.arrowz_telegram_provider.ArrowzTelegramProvider"
                if use_arrowz
                else "notifypro.channels.telegram_provider.TelegramProvider"
            ),
            "SMS": "notifypro.channels.sms_provider.SMSProvider",
            "Email": "notifypro.channels.email_provider.EmailProvider",
            "Push": "notifypro.channels.push_provider.PushProvider",
        }
        provider_path = provider_map.get(channel.channel_type)
        if not provider_path:
            frappe.throw(_("Unsupported channel type: {0}").format(channel.channel_type))
        module_path, class_name = provider_path.rsplit(".", 1)
        module = frappe.get_module(module_path)
        return getattr(module, class_name)(channel)

    @staticmethod
    def check_channel_health():
        """Background task: check all channel providers are reachable."""
        channels = ChannelService.get_active_channels()
        for ch in channels:
            try:
                provider = ChannelService.get_channel_provider(ch["name"])
                provider.health_check()
                frappe.db.set_value("NP Channel", ch["name"], "health_status", "Healthy")
            except Exception as e:
                frappe.db.set_value("NP Channel", ch["name"], "health_status", "Unhealthy")
                frappe.log_error(title=f"Channel health check failed: {ch['name']}", message=str(e))
        frappe.db.commit()
