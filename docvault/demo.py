# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""
DocVault — Demo Data
Load / clear demo data for showcasing app features.
"""
import frappe
from frappe import _


def load_demo_data():
    """Load realistic demo records for DocVault."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return

    # Demo categories
    categories = [
        {"category_name": "Contracts", "icon": "file-text", "color": "#6366F1",
         "default_retention_days": 2555, "requires_approval": 1},
        {"category_name": "Invoices", "icon": "receipt", "color": "#10B981",
         "default_retention_days": 1825},
        {"category_name": "HR Documents", "icon": "users", "color": "#F59E0B",
         "default_retention_days": 3650, "requires_approval": 1},
        {"category_name": "Policies", "icon": "shield", "color": "#EF4444",
         "default_retention_days": 0},
    ]
    for cat in categories:
        if not frappe.db.exists("DV Category", {"category_name": cat["category_name"]}):
            doc = frappe.get_doc({"doctype": "DV Category", **cat})
            doc.insert(ignore_permissions=True)

    # Demo folders
    folders = [
        {"folder_name": "Finance", "is_root": 1},
        {"folder_name": "Human Resources", "is_root": 1},
        {"folder_name": "Legal", "is_root": 1},
    ]
    for fld in folders:
        if not frappe.db.exists("DV Folder", {"folder_name": fld["folder_name"]}):
            doc = frappe.get_doc({"doctype": "DV Folder", **fld})
            doc.insert(ignore_permissions=True)

    # Demo tags
    tags = [
        {"tag_name": "Urgent", "color": "#EF4444"},
        {"tag_name": "Confidential", "color": "#7C3AED"},
        {"tag_name": "Archived", "color": "#6B7280"},
    ]
    for tag in tags:
        if not frappe.db.exists("DV Tag", {"tag_name": tag["tag_name"]}):
            doc = frappe.get_doc({"doctype": "DV Tag", **tag})
            doc.insert(ignore_permissions=True)

    # Demo documents
    documents = [
        {"title": "Service Agreement 2024", "file": "/files/demo-contract.pdf",
         "status": "Active", "version_number": 2, "confidentiality": "Internal"},
        {"title": "Q4 Financial Report", "file": "/files/demo-report.pdf",
         "status": "Active", "version_number": 1, "confidentiality": "Confidential"},
        {"title": "Employee Handbook v3", "file": "/files/demo-handbook.pdf",
         "status": "Draft", "version_number": 3, "confidentiality": "Public"},
        {"title": "Data Protection Policy", "file": "/files/demo-policy.pdf",
         "status": "Active", "version_number": 1, "confidentiality": "Internal"},
        {"title": "Expired NDA 2022", "file": "/files/demo-nda.pdf",
         "status": "Archived", "version_number": 1, "confidentiality": "Confidential"},
    ]
    for d in documents:
        if not frappe.db.exists("DV Document", {"title": d["title"]}):
            doc = frappe.get_doc({"doctype": "DV Document", **d})
            doc.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.msgprint(_("DocVault demo data loaded successfully."))


def clear_demo_data():
    """Remove all demo data."""
    for dt in ["DV Document", "DV Tag", "DV Folder", "DV Category"]:
        for name in frappe.get_all(dt, filters={"owner": "Administrator"}, pluck="name", limit=50):
            try:
                frappe.delete_doc(dt, name, force=True)
            except Exception:
                pass
    frappe.db.commit()
    frappe.msgprint(_("DocVault demo data cleared."))
