# DocVault — Main Dashboard Screen

# لوحة التحكم الرئيسية — خزنة المستندات

## Screen Identity

- **Route**: `/desk/docvault`
- **Scenario IDs**: DS-001 (Admin, Manager, Editor, Compliance)
- **Primary Users**: All DocVault roles

## frappe_visual Components

| Component           | Purpose                          |
| ------------------- | -------------------------------- |
| `scenePresetOffice` | Workspace header with KPI frames |
| `DataCard`          | Document counts by status        |
| `Donut`             | Documents by category breakdown  |
| `Sparkline`         | Upload activity trend (7 days)   |
| `Area`              | Storage usage over time          |
| `KanbanBoard`       | Document workflow pipeline       |

## CSS Effects (minimum 3)

1. `.fv-fx-glass` — Dashboard card containers
2. `.fv-fx-hover-lift` — Category cards on hover
3. `.fv-fx-page-enter` — Entrance animation on load
4. `.fv-fx-gradient-text` — Dashboard title

## Layout

```
┌─────────────────────────────────────────────────┐
│  Scene Header (scenePresetOffice)               │
│  [Total Docs] [Pending Review] [Storage Used]   │
├─────────────────┬───────────────────────────────┤
│  Category Donut │  Upload Activity Sparkline    │
│                 │  Storage Area Chart           │
├─────────────────┴───────────────────────────────┤
│  Recent Documents (KanbanBoard by status)       │
│  [Draft] → [Under Review] → [Approved] → [Pub] │
└─────────────────────────────────────────────────┘
```

## Responsive Breakpoints

| Breakpoint          | Layout                           |
| ------------------- | -------------------------------- |
| Desktop (≥1024px)   | 2-column grid, full scene header |
| Tablet (768-1023px) | Single column, compact scene     |
| Mobile (320-767px)  | Stacked cards, no scene header   |

## Dark Mode

All colors via CSS variables — no hardcoded values.

## RTL Support

CSS Logical Properties: `margin-inline-start`, `padding-inline-end`.
