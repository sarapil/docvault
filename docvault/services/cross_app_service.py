# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault — Cross-App Integration Service

Provides a unified API for other Arkan Lab apps to store, retrieve, and
manage documents through DocVault without directly coupling to its DocTypes.

Supported integrations:
- Vertex  → construction documents (drawings, BOQs, contracts)
- ClinicFlow → medical records (lab results, prescriptions, imaging)
- Masar   → design documents (mood boards, floor plans, revisions)
"""
import frappe
from frappe import _


# Mapping of app prefixes → default categories / folders
APP_DOCUMENT_PROFILES: dict[str, dict] = {
    "vertex": {
        "folder": "Construction",
        "categories": {
            "drawing": "Construction Drawing",
            "boq": "Bill of Quantities",
            "contract": "Contract Document",
            "safety": "Safety Report",
            "progress": "Progress Report",
        },
    },
    "clinicflow": {
        "folder": "Medical Records",
        "categories": {
            "lab_result": "Lab Result",
            "prescription": "Prescription",
            "imaging": "Medical Imaging",
            "consent": "Consent Form",
            "discharge": "Discharge Summary",
        },
    },
    "masar": {
        "folder": "Interior Design",
        "categories": {
            "mood_board": "Mood Board",
            "floor_plan": "Floor Plan",
            "material_spec": "Material Specification",
            "revision": "Design Revision",
            "render": "3D Render",
        },
    },
}


class CrossAppDocumentService:
    """Facade for other Arkan Lab apps to interact with DocVault."""

    @staticmethod
    def store_document(
        app: str,
        title: str,
        file_url: str,
        category_key: str,
        linked_doctype: str | None = None,
        linked_name: str | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Store a document on behalf of another app.

        Args:
            app: Calling app name (e.g. "vertex", "clinicflow", "masar").
            title: Human-readable document title.
            file_url: Frappe file URL for the uploaded file.
            category_key: Short key from APP_DOCUMENT_PROFILES (e.g. "drawing").
            linked_doctype: Optional originating DocType for back-reference.
            linked_name: Optional originating document name.
            tags: Optional list of tag strings.

        Returns:
            Name of the newly created DV Document.
        """
        profile = APP_DOCUMENT_PROFILES.get(app, {})
        folder = profile.get("folder", "General")
        category = profile.get("categories", {}).get(category_key, category_key)

        # Ensure the folder exists
        _ensure_folder(folder)

        doc = frappe.new_doc("DV Document")
        doc.title = title
        doc.category = category
        doc.file = file_url
        doc.folder = folder
        doc.status = "Draft"
        doc.version_number = 1
        if linked_doctype and linked_name:
            doc.linked_doctype = linked_doctype
            doc.linked_name = linked_name
        doc.source_app = app
        doc.insert(ignore_permissions=True)

        if tags:
            for tag in tags:
                doc.add_tag(tag)

        # Create initial version entry
        _create_initial_version(doc.name, file_url)
        return doc.name

    @staticmethod
    def get_documents_for(
        linked_doctype: str,
        linked_name: str,
        category: str | None = None,
    ) -> list[dict]:
        """Retrieve DV Documents linked to a specific source document.

        Useful for dashboard sections: "show all documents attached to this
        VX Project / CF Patient / MS Design Order".
        """
        filters = {
            "linked_doctype": linked_doctype,
            "linked_name": linked_name,
        }
        if category:
            filters["category"] = category
        return frappe.get_all(
            "DV Document",
            filters=filters,
            fields=["name", "title", "category", "file", "status", "version_number", "creation"],
            order_by="creation desc",
        )

    @staticmethod
    def get_latest_version_url(document_name: str) -> str | None:
        """Return the file URL of the latest version."""
        return frappe.db.get_value("DV Document", document_name, "file")


def _ensure_folder(folder_name: str):
    """Create a DV Folder if it doesn't already exist."""
    if not frappe.db.exists("DV Folder", {"folder_name": folder_name}):
        try:
            doc = frappe.new_doc("DV Folder")
            doc.folder_name = folder_name
            doc.insert(ignore_permissions=True)
        except frappe.DuplicateEntryError:
            pass


def _create_initial_version(document_name: str, file_url: str):
    """Create a DV Version record for the initial upload."""
    if frappe.db.exists("DocType", "DV Version"):
        ver = frappe.new_doc("DV Version")
        ver.document = document_name
        ver.file = file_url
        ver.version_number = 1
        ver.change_notes = "Initial upload via cross-app integration"
        ver.insert(ignore_permissions=True)
