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
        {"fieldname": "name", "label": _("Document"), "fieldtype": "Link", "options": "DV Document", "width": 180},
        {"fieldname": "title", "label": _("Title"), "fieldtype": "Data", "width": 220},
        {"fieldname": "category", "label": _("Category"), "fieldtype": "Link", "options": "DV Category", "width": 150},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "version_number", "label": _("Version"), "fieldtype": "Int", "width": 80},
        {"fieldname": "owner", "label": _("Uploaded By"), "fieldtype": "Link", "options": "User", "width": 150},
        {"fieldname": "modified", "label": _("Last Modified"), "fieldtype": "Datetime", "width": 160},
    ]


def get_data(filters):
    conditions = {}
    if filters and filters.get("category"):
        conditions["category"] = filters["category"]
    if filters and filters.get("status"):
        conditions["status"] = filters["status"]
    if filters and filters.get("from_date"):
        conditions["creation"] = [">=", filters["from_date"]]
    if filters and filters.get("to_date"):
        conditions["modified"] = ["<=", filters["to_date"]]

    return frappe.get_all(
        "DV Document",
        filters=conditions,
        fields=["name", "title", "category", "status", "version_number", "owner", "modified"],
        order_by="modified desc",
        limit=100,
    )


def get_chart(data):
    if not data:
        return None
    status_counts = {}
    for row in data:
        s = row.get("status") or "Unknown"
        status_counts[s] = status_counts.get(s, 0) + 1
    return {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{"name": _("Documents"), "values": list(status_counts.values())}],
        },
        "type": "donut",
    }
