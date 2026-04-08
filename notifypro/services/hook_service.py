# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Hook Trigger Execution Service
"""
import frappe
from frappe import _


def execute_trigger(trigger_name: str, doc_name: str, doctype: str):
    """Execute a hook trigger for a document event."""
    if not frappe.db.exists("NP Hook Trigger", trigger_name):
        return
    trigger = frappe.get_doc("NP Hook Trigger", trigger_name)
    doc = frappe.get_doc(doctype, doc_name)

    # Evaluate conditions
    for condition in trigger.get("conditions", []):
        field_val = doc.get(condition.field)
        if not _evaluate_condition(field_val, condition.operator, condition.value):
            return

    # Send notification
    from notifypro.services.template_service import TemplateService
    for tmpl in trigger.get("templates", []):
        context = {"doc": doc, "frappe": frappe}
        content = TemplateService.render(tmpl.template, context)
        _create_message(doc, content, tmpl.channel)


def _evaluate_condition(field_val, operator, expected):
    match operator:
        case "equals": return str(field_val) == str(expected)
        case "not_equals": return str(field_val) != str(expected)
        case "contains": return str(expected) in str(field_val)
        case "greater_than": return float(field_val or 0) > float(expected or 0)
        case "less_than": return float(field_val or 0) < float(expected or 0)
        case _: return True


def _create_message(doc, content, channel):
    msg = frappe.new_doc("NP Message")
    msg.content = content
    msg.channel = channel
    msg.reference_doctype = doc.doctype
    msg.reference_name = doc.name
    msg.recipient = doc.owner
    msg.status = "Queued"
    msg.insert(ignore_permissions=True)
