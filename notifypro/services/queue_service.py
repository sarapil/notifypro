# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Queue & Delivery Service
Handles message queue processing and retries.
"""
import frappe
from frappe import _


def process_queue():
    """Scheduled: process pending messages in queue."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    if not frappe.db.exists("DocType", "NP Queue"):
        return
    pending = frappe.get_all(
        "NP Queue",
        filters={"status": "Pending"},
        fields=["name", "message"],
        order_by="creation asc",
        limit=100,
    )
    for item in pending:
        try:
            send_message(item.message)
            frappe.db.set_value("NP Queue", item.name, "status", "Sent")
        except Exception as e:
            frappe.db.set_value("NP Queue", item.name, "status", "Failed")
            frappe.db.set_value("NP Queue", item.name, "error_message", str(e)[:500])
            frappe.log_error(title=f"NP Queue processing error: {item.name}")
    frappe.db.commit()


def send_message(message_name: str):
    """Send a single message via its assigned channel."""
    msg = frappe.get_doc("NP Message", message_name)
    if msg.status in ("Sent", "Delivered"):
        return
    from notifypro.services.channel_service import ChannelService
    provider = ChannelService.get_channel_provider(msg.channel)
    result = provider.send(
        recipient=msg.recipient,
        content=msg.content,
        template=msg.template,
    )
    msg.db_set("status", "Sent")
    msg.db_set("external_id", result.get("message_id", ""))
    frappe.db.commit()


def retry_failed_messages():
    """Scheduled: retry failed messages up to max retries."""
    if not frappe.db.exists("DocType", "NP Message"):
        return
    failed = frappe.get_all(
        "NP Message",
        filters={"status": "Failed", "retry_count": ["<", 3]},
        fields=["name"],
        limit=50,
    )
    for msg in failed:
        frappe.db.set_value("NP Message", msg.name, "retry_count", frappe.db.get_value("NP Message", msg.name, "retry_count") + 1)
        frappe.enqueue(
            "notifypro.services.queue_service.send_message",
            queue="short",
            message_name=msg.name,
        )
    frappe.db.commit()
