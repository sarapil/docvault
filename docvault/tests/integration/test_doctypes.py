# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest


class TestDVDocument:
    """Integration tests for DV Document DocType."""

    def test_create_document(self, dv_document):
        assert dv_document.name is not None
        assert frappe.db.exists("DV Document", dv_document.name)

    def test_document_default_status(self, dv_document):
        assert dv_document.status == "Draft"

    def test_document_version_number(self, dv_document):
        assert dv_document.version_number == 1

    def test_document_with_category(self, dv_category):
        name = frappe.generate_hash(length=10)
        doc = frappe.get_doc({
            "doctype": "DV Document",
            "title": f"Categorized Doc {name}",
            "file": "/files/test.pdf",
            "category": dv_category.name,
        })
        doc.insert(ignore_permissions=True)
        assert doc.category == dv_category.name
        frappe.delete_doc("DV Document", doc.name, force=True)


class TestDVCategory:
    """Integration tests for DV Category DocType."""

    def test_create_category(self, dv_category):
        assert dv_category.name is not None
        assert frappe.db.exists("DV Category", dv_category.name)

    def test_nested_category(self, dv_category):
        name = frappe.generate_hash(length=10)
        child = frappe.get_doc({
            "doctype": "DV Category",
            "category_name": f"Child Category {name}",
            "parent_category": dv_category.name,
        })
        child.insert(ignore_permissions=True)
        assert child.parent_category == dv_category.name
        frappe.delete_doc("DV Category", child.name, force=True)


class TestDVFolder:
    """Integration tests for DV Folder DocType."""

    def test_create_folder(self, dv_folder):
        assert dv_folder.name is not None
        assert frappe.db.exists("DV Folder", dv_folder.name)

    def test_nested_folder(self, dv_folder):
        name = frappe.generate_hash(length=10)
        child = frappe.get_doc({
            "doctype": "DV Folder",
            "folder_name": f"Child Folder {name}",
            "parent_folder": dv_folder.name,
        })
        child.insert(ignore_permissions=True)
        assert child.parent_folder == dv_folder.name
        frappe.delete_doc("DV Folder", child.name, force=True)


class TestDVTag:
    """Integration tests for DV Tag DocType."""

    def test_create_tag(self, dv_tag):
        assert dv_tag.name is not None
        assert frappe.db.exists("DV Tag", dv_tag.name)
