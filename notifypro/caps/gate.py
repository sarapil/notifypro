# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
notifypro — CAPS Gate
"""
import frappe


def check_user_capability(capability_name, throw=True):
    """Check if current user has the named capability."""
    if "caps" not in frappe.get_installed_apps():
        return True
    from caps.services.capability_service import check_capability
    return check_capability(capability_name, frappe.session.user, throw=throw)
