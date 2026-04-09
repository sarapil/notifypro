# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "channel", "label": _("Channel"), "fieldtype": "Data", "width": 150},
        {"fieldname": "total", "label": _("Total Sent"), "fieldtype": "Int", "width": 120},
        {"fieldname": "delivered", "label": _("Delivered"), "fieldtype": "Int", "width": 120},
        {"fieldname": "failed", "label": _("Failed"), "fieldtype": "Int", "width": 120},
        {"fieldname": "delivery_rate", "label": _("Delivery Rate %"), "fieldtype": "Percent", "width": 130},
    ]


def get_data(filters):
    conditions = ""
    values = {}
    if filters and filters.get("from_date"):
        conditions += " AND creation >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters and filters.get("to_date"):
        conditions += " AND creation <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    results = frappe.db.sql(
        f"""
        SELECT
            channel,
            COUNT(*) as total,
            SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) as delivered,
            SUM(CASE WHEN status = 'Failed' THEN 1 ELSE 0 END) as failed
        FROM `tabNP Notification Log`
        WHERE 1=1 {conditions}
        GROUP BY channel
        ORDER BY total DESC
        """,
        values,
        as_dict=True,
    )

    for row in results:
        row["delivery_rate"] = (row["delivered"] / row["total"] * 100) if row["total"] else 0

    return results


def get_chart(data):
    if not data:
        return None
    return {
        "data": {
            "labels": [d["channel"] for d in data],
            "datasets": [
                {"name": _("Delivered"), "values": [d["delivered"] for d in data]},
                {"name": _("Failed"), "values": [d["failed"] for d in data]},
            ],
        },
        "type": "bar",
    }
