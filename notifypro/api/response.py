# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Standard API Response Helpers
"""
import frappe
from frappe import _


def success(data=None, message=None, status_code=200):
    response = {"status": "success"}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = _(message)
    frappe.response["http_status_code"] = status_code
    return response


def error(message, error_code=None, details=None, status_code=400):
    response = {"status": "error", "message": _(message)}
    if error_code:
        response["error_code"] = error_code
    if details:
        response["details"] = details
    frappe.response["http_status_code"] = status_code
    return response


def paginated(data, total, page=1, page_size=20):
    return {
        "status": "success",
        "data": data,
        "meta": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": -(-total // page_size),
        },
    }
