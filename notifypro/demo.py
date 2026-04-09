# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""
NotifyPro — Demo Data
Load / clear demo data for showcasing app features.
"""
import frappe
from frappe import _


def load_demo_data():
    """Load realistic demo records for NotifyPro."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return

    # Demo channels
    channels = [
        {"channel_name": "Demo Email Channel", "channel_type": "Email", "enabled": 1},
        {"channel_name": "Demo SMS Channel", "channel_type": "SMS", "enabled": 1},
        {"channel_name": "Demo WhatsApp Channel", "channel_type": "WhatsApp", "enabled": 0},
    ]
    for ch in channels:
        if not frappe.db.exists("NP Channel", {"channel_name": ch["channel_name"]}):
            doc = frappe.get_doc({"doctype": "NP Channel", **ch})
            doc.insert(ignore_permissions=True)

    # Demo templates
    templates = [
        {
            "template_name": "Welcome Email",
            "channel": "Email",
            "subject": "Welcome to {company}!",
            "body": "Dear {name},\n\nThank you for joining {company}.",
            "language": "en",
        },
        {
            "template_name": "رسالة ترحيب",
            "channel": "Email",
            "subject": "أهلاً بك في {company}!",
            "body": "عزيزي {name}،\n\nشكراً لانضمامك إلى {company}.",
            "language": "ar",
        },
        {
            "template_name": "Order Confirmation SMS",
            "channel": "SMS",
            "subject": "",
            "body": "Your order #{order_id} has been confirmed. Thank you!",
            "language": "en",
        },
    ]
    for tmpl in templates:
        if not frappe.db.exists("NP Template", {"template_name": tmpl["template_name"]}):
            doc = frappe.get_doc({"doctype": "NP Template", **tmpl})
            doc.insert(ignore_permissions=True)

    # Demo notification logs
    statuses = ["Sent", "Delivered", "Failed", "Delivered", "Delivered", "Sent"]
    for i, status in enumerate(statuses):
        if not frappe.db.exists("NP Notification Log", {"subject": f"Demo notification {i+1}"}):
            doc = frappe.get_doc({
                "doctype": "NP Notification Log",
                "subject": f"Demo notification {i+1}",
                "channel": "Email",
                "recipient": f"demo{i+1}@example.com",
                "status": status,
            })
            doc.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.msgprint(_("NotifyPro demo data loaded successfully."))


def clear_demo_data():
    """Remove all demo data."""
    for dt in ["NP Notification Log", "NP Template", "NP Channel"]:
        for name in frappe.get_all(dt, filters={"owner": "Administrator"}, pluck="name", limit=50):
            try:
                frappe.delete_doc(dt, name, force=True)
            except Exception:
                pass
    frappe.db.commit()
    frappe.msgprint(_("NotifyPro demo data cleared."))
