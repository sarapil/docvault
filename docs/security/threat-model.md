# DocVault — Threat Model
# نموذج التهديدات — خزنة المستندات

## Overview

DocVault manages sensitive organizational documents. This threat model follows OWASP guidelines.

## Assets

| Asset | Sensitivity | Storage |
|-------|-------------|---------|
| Documents (files) | High | File system / S3 |
| Document metadata | Medium | MariaDB |
| Audit logs | High | MariaDB |
| User sessions | High | Redis |
| Classification labels | Medium | MariaDB |

## Threat Categories

### T1: Unauthorized Document Access
- **Risk**: High
- **Vector**: Bypassing CAPS permission checks
- **Mitigation**: All API endpoints check `frappe.has_permission()` first; CAPS field-level masking for classified documents; DV Audit Log records every access

### T2: Document Tampering
- **Risk**: High
- **Vector**: Direct database modification or file replacement
- **Mitigation**: Version history with checksums; check-out/check-in locking; audit trail of all modifications

### T3: Audit Log Manipulation
- **Risk**: Critical
- **Vector**: Admin deleting or modifying audit entries
- **Mitigation**: DV Audit Log is append-only (no update/delete permissions); separate CAPS capability for audit access

### T4: File Upload Attacks
- **Risk**: Medium
- **Vector**: Malicious files (executables, scripts) uploaded as documents
- **Mitigation**: File type validation; extension allowlist; content-type verification; size limits

### T5: Portal Access Escalation
- **Risk**: Medium
- **Vector**: External portal users accessing internal documents
- **Mitigation**: DV Portal module with separate permission model; portal users cannot access desk routes

### T6: Retention Policy Bypass
- **Risk**: Medium
- **Vector**: Users retaining documents beyond legal retention period
- **Mitigation**: Automated retention schedule enforcement; compliance officer approval for extensions

### T7: Information Disclosure via Search
- **Risk**: Medium
- **Vector**: Search results exposing document titles/metadata user shouldn't see
- **Mitigation**: Search results filtered through permission checks; CAPS field masking applied to search results

## Security Controls

| Control | Implementation |
|---------|---------------|
| Authentication | Frappe session (cookie-based) |
| Authorization | CAPS capabilities + Frappe permissions |
| Audit | DV Audit Log (append-only) |
| Encryption | HTTPS in transit; at-rest per infrastructure |
| Input validation | `validators.py` for all API inputs |
| Rate limiting | `frappe.rate_limiter` on public APIs |
