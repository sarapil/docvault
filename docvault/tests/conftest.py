# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest


@pytest.fixture
def dv_category():
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DV Category",
        "category_name": f"Test Category {name}",
    })
    doc.insert(ignore_permissions=True)
    yield doc
    frappe.delete_doc("DV Category", doc.name, force=True)


@pytest.fixture
def dv_folder():
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DV Folder",
        "folder_name": f"Test Folder {name}",
    })
    doc.insert(ignore_permissions=True)
    yield doc
    frappe.delete_doc("DV Folder", doc.name, force=True)


@pytest.fixture
def dv_tag():
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DV Tag",
        "tag_name": f"Test Tag {name}",
    })
    doc.insert(ignore_permissions=True)
    yield doc
    frappe.delete_doc("DV Tag", doc.name, force=True)


@pytest.fixture
def dv_document():
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DV Document",
        "title": f"Test Document {name}",
        "file": "/files/test-file.pdf",
        "status": "Draft",
        "version_number": 1,
    })
    doc.insert(ignore_permissions=True)
    yield doc
    frappe.delete_doc("DV Document", doc.name, force=True)
