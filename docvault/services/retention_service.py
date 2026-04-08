# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault — Retention Policy Service
"""
import frappe
from frappe import _


def check_retention_policies():
    """Daily: enforce retention policies on documents."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    if not frappe.db.exists("DocType", "DV Retention Policy"):
        return
    policies = frappe.get_all(
        "DV Retention Policy",
        filters={"enabled": 1},
        fields=["name", "category", "retention_years", "action_after"],
    )
    for policy in policies:
        cutoff = frappe.utils.add_years(frappe.utils.today(), -policy.retention_years)
        expired = frappe.get_all(
            "DV Document",
            filters={"category": policy.category, "creation": ["<", cutoff], "status": ["!=", "Archived"]},
            fields=["name"],
        )
        for doc in expired:
            match policy.action_after:
                case "Archive":
                    frappe.db.set_value("DV Document", doc.name, "status", "Archived")
                case "Flag":
                    frappe.db.set_value("DV Document", doc.name, "retention_flagged", 1)
    frappe.db.commit()
