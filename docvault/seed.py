# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""
DocVault — Seed Data
Runs on `after_migrate` to ensure reference data exists.
"""
import frappe
from frappe import _


def seed_data():
    """Idempotent seed — safe to run multiple times."""
    _seed_settings()
    _seed_categories()
    _seed_folders()
    frappe.db.commit()


def _seed_settings():
    settings_dt = "DV Settings"
    if not frappe.db.exists("DocType", settings_dt):
        return
    try:
        if not frappe.db.exists(settings_dt, settings_dt):
            frappe.new_doc(settings_dt).insert(ignore_permissions=True)
    except Exception:
        pass


def _seed_categories():
    if not frappe.db.exists("DocType", "DV Category"):
        return
    categories = [
        {"category_name": "General", "description": _("General documents"), "icon": "folder", "color": "#6B7280"},
        {"category_name": "Contracts", "description": _("Legal contracts and agreements"), "icon": "file-text", "color": "#3B82F6", "default_retention_days": 2555},
        {"category_name": "Invoices", "description": _("Financial invoices and receipts"), "icon": "credit-card", "color": "#10B981", "default_retention_days": 1825},
        {"category_name": "HR Documents", "description": _("Employee-related documents"), "icon": "users", "color": "#8B5CF6", "default_retention_days": 3650},
        {"category_name": "Legal", "description": _("Legal and compliance documents"), "icon": "shield", "color": "#EF4444", "default_retention_days": 3650, "requires_approval": 1},
        {"category_name": "Technical", "description": _("Technical documentation"), "icon": "tool", "color": "#F59E0B"},
        {"category_name": "Policies", "description": _("Company policies and procedures"), "icon": "book", "color": "#6366F1", "requires_approval": 1},
        {"category_name": "Reports", "description": _("Business reports and analysis"), "icon": "bar-chart-2", "color": "#EC4899"},
    ]
    for cat in categories:
        if not frappe.db.exists("DV Category", {"category_name": cat["category_name"]}):
            doc = frappe.new_doc("DV Category")
            doc.update(cat)
            doc.insert(ignore_permissions=True)


def _seed_folders():
    if not frappe.db.exists("DocType", "DV Folder"):
        return
    folders = [
        {"folder_name": "Documents", "description": _("Root folder for all documents")},
        {"folder_name": "Archive", "description": _("Archived documents")},
        {"folder_name": "Templates", "description": _("Document templates")},
        {"folder_name": "Shared", "description": _("Shared across departments")},
    ]
    for f in folders:
        if not frappe.db.exists("DV Folder", {"folder_name": f["folder_name"]}):
            doc = frappe.new_doc("DV Folder")
            doc.update(f)
            doc.insert(ignore_permissions=True)
