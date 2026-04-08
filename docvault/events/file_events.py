# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault — File Upload Event Handler
"""
import frappe


def on_file_upload(doc, method):
    """Auto-create DV Document when a file is uploaded if auto-capture is enabled."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    try:
        if not frappe.db.table_exists("tabDV Settings"):
            return
        settings = frappe.get_cached_doc("DV Settings")
        if not getattr(settings, "auto_capture_uploads", False):
            return
        if frappe.db.exists("DV Document", {"source_file": doc.name}):
            return
        frappe.enqueue(
            "docvault.services.document_service.create_from_file",
            queue="short",
            file_doc_name=doc.name,
        )
    except Exception:
        pass
