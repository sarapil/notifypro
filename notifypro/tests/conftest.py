# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest


@pytest.fixture
def np_channel():
    """Create a test NP Channel."""
    if frappe.db.exists("NP Channel", "test-email-channel"):
        return frappe.get_doc("NP Channel", "test-email-channel")
    doc = frappe.get_doc({
        "doctype": "NP Channel",
        "name": "test-email-channel",
        "channel_name": "Test Email",
        "channel_type": "Email",
        "enabled": 1,
        "is_default": 1,
        "priority": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    frappe.delete_doc("NP Channel", doc.name, force=True)
    frappe.db.commit()


@pytest.fixture
def np_template():
    """Create a test NP Template."""
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "NP Template",
        "template_name": f"Test Template {name}",
        "channel_type": "Email",
        "content": "Hello {{ recipient_name }}, your {{ doctype }} is ready.",
        "enabled": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    if frappe.db.exists("NP Template", doc.name):
        frappe.delete_doc("NP Template", doc.name, force=True)
        frappe.db.commit()


@pytest.fixture
def np_category():
    """Create a test NP Category."""
    if frappe.db.exists("NP Category", "test-category"):
        return frappe.get_doc("NP Category", "test-category")
    doc = frappe.get_doc({
        "doctype": "NP Category",
        "category_name": "Test Category",
        "description": "For testing",
        "enabled": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    frappe.delete_doc("NP Category", doc.name, force=True)
    frappe.db.commit()
