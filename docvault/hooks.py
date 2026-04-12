# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

app_name = "docvault"
app_title = "DocVault"
app_publisher = "Arkan Lab"
app_description = "Enterprise Document Management System for Frappe"
app_email = "dev@arkan.it.com"
app_license = "mit"
app_icon = "/assets/docvault/images/docvault_icon.svg"
app_color = "#059669"
app_logo_url = "/assets/docvault/images/docvault-logo.svg"

# Required Apps
required_apps = ["frappe", "frappe_visual", "arkan_help", "base_base"]

# Feature Registry (Open Core)
app_feature_registry = {
    "document_upload": "free",
    "version_control": "free",
    "basic_search": "free",
    "folder_management": "free",
    "basic_sharing": "free",
    "tags_categories": "free",
    "approval_workflows": "premium",
    "ocr_extraction": "premium",
    "full_text_search": "premium",
    "compliance_management": "premium",
    "retention_policies": "premium",
    "external_storage": "premium",
    "portal_sharing": "premium",
    "ai_classification": "premium",
    "watermarking": "premium",
    "controlled_documents": "premium",
}

# Apps Screen
add_to_apps_screen = [
    {
        "name": "docvault",
        "logo": "/assets/docvault/images/docvault_icon.svg",
        "title": "DocVault",
        "route": "/app/docvault",
        "has_permission": "docvault.api.permissions.has_app_permission",
    }
]

# Includes in <head>
app_include_css = ["/assets/docvault/css/docvault_combined.css"]
app_include_js = ["/assets/docvault/js/docvault_combined.js"]

# Installation
before_install = "docvault.install.before_install"
after_install = "docvault.install.after_install"
after_migrate = ["docvault.seed.seed_data"]
before_uninstall = "docvault.install.before_uninstall"

# Boot Session
boot_session = "docvault.boot.boot_session"

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "docvault.services.retention_service.check_retention_policies",
        "docvault.services.compliance_service.check_review_dates",
    ],
    "hourly": [
        "docvault.services.search_service.index_pending_documents",
    ],
    "weekly": [
        "docvault.services.analytics_service.generate_storage_report",
    ],
}

# Document Events
doc_events = {
    "File": {
        "after_insert": "docvault.events.file_events.on_file_upload",
    },
}

# Fixtures
fixtures = [
    {"dt": "Role", "filters": [["name", "like", "DV%"]]},
    {"dt": "Workspace", "filters": [["module", "like", "Docvault%"]]},
    {"dt": "Desktop Icon", "filters": [["app", "=", "docvault"]]},
]

# Website Route Rules
website_route_rules = [
    {"from_route": "/docvault-about", "to_route": "docvault_about"},
    {"from_route": "/docvault-onboarding", "to_route": "docvault_onboarding"},
]

# Global Search
global_search_doctypes = {
    "Default": [
        {"doctype": "DV Document", "index": 1},
        {"doctype": "DV Folder", "index": 2},
        {"doctype": "DV Category", "index": 3},
        {"doctype": "DV Controlled Document", "index": 4},
    ]
}

export_python_type_annotations = True

# CAPS Integration
caps_capabilities = [
    {"name": "DV_view_dashboard", "category": "Module", "description": "عرض لوحة التحكم"},
    {"name": "DV_manage_documents", "category": "Module", "description": "إدارة الوثائق"},
    {"name": "DV_manage_folders", "category": "Module", "description": "إدارة المجلدات"},
    {"name": "DV_manage_compliance", "category": "Module", "description": "إدارة الامتثال"},
    {"name": "DV_manage_storage", "category": "Module", "description": "إدارة التخزين"},
    {"name": "DV_create_document", "category": "Action", "description": "إنشاء وثيقة"},
    {"name": "DV_approve_document", "category": "Action", "description": "اعتماد وثيقة"},
    {"name": "DV_publish_document", "category": "Action", "description": "نشر وثيقة"},
    {"name": "DV_delete_document", "category": "Action", "description": "حذف وثيقة"},
    {"name": "DV_share_externally", "category": "Action", "description": "مشاركة خارجية"},
    {"name": "DV_bulk_download", "category": "Action", "description": "تحميل جماعي"},
    {"name": "DV_manage_retention", "category": "Action", "description": "إدارة الاحتفاظ"},
    {"name": "DV_checkout_document", "category": "Action", "description": "استعارة وثيقة"},
    {"name": "DV_view_confidential", "category": "Field", "description": "عرض السري"},
    {"name": "DV_view_audit_trail", "category": "Field", "description": "عرض سجل التدقيق"},
    {"name": "DV_view_access_logs", "category": "Field", "description": "عرض سجل الوصول"},
    {"name": "DV_export_reports", "category": "Report", "description": "تصدير التقارير"},
    {"name": "DV_view_storage_reports", "category": "Report", "description": "تقارير التخزين"},
    {"name": "DV_view_compliance_reports", "category": "Report", "description": "تقارير الامتثال"},
    {"name": "DV_view_usage_analytics", "category": "Report", "description": "تحليلات الاستخدام"},
]

caps_field_maps = [
    {"capability": "DV_view_confidential", "doctype": "DV Document", "field": "confidential_notes", "behavior": "hide"},
    {"capability": "DV_view_audit_trail", "doctype": "DV Audit Trail", "field": "ip_address", "behavior": "mask"},
]
