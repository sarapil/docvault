# DV Admin — Usage Scenarios
# سيناريوهات استخدام — مدير النظام

## Role Overview

- **Title**: DocVault Administrator / مدير DocVault
- **CAPS Capabilities**: DV_manage_settings, DV_manage_categories, DV_manage_folders, DV_manage_workflows, DV_manage_retention
- **Primary DocTypes**: DV Settings, DV Category, DV Folder, DV Workflow Template, DV Retention Policy
- **Device**: Desktop

## Daily Scenarios (يومي)

### DS-001: Create Category Structure
- **Goal**: Set up document classification hierarchy
- **Steps**:
  1. Navigate to Classification workspace → DV Category → New
  2. Set category_name, parent_category (if child), retention days
  3. Repeat for subcategories
  4. Verify: Category tree displays correctly

### DS-002: Configure Folder Structure
- **Goal**: Organize document storage folders
- **Steps**:
  1. Navigate to DV Core → DV Folder → New
  2. Set folder_name, parent_folder, access roles
  3. Verify: Folder hierarchy is navigable

## Weekly Scenarios (أسبوعي)

### WS-001: Define Retention Policy
- **Goal**: Set document retention rules for compliance
- **Steps**:
  1. Navigate to DV Compliance → DV Retention Policy → New
  2. Set policy name, retention days, action (archive/delete)
  3. Link to categories
  4. Enable retention schedule
