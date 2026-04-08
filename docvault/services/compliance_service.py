# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault — Compliance Service
Document control, retention, and audit.
"""
import frappe
from frappe import _


def check_review_dates():
    """Daily: check for controlled documents nearing review dates."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    if not frappe.db.exists("DocType", "DV Controlled Document"):
        return
    today = frappe.utils.today()
    warning_days = 30
    upcoming = frappe.get_all(
        "DV Controlled Document",
        filters={
            "next_review": ["between", [today, frappe.utils.add_days(today, warning_days)]],
            "status": "Effective",
        },
        fields=["name", "document", "next_review", "owner"],
    )
    for item in upcoming:
        frappe.get_doc({
            "doctype": "ToDo",
            "description": _("Document {0} is due for review on {1}").format(item.document, item.next_review),
            "allocated_to": item.owner,
            "reference_type": "DV Controlled Document",
            "reference_name": item.name,
        }).insert(ignore_permissions=True)
    frappe.db.commit()


class ComplianceService:
    @staticmethod
    def log_access(document_name: str, action: str = "View"):
        """Log document access for audit trail."""
        if not frappe.db.exists("DocType", "DV Audit Trail"):
            return
        frappe.get_doc({
            "doctype": "DV Audit Trail",
            "document": document_name,
            "action": action,
            "user": frappe.session.user,
            "ip_address": frappe.local.request_ip if hasattr(frappe.local, "request_ip") else "",
        }).insert(ignore_permissions=True)
