# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""Unit tests for NotifyPro validators."""
import frappe
from frappe.tests.utils import FrappeTestCase


class TestValidators(FrappeTestCase):
    def test_validate_required_passes(self):
        """Non-empty value should not raise."""
        from notifypro.utils.validators import validate_required
        # Should not raise
        validate_required("some value", "Test Field")

    def test_validate_required_fails(self):
        """Empty value should raise ValidationError."""
        from notifypro.utils.validators import validate_required
        with self.assertRaises(frappe.ValidationError):
            validate_required("", "Test Field")

    def test_validate_required_none_fails(self):
        """None value should raise ValidationError."""
        from notifypro.utils.validators import validate_required
        with self.assertRaises(frappe.ValidationError):
            validate_required(None, "Test Field")

    def test_validate_max_length_passes(self):
        """Short string should not raise."""
        from notifypro.utils.validators import validate_max_length
        validate_max_length("abc", 10, "Test Field")

    def test_validate_max_length_fails(self):
        """Long string should raise."""
        from notifypro.utils.validators import validate_max_length
        with self.assertRaises(frappe.ValidationError):
            validate_max_length("a" * 200, 100, "Test Field")

    def test_validate_max_length_none_passes(self):
        """None value should not raise (field not set)."""
        from notifypro.utils.validators import validate_max_length
        validate_max_length(None, 100, "Test Field")
