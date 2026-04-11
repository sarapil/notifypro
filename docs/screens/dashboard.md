# NotifyPro Dashboard — Screen Spec

# لوحة تحكم NotifyPro

## Overview

Primary workspace dashboard showing channel health, delivery metrics, and recent activity.

## Scenarios Served

- Admin DS-001: Monitor Channel Health
- Manager MS-001: Review Analytics
- Operator DS-002: Clear Notification Queue

## frappe_visual Components

- `frappe.visual.scenePresetOffice` — Animated workspace header with KPI frames
- `frappe.visual.heatmap` — Delivery heatmap by hour/day
- `frappe.visual.donut` — Channel distribution chart
- `frappe.visual.sparkline` — Delivery trend per channel

## CSS Effects (3+)

- `.fv-fx-glass` — Dashboard card backgrounds
- `.fv-fx-hover-lift` — Card hover interaction
- `.fv-fx-page-enter` — Page entrance animation

## Responsive Breakpoints

| Breakpoint | Layout              |
| ---------- | ------------------- |
| >= 1280px  | 3-column grid       |
| 768-1279px | 2-column grid       |
| < 768px    | Single column stack |

## RTL Support

CSS Logical Properties used throughout. All labels wrapped in `__()`.

## Dark Mode

Uses CSS variables only — no hardcoded colors.
