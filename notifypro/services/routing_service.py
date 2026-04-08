# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Smart Routing Service
Determines the best channel for each notification.
"""
import frappe
from frappe import _


class RoutingService:
    @staticmethod
    def determine_channel(recipient: str, message_type: str = "info", doctype: str | None = None) -> str | None:
        """Pick the best channel based on user preference, availability, cost."""
        # 1. Check user preference
        pref = frappe.db.get_value(
            "NP User Preference",
            {"user": recipient},
            "preferred_channel",
        )
        if pref:
            channel = frappe.db.get_value("NP Channel", {"name": pref, "enabled": 1}, "name")
            if channel:
                return channel

        # 2. Check routing rules
        rules = frappe.get_all(
            "NP Routing Rule",
            filters={"enabled": 1, "message_type": message_type},
            fields=["name", "channel"],
            order_by="priority asc",
            limit=1,
        )
        if rules:
            return rules[0]["channel"]

        # 3. Fallback to default channel
        default = frappe.db.get_value("NP Channel", {"is_default": 1, "enabled": 1}, "name")
        return default

    @staticmethod
    def route_message(message_doc):
        """Route a message to the appropriate channel and enqueue sending."""
        channel = RoutingService.determine_channel(
            recipient=message_doc.recipient,
            message_type=message_doc.message_type,
            doctype=message_doc.reference_doctype,
        )
        if not channel:
            frappe.db.set_value("NP Message", message_doc.name, "status", "Failed")
            frappe.db.set_value("NP Message", message_doc.name, "error_message", "No channel available")
            return
        frappe.db.set_value("NP Message", message_doc.name, "channel", channel)
        frappe.enqueue(
            "notifypro.services.queue_service.send_message",
            queue="short",
            message_name=message_doc.name,
        )
