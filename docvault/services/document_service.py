# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault — Document Service
Core document management operations.
"""
import frappe
from frappe import _


class DocumentService:
    @staticmethod
    def create_document(title: str, category: str, file_url: str, folder: str | None = None) -> str:
        """Create a new DV Document."""
        frappe.has_permission("DV Document", "create", throw=True)
        doc = frappe.new_doc("DV Document")
        doc.title = title
        doc.category = category
        doc.file = file_url
        doc.folder = folder
        doc.status = "Draft"
        doc.version_number = 1
        doc.insert()
        # Create initial version
        DocumentService._create_version(doc.name, file_url, "Initial upload", 1)
        return doc.name

    @staticmethod
    def create_from_file(file_doc_name: str):
        """Auto-create DV Document from a Frappe File upload."""
        file_doc = frappe.get_doc("File", file_doc_name)
        title = file_doc.file_name or file_doc.name
        doc = frappe.new_doc("DV Document")
        doc.title = title
        doc.file = file_doc.file_url
        doc.source_file = file_doc.name
        doc.status = "Draft"
        doc.version_number = 1
        doc.insert(ignore_permissions=True)
        DocumentService._create_version(doc.name, file_doc.file_url, "Auto-captured", 1)
        frappe.db.commit()

    @staticmethod
    def upload_new_version(document_name: str, file_url: str, change_notes: str = "") -> str:
        """Upload a new version of an existing document."""
        doc = frappe.get_doc("DV Document", document_name)
        frappe.has_permission("DV Document", "write", doc=doc, throw=True)
        new_version = (doc.version_number or 0) + 1
        doc.file = file_url
        doc.version_number = new_version
        doc.save()
        version_name = DocumentService._create_version(doc.name, file_url, change_notes, new_version)
        return version_name

    @staticmethod
    def _create_version(document: str, file_url: str, notes: str, version_no: int) -> str:
        ver = frappe.new_doc("DV Version")
        ver.document = document
        ver.version_no = version_no
        ver.file = file_url
        ver.change_notes = notes
        ver.created_by = frappe.session.user
        ver.insert(ignore_permissions=True)
        return ver.name

    @staticmethod
    def checkout(document_name: str, reason: str = "") -> str:
        """Check out a document for exclusive editing."""
        doc = frappe.get_doc("DV Document", document_name)
        if doc.checked_out_by:
            frappe.throw(_("Document is already checked out by {0}").format(doc.checked_out_by))
        doc.checked_out_by = frappe.session.user
        doc.checked_out_at = frappe.utils.now()
        doc.save()
        if frappe.db.exists("DocType", "DV Checkout"):
            co = frappe.new_doc("DV Checkout")
            co.document = document_name
            co.checked_out_by = frappe.session.user
            co.reason = reason
            co.insert(ignore_permissions=True)
        return doc.name

    @staticmethod
    def checkin(document_name: str):
        """Check in a document after editing."""
        doc = frappe.get_doc("DV Document", document_name)
        if doc.checked_out_by != frappe.session.user and frappe.session.user != "Administrator":
            frappe.throw(_("Only the user who checked out this document can check it in"))
        doc.checked_out_by = None
        doc.checked_out_at = None
        doc.save()
