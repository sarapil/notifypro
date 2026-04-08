# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Boot Session
"""
import frappe


def boot_session(bootinfo):
    """Add NotifyPro data to boot session."""
    if frappe.session.user == "Guest":
        return

    bootinfo.notifypro = {
        "has_access": True,
    }
