# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from notifypro.api.response import success, error


@frappe.whitelist()
def render(template_name, context=None):
    """Render a notification template with context."""
    frappe.has_permission("NP Template", "read", throw=True)
    from notifypro.services.template_service import TemplateService
    try:
        if isinstance(context, str):
            context = frappe.parse_json(context)
        result = TemplateService.render_template(template_name, context or {})
        return success(data=result)
    except Exception as e:
        return error(str(e), error_code="NP_TEMPLATE_RENDER_FAILED")


@frappe.whitelist()
def preview(template_name, context=None):
    """Preview a template without sending."""
    frappe.has_permission("NP Template", "read", throw=True)
    from notifypro.services.template_service import TemplateService
    try:
        if isinstance(context, str):
            context = frappe.parse_json(context)
        result = TemplateService.render_template(template_name, context or {})
        return success(data={"preview": result, "template": template_name})
    except Exception as e:
        return error(str(e), error_code="NP_TEMPLATE_PREVIEW_FAILED")


@frappe.whitelist()
def list_templates(channel=None):
    """List available templates, optionally filtered by channel."""
    frappe.has_permission("NP Template", "read", throw=True)
    filters = {}
    if channel:
        filters["channel"] = channel
    templates = frappe.get_all("NP Template",
        filters=filters,
        fields=["name", "template_name", "channel", "subject", "enabled"],
        order_by="template_name asc",
    )
    return success(data=templates)
