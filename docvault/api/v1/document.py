# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from docvault.api.response import success, error


@frappe.whitelist()
def upload(file_url=None, folder=None, category=None, tags=None, title=None):
    """Upload a document to DocVault."""
    frappe.has_permission("DV Document", "create", throw=True)
    from docvault.services.document_service import DocumentService
    try:
        if isinstance(tags, str):
            tags = frappe.parse_json(tags)
        result = DocumentService.create_document(
            file_url=file_url,
            folder=folder,
            category=category,
            tags=tags or [],
            title=title,
        )
        return success(data=result, message="Document uploaded successfully")
    except Exception as e:
        frappe.log_error("DocVault Upload Error")
        return error(str(e), error_code="DV_UPLOAD_FAILED")


@frappe.whitelist()
def checkout(document_name):
    """Check out a document for editing."""
    frappe.has_permission("DV Document", "write", throw=True)
    from docvault.services.document_service import DocumentService
    try:
        result = DocumentService.checkout(document_name)
        return success(data=result, message="Document checked out")
    except Exception as e:
        return error(str(e), error_code="DV_CHECKOUT_FAILED")


@frappe.whitelist()
def checkin(document_name, file_url=None, comment=None):
    """Check in a document after editing."""
    frappe.has_permission("DV Document", "write", throw=True)
    from docvault.services.document_service import DocumentService
    try:
        result = DocumentService.checkin(document_name, file_url=file_url, comment=comment)
        return success(data=result, message="Document checked in")
    except Exception as e:
        return error(str(e), error_code="DV_CHECKIN_FAILED")


@frappe.whitelist()
def get_versions(document_name):
    """Get version history of a document."""
    frappe.has_permission("DV Version", "read", throw=True)
    versions = frappe.get_all("DV Version",
        filters={"document": document_name},
        fields=["name", "version_number", "file_url", "file_size", "uploaded_by", "comment", "creation"],
        order_by="version_number desc",
    )
    return success(data=versions)


@frappe.whitelist()
def get_document_info(document_name):
    """Get full document info including metadata."""
    frappe.has_permission("DV Document", "read", throw=True)
    from docvault.services.compliance_service import ComplianceService
    doc = frappe.get_doc("DV Document", document_name)
    ComplianceService.log_access(document_name, "view")
    return success(data={
        "name": doc.name,
        "title": doc.title,
        "file_url": doc.file_url,
        "folder": doc.folder,
        "category": doc.category,
        "status": doc.status,
        "file_size": doc.file_size,
        "current_version": doc.current_version,
        "is_checked_out": doc.is_checked_out,
        "checked_out_by": doc.checked_out_by,
        "tags": [t.tag for t in doc.tags] if hasattr(doc, 'tags') else [],
        "owner": doc.owner,
        "creation": str(doc.creation),
        "modified": str(doc.modified),
    })
