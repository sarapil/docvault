# DocVault — AI Context

# سياق الذكاء الاصطناعي — خزنة المستندات

## What is DocVault?

DocVault is an enterprise document management and compliance system for Frappe/ERPNext. It provides document versioning, classification, workflow-based approvals, retention policy enforcement, full-text search, and collaboration with a self-service portal.

## Architecture

- **24 DocTypes** across 9 modules
- **5 Services**: document, search, compliance, retention, analytics
- **8 Roles**: DV Admin, DV Manager, DV Editor, DV Viewer, DV Compliance Officer, DV Auditor, DV Portal User, DV Reviewer
- **20 CAPS Capabilities**: DV_manage_settings through DV_manage_portal

## Key DocTypes

- `DV Settings` — Global configuration
- `DV Document` — Core document record with file and metadata
- `DV Version` — Document version history
- `DV Category` — Classification taxonomy
- `DV Folder` — Hierarchical folder structure
- `DV Retention Policy` — Legal retention rules
- `DV Audit Log` — Append-only access and modification log
- `DV Controlled Document` — Compliance-reviewed documents
- `DV Checkout` — Exclusive editing locks

## Dependencies

`frappe`, `frappe_visual`, `arkan_help`, `base_base`

## Tech Stack

Python 3.14+ | Frappe v16 | MariaDB 11.8+ | Node.js v24+
