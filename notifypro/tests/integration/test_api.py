# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""Integration tests for NotifyPro API endpoints."""
import frappe
from frappe.tests.utils import FrappeTestCase


class TestNotificationAPI(FrappeTestCase):
    def test_send_notification_api(self):
        """Test the send_notification whitelisted endpoint."""
        from notifypro.api.v1.notification import send_notification

        # Create a test channel first
        ch_name = frappe.generate_hash(length=10)
        ch = frappe.get_doc({
            "doctype": "NP Channel",
            "channel_name": f"API Test {ch_name}",
            "channel_type": "Email",
            "enabled": 1,
            "is_default": 1,
            "priority": 1,
        })
        ch.insert(ignore_permissions=True)
        frappe.db.commit()

        try:
            result = send_notification(
                recipient="Administrator",
                subject="Integration Test",
                content="Test content from integration test",
            )
            self.assertIsInstance(result, dict)
            self.assertIn("status", result)
        finally:
            frappe.delete_doc("NP Channel", ch.name, force=True)
            frappe.db.commit()

    def test_get_notifications_api(self):
        """Test fetching notifications list."""
        from notifypro.api.v1.notification import get_notifications

        result = get_notifications()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("status"), "success")


class TestChannelAPI(FrappeTestCase):
    def test_get_channels(self):
        """Test listing channels."""
        from notifypro.api.v1.channel import get_channels

        result = get_channels()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("status"), "success")

    def test_get_channel_status(self):
        """Test channel health status endpoint."""
        from notifypro.api.v1.channel import get_channel_status

        result = get_channel_status()
        self.assertIsInstance(result, dict)


class TestTemplateAPI(FrappeTestCase):
    def test_get_templates(self):
        """Test listing templates."""
        from notifypro.api.v1.template import get_templates

        result = get_templates()
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("status"), "success")

    def test_preview_template(self):
        """Test template preview with sample data."""
        from notifypro.api.v1.template import preview_template

        # Create a template
        name = frappe.generate_hash(length=10)
        t = frappe.get_doc({
            "doctype": "NP Template",
            "template_name": f"Preview Test {name}",
            "channel_type": "Email",
            "content": "Hello {{ name }}",
            "enabled": 1,
        })
        t.insert(ignore_permissions=True)
        frappe.db.commit()

        try:
            result = preview_template(
                template_name=t.name,
                sample_data='{"name": "Test User"}',
            )
            self.assertIsInstance(result, dict)
        finally:
            frappe.delete_doc("NP Template", t.name, force=True)
            frappe.db.commit()
