# NotifyPro — AI Context

# سياق الذكاء الاصطناعي — نوتيفاي برو

## What is NotifyPro?

NotifyPro is a multi-channel notification management system for Frappe/ERPNext. It provides centralized control over Email, SMS, WhatsApp, Telegram, and Push notifications with template management, routing rules, campaigns, and analytics.

## Architecture

- **30 DocTypes** across 10 modules
- **6 Services**: notification, template, routing, campaign, analytics, preference
- **6 Channel Providers**: email, sms, whatsapp, telegram, push, base
- **5 Roles**: NP Admin, NP Manager, NP Operator, NP Viewer, NP Template Designer
- **15 CAPS Capabilities**: NP_manage_settings through NP_manage_integrations

## Key DocTypes

- `NP Settings` — Global app configuration
- `NP Channel` — Channel definitions (Email/SMS/WhatsApp/Telegram/Push)
- `NP Template` — Notification templates with Jinja2
- `NP Notification Log` — Delivery tracking and status
- `NP Campaign` — Bulk notification campaigns
- `NP Routing Rule` — Smart routing logic
- `NP Preference` — Per-user notification preferences

## Dependencies

`frappe`, `frappe_visual`, `arkan_help`, `base_base`

## Tech Stack

Python 3.14+ | Frappe v16 | MariaDB 11.8+ | Node.js v24+
