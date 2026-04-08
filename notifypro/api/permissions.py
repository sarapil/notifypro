# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Permission Checks
"""
import frappe


def has_app_permission():
    """Check if current user can access NotifyPro."""
    if frappe.session.user == "Administrator":
        return True
    user_roles = frappe.get_roles(frappe.session.user)
    app_roles = [r for r in user_roles if r.startswith("NO")]
    return bool(app_roles) or "System Manager" in user_roles
