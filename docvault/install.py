# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DocVault Installation Scripts
"""
import frappe
from frappe import _


def before_install():
    """Pre-installation checks."""
    pass


def after_install():
    """Post-installation setup."""
    create_roles()
    create_settings()
    from docvault.desktop_utils import inject_app_desktop_icon
    inject_app_desktop_icon(
        app="docvault",
        label="DocVault",
        route="/app/docvault",
        logo_url="/assets/docvault/images/docvault-logo.svg",
        bg_color="#059669",
    )
    frappe.db.commit()
    frappe.msgprint(_("DocVault installed successfully!"))


def create_roles():
    """Create default DocVault roles."""
    roles = [
        {"role_name": "DV Administrator", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV Manager", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV Author", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV Reviewer", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV Reader", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV Compliance Officer", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV External User", "desk_access": 1, "is_custom": 1},
        {"role_name": "DV Archivist", "desk_access": 1, "is_custom": 1}
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)


def create_settings():
    """Create singleton settings record if doctype exists."""
    settings_dt = "DV Settings"
    if frappe.db.exists("DocType", settings_dt):
        if not frappe.db.exists(settings_dt, settings_dt):
            settings = frappe.new_doc(settings_dt)
            settings.insert(ignore_permissions=True)


def before_uninstall():
    """Cleanup before uninstall."""
    pass
