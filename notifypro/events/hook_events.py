# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — DocType Event Handler for Hook Triggers
"""
import frappe


def on_doc_event(doc, method):
    """Called on all document events to check for NP Hook Triggers."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    try:
        if not frappe.db.table_exists("tabNP Hook Trigger"):
            return
        triggers = frappe.get_all(
            "NP Hook Trigger",
            filters={"enabled": 1, "source_doctype": doc.doctype, "event": method.split(".")[-1]},
            fields=["name"],
        )
        if not triggers:
            return
        for trigger in triggers:
            frappe.enqueue(
                "notifypro.services.hook_service.execute_trigger",
                queue="short",
                trigger_name=trigger.name,
                doc_name=doc.name,
                doctype=doc.doctype,
            )
    except Exception:
        pass
