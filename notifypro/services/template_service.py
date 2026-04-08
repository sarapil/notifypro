# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Template Service
Renders notification templates with Jinja.
"""
import frappe
from frappe import _
from frappe.utils.jinja import render_template


class TemplateService:
    @staticmethod
    def render(template_name: str, context: dict, channel_type: str | None = None) -> str:
        """Render a notification template with given context."""
        template = frappe.get_cached_doc("NP Template", template_name)
        # Get channel-specific content if available
        content = template.content
        if channel_type and hasattr(template, "channel_contents"):
            for ch in template.channel_contents:
                if ch.channel_type == channel_type:
                    content = ch.content
                    break
        return render_template(content, context)

    @staticmethod
    def get_templates_for_doctype(doctype: str) -> list[dict]:
        """Get all templates applicable to a doctype."""
        return frappe.get_all(
            "NP Template",
            filters={"reference_doctype": doctype, "enabled": 1},
            fields=["name", "template_name", "channel_type"],
        )
