# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from docvault.api.response import success, error


@frappe.whitelist()
def search(query, folder=None, category=None, tags=None, file_type=None, page=1, page_size=20):
    """Search documents in DocVault."""
    frappe.has_permission("DV Document", "read", throw=True)
    from docvault.services.search_service import SearchService
    try:
        if isinstance(tags, str):
            tags = frappe.parse_json(tags)
        result = SearchService.search(
            query=query,
            folder=folder,
            category=category,
            tags=tags,
            file_type=file_type,
            page=int(page),
            page_size=int(page_size),
        )
        return success(data=result)
    except Exception as e:
        return error(str(e), error_code="DV_SEARCH_FAILED")


@frappe.whitelist()
def get_folder_tree(parent=None):
    """Get folder hierarchy."""
    frappe.has_permission("DV Folder", "read", throw=True)
    filters = {}
    if parent:
        filters["parent_folder"] = parent
    else:
        filters["parent_folder"] = ["is", "not set"]

    folders = frappe.get_all("DV Folder",
        filters=filters,
        fields=["name", "folder_name", "parent_folder", "description"],
        order_by="folder_name asc",
    )
    for folder in folders:
        folder["doc_count"] = frappe.db.count("DV Document", {"folder": folder.name})
        folder["has_children"] = bool(frappe.db.count("DV Folder", {"parent_folder": folder.name}))
    return success(data=folders)


@frappe.whitelist()
def get_categories():
    """Get all document categories."""
    frappe.has_permission("DV Category", "read", throw=True)
    categories = frappe.get_all("DV Category",
        fields=["name", "category_name", "parent_category", "description"],
        order_by="category_name asc",
    )
    for cat in categories:
        cat["doc_count"] = frappe.db.count("DV Document", {"category": cat.name})
    return success(data=categories)


@frappe.whitelist()
def get_tags():
    """Get all tags with usage count."""
    frappe.has_permission("DV Tag", "read", throw=True)
    tags = frappe.get_all("DV Tag",
        fields=["name", "tag_name", "color"],
        order_by="tag_name asc",
    )
    for tag in tags:
        tag["usage_count"] = frappe.db.count("DV Document Tag", {"tag": tag.name})
    return success(data=tags)


@frappe.whitelist()
def share_document(document_name, shared_with=None, access_level="View", expiry=None, password=None):
    """Create a share link for a document."""
    frappe.has_permission("DV Document", "write", throw=True)
    try:
        import secrets
        link_key = secrets.token_urlsafe(32)
        share = frappe.get_doc({
            "doctype": "DV Share Link",
            "document": document_name,
            "shared_with": shared_with,
            "access_level": access_level,
            "link_key": link_key,
            "expiry_date": expiry,
            "password_protected": 1 if password else 0,
        }).insert()
        return success(data={
            "share_link": share.name,
            "link_key": link_key,
            "expiry": expiry,
        }, message="Share link created")
    except Exception as e:
        return error(str(e), error_code="DV_SHARE_FAILED")


@frappe.whitelist()
def get_audit_trail(document_name, page=1, page_size=20):
    """Get audit trail for a document."""
    frappe.has_permission("DV Audit Trail", "read", throw=True)
    page = int(page)
    page_size = int(page_size)
    total = frappe.db.count("DV Audit Trail", {"document": document_name})
    trails = frappe.get_all("DV Audit Trail",
        filters={"document": document_name},
        fields=["name", "action", "user", "details", "ip_address", "creation"],
        order_by="creation desc",
        start=(page - 1) * page_size,
        limit_page_length=page_size,
    )
    return success(data={
        "trails": trails,
        "total": total,
        "page": page,
        "page_size": page_size,
    })
