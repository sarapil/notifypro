# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro Installation Scripts
"""
import frappe
from frappe import _


def before_install():
    """Pre-installation checks."""
    pass


def after_install():
    """Post-installation setup."""
    create_roles()
    create_settings()
    from notifypro.desktop_utils import inject_app_desktop_icon
    inject_app_desktop_icon(
        app="notifypro",
        label="NotifyPro",
        route="/app/notifypro",
        logo_url="/assets/notifypro/images/notifypro-logo.svg",
        bg_color="#7C3AED",
    )
    frappe.db.commit()
    frappe.msgprint(_("NotifyPro installed successfully!"))


def create_roles():
    """Create default NotifyPro roles."""
    roles = [
        {"role_name": "NP Admin", "desk_access": 1, "is_custom": 1},
        {"role_name": "NP Campaign Manager", "desk_access": 1, "is_custom": 1},
        {"role_name": "NP Template Editor", "desk_access": 1, "is_custom": 1},
        {"role_name": "NP Viewer", "desk_access": 1, "is_custom": 1},
        {"role_name": "NP API User", "desk_access": 1, "is_custom": 1}
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)


def create_settings():
    """Create singleton settings record if doctype exists."""
    settings_dt = "NP Settings"
    if frappe.db.exists("DocType", settings_dt):
        if not frappe.db.exists(settings_dt, settings_dt):
            settings = frappe.new_doc(settings_dt)
            settings.insert(ignore_permissions=True)


def before_uninstall():
    """Cleanup before uninstall."""
    pass
