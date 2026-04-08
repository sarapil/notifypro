# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Input Validation Helpers
"""
import frappe
from frappe import _


def validate_required(value, field_name: str):
    """Raise if value is falsy."""
    if not value:
        frappe.throw(_("{0} is required").format(field_name))


def validate_max_length(value: str, max_len: int, field_name: str):
    """Raise if string exceeds max length."""
    if value and len(value) > max_len:
        frappe.throw(_("{0} must not exceed {1} characters").format(field_name, max_len))
