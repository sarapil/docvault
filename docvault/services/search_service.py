# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault — Search & Indexing Service
"""
import frappe


def index_pending_documents():
    """Hourly: index documents that need search indexing."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    if not frappe.db.exists("DocType", "DV Document"):
        return
    # Find documents not yet indexed
    unindexed = frappe.get_all(
        "DV Document",
        filters={"indexed": 0},
        fields=["name", "title", "file"],
        limit=50,
    )
    for doc in unindexed:
        try:
            frappe.db.set_value("DV Document", doc.name, "indexed", 1)
        except Exception:
            frappe.log_error(title=f"DocVault indexing failed: {doc.name}")
    frappe.db.commit()


class SearchService:
    @staticmethod
    def search_documents(query: str, category: str | None = None, folder: str | None = None, limit: int = 20) -> list[dict]:
        """Search documents by title and content."""
        filters = {}
        if category:
            filters["category"] = category
        if folder:
            filters["folder"] = folder
        # Basic title search
        return frappe.get_all(
            "DV Document",
            filters=filters,
            or_filters={"title": ["like", f"%{query}%"]},
            fields=["name", "title", "category", "folder", "status", "creation", "owner"],
            order_by="modified desc",
            limit=limit,
        )
