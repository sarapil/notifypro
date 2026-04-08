# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Analytics Service
"""
import frappe


def generate_daily_summary():
    """Daily: aggregate delivery stats."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    if not frappe.db.exists("DocType", "NP Analytics Summary"):
        return
    pass


def generate_weekly_report():
    """Weekly: generate summary report."""
    pass
