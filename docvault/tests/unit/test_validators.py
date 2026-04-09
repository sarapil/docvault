# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest

from docvault.utils.validators import validate_required, validate_max_length


class TestValidateRequired:
    def test_raises_on_none(self):
        with pytest.raises(frappe.exceptions.ValidationError):
            validate_required(None, "Title")

    def test_raises_on_empty_string(self):
        with pytest.raises(frappe.exceptions.ValidationError):
            validate_required("", "Title")

    def test_passes_on_valid_string(self):
        validate_required("hello", "Title")

    def test_passes_on_number(self):
        validate_required(42, "Count")


class TestValidateMaxLength:
    def test_raises_when_too_long(self):
        with pytest.raises(frappe.exceptions.ValidationError):
            validate_max_length("a" * 150, 100, "Title")

    def test_passes_when_within_limit(self):
        validate_max_length("short", 100, "Title")

    def test_passes_on_none(self):
        validate_max_length(None, 100, "Title")

    def test_passes_on_exact_length(self):
        validate_max_length("a" * 100, 100, "Title")
