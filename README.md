<div align="center">

# 🔒 DocVault

**Enterprise Document Management System for Frappe**

[![CI](https://github.com/sarapil/docvault/actions/workflows/ci.yml/badge.svg)](https://github.com/sarapil/docvault/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Overview

DocVault is a full-featured document management system for Frappe v16. It provides document versioning, check-in/check-out, hierarchical classification, compliance-grade retention policies, full-text search with OCR, and collaboration tools — all within the Frappe desk.

## Features

- **Document Versioning** — Full version history with change notes and rollback
- **Check-In/Check-Out** — Exclusive editing locks with checkout tracking
- **Classification** — Hierarchical categories, folders, and tag-based organization
- **Compliance Framework** — Retention policies, controlled documents, audit trails
- **Full-Text Search** — Title and content search with OCR indexing support
- **Workflow Engine** — Document review and approval workflows
- **Collaboration** — Comments, sharing, and team document workspaces
- **Portal Access** — External users can view/download shared documents
- **CAPS Integration** — 20 fine-grained capabilities for permission control
- **Bilingual** — Full Arabic + English support with RTL-ready UI

## Architecture

- **24 DocTypes** across 9 modules
- **5 Services**: document, search, compliance, retention, analytics
- **8 Roles**: DV Admin, DV Manager, DV Editor, DV Viewer, DV Compliance Officer, DV Auditor, DV Portal User, DV API User

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/sarapil/docvault --branch main
bench --site your-site install-app docvault
bench --site your-site migrate
```

### Required Apps

- `frappe` >= 16.0.0
- `frappe_visual` >= 0.1.0
- `arkan_help` >= 0.0.1
- `base_base` >= 0.0.1

## Configuration

1. Navigate to **DV Settings** and configure storage and retention defaults
2. Set up categories under **Classification** workspace
3. Create folder structure under **DV Core**
4. Define compliance policies under **DV Compliance**

## Reports

| Report            | Module        | Description                                  |
| ----------------- | ------------- | -------------------------------------------- |
| Document Activity | DV Compliance | Document activity by status with donut chart |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. This app uses `pre-commit` for code quality:

```bash
cd apps/docvault
pre-commit install
```

Tools: ruff, eslint, prettier, pyupgrade

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT — See [license.txt](license.txt)

## Contact

For support and inquiries:
- Phone: +201508268982
- WhatsApp: https://wa.me/201508268982

