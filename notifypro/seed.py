# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Seed Data
Runs on `after_migrate` to ensure reference data exists.
"""
import frappe
from frappe import _


def seed_data():
    """Idempotent seed — safe to run multiple times."""
    frappe.logger().info("NotifyPro: Running seed_data()...")
    _seed_settings()
    frappe.db.commit()
    frappe.logger().info("NotifyPro: seed_data() complete.")


def _seed_settings():
    """Ensure Settings singleton has sensible defaults."""
    settings_dt = "NP Settings"
    if not frappe.db.exists("DocType", settings_dt):
        return
    try:
        if not frappe.db.exists(settings_dt, settings_dt):
            settings = frappe.new_doc(settings_dt)
            settings.insert(ignore_permissions=True)
    except Exception as e:
        frappe.logger().warning(f"Could not seed settings: {e}")
