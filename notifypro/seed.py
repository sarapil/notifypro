# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""
NotifyPro — Seed Data
Runs on `after_migrate` to ensure reference data exists.
"""
import frappe
from frappe import _


def seed_data():
    """Idempotent seed — safe to run multiple times."""
    _seed_settings()
    _seed_channels()
    _seed_categories()
    frappe.db.commit()


def _seed_settings():
    settings_dt = "NP Settings"
    if not frappe.db.exists("DocType", settings_dt):
        return
    try:
        if not frappe.db.exists(settings_dt, settings_dt):
            frappe.new_doc(settings_dt).insert(ignore_permissions=True)
    except Exception:
        pass


def _seed_channels():
    if not frappe.db.exists("DocType", "NP Channel"):
        return
    channels = [
        {"channel_name": "Email", "channel_type": "Email", "enabled": 1, "priority": 1,
         "rate_limit_per_minute": 30, "rate_limit_per_hour": 500, "daily_limit": 5000},
        {"channel_name": "SMS", "channel_type": "SMS", "enabled": 0, "priority": 2,
         "rate_limit_per_minute": 10, "rate_limit_per_hour": 100, "daily_limit": 1000},
        {"channel_name": "WhatsApp", "channel_type": "WhatsApp", "enabled": 0, "priority": 3,
         "rate_limit_per_minute": 20, "rate_limit_per_hour": 200, "daily_limit": 2000},
        {"channel_name": "Telegram", "channel_type": "Telegram", "enabled": 0, "priority": 4,
         "rate_limit_per_minute": 30, "rate_limit_per_hour": 500, "daily_limit": 5000},
        {"channel_name": "Push Notification", "channel_type": "Push", "enabled": 0, "priority": 5,
         "rate_limit_per_minute": 60, "rate_limit_per_hour": 1000, "daily_limit": 10000},
        {"channel_name": "In-App", "channel_type": "In-App", "enabled": 1, "priority": 0,
         "rate_limit_per_minute": 100, "rate_limit_per_hour": 5000, "daily_limit": 50000},
    ]
    for ch in channels:
        if not frappe.db.exists("NP Channel", {"channel_name": ch["channel_name"]}):
            doc = frappe.new_doc("NP Channel")
            doc.update(ch)
            doc.insert(ignore_permissions=True)


def _seed_categories():
    if not frappe.db.exists("DocType", "NP Notification Category"):
        return
    categories = [
        {"category_name": "System", "description": _("System notifications"), "default_channel": "In-App", "allow_opt_out": 0, "icon": "settings"},
        {"category_name": "Alerts", "description": _("Important alerts"), "default_channel": "Email", "allow_opt_out": 0, "icon": "alert-circle"},
        {"category_name": "Marketing", "description": _("Marketing campaigns"), "default_channel": "Email", "allow_opt_out": 1, "icon": "megaphone"},
        {"category_name": "Transactional", "description": _("Order/payment updates"), "default_channel": "Email", "allow_opt_out": 0, "icon": "credit-card"},
        {"category_name": "Social", "description": _("Mentions, comments"), "default_channel": "In-App", "allow_opt_out": 1, "icon": "message-circle"},
        {"category_name": "Reminders", "description": _("Scheduled reminders"), "default_channel": "Email", "allow_opt_out": 1, "icon": "clock"},
    ]
    for cat in categories:
        if not frappe.db.exists("NP Notification Category", {"category_name": cat["category_name"]}):
            doc = frappe.new_doc("NP Notification Category")
            doc.update(cat)
            doc.insert(ignore_permissions=True)
