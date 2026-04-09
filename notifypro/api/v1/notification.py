# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from notifypro.api.response import success, error, paginated


@frappe.whitelist()
def send(recipients, channel, subject=None, message=None, template=None, template_context=None, priority="Medium"):
    """Send a notification through a specified channel."""
    frappe.has_permission("NP Message", "create", throw=True)
    from notifypro.services.channel_service import ChannelService
    try:
        if isinstance(recipients, str):
            recipients = [r.strip() for r in recipients.split(",")]
        if isinstance(template_context, str):
            template_context = frappe.parse_json(template_context)

        result = ChannelService.send_notification(
            recipients=recipients,
            channel=channel,
            subject=subject,
            message=message,
            template=template,
            template_context=template_context or {},
            priority=priority,
        )
        return success(data=result, message="Notification queued successfully")
    except Exception as e:
        frappe.log_error("NotifyPro Send Error")
        return error(str(e), error_code="NP_SEND_FAILED")


@frappe.whitelist()
def send_bulk(recipients, channel, template, template_context=None, campaign=None):
    """Send bulk notifications."""
    frappe.has_permission("NP Campaign", "create", throw=True)
    from notifypro.services.queue_service import QueueService
    try:
        if isinstance(recipients, str):
            recipients = frappe.parse_json(recipients)
        if isinstance(template_context, str):
            template_context = frappe.parse_json(template_context)

        result = QueueService.enqueue_bulk(
            recipients=recipients,
            channel=channel,
            template=template,
            template_context=template_context or {},
            campaign=campaign,
        )
        return success(data=result, message="Bulk send queued")
    except Exception as e:
        frappe.log_error("NotifyPro Bulk Send Error")
        return error(str(e), error_code="NP_BULK_FAILED")


@frappe.whitelist()
def get_status(message_name):
    """Get delivery status of a notification."""
    frappe.has_permission("NP Message", "read", throw=True)
    msg = frappe.get_doc("NP Message", message_name)
    return success(data={
        "name": msg.name,
        "status": msg.status,
        "channel": msg.channel,
        "recipient": msg.recipient,
        "sent_at": str(msg.sent_at) if msg.sent_at else None,
        "delivered_at": str(msg.delivered_at) if msg.delivered_at else None,
        "error_message": msg.error_message,
    })


@frappe.whitelist()
def get_queue_stats():
    """Get notification queue statistics."""
    frappe.has_permission("NP Queue", "read", throw=True)
    stats = {
        "pending": frappe.db.count("NP Queue", {"status": "Pending"}),
        "processing": frappe.db.count("NP Queue", {"status": "Processing"}),
        "sent": frappe.db.count("NP Queue", {"status": "Sent"}),
        "failed": frappe.db.count("NP Queue", {"status": "Failed"}),
    }
    return success(data=stats)
