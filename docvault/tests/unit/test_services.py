# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest

from docvault.services.search_service import SearchService
from docvault.services.compliance_service import ComplianceService


class TestSearchServiceSearchDocuments:
    """Test SearchService.search_documents."""

    def test_returns_list(self):
        results = SearchService.search_documents("nonexistent-xyz-query")
        assert isinstance(results, list)

    def test_search_by_title(self, dv_document):
        results = SearchService.search_documents(dv_document.title)
        names = [r["name"] for r in results]
        assert dv_document.name in names

    def test_filter_by_category(self, dv_category, dv_document):
        dv_document.category = dv_category.name
        dv_document.save(ignore_permissions=True)
        results = SearchService.search_documents(
            dv_document.title, category=dv_category.name
        )
        names = [r["name"] for r in results]
        assert dv_document.name in names

    def test_filter_by_folder(self, dv_folder, dv_document):
        dv_document.folder = dv_folder.name
        dv_document.save(ignore_permissions=True)
        results = SearchService.search_documents(
            dv_document.title, folder=dv_folder.name
        )
        names = [r["name"] for r in results]
        assert dv_document.name in names

    def test_respects_limit(self):
        results = SearchService.search_documents("test", limit=1)
        assert len(results) <= 1


class TestComplianceServiceLogAccess:
    """Test ComplianceService.log_access."""

    def test_log_access_does_not_throw(self, dv_document):
        # Should not raise even if DV Audit Trail doesn't exist
        ComplianceService.log_access(dv_document.name, "View")

    def test_log_access_with_custom_action(self, dv_document):
        ComplianceService.log_access(dv_document.name, "Download")
