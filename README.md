<div align="center">

# 📣 NotifyPro

**Unified Notification Center for Frappe**

[![CI](https://github.com/sarapil/notifypro/actions/workflows/ci.yml/badge.svg)](https://github.com/sarapil/notifypro/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Overview

NotifyPro is a multi-channel notification engine for Frappe v16. It centralizes Email, SMS, WhatsApp, Telegram, and Push notifications into a single platform with template management, campaign scheduling, audience targeting, delivery analytics, and user preference controls.

## Features

- **Multi-Channel Delivery** — Email, SMS, WhatsApp, Telegram, Push with pluggable provider architecture
- **Template Engine** — Variable substitution, multi-language templates, channel-specific formatting
- **Campaign Scheduler** — Schedule campaigns with audience filters, A/B testing support
- **Smart Routing** — Priority-based routing with automatic fallback channels
- **User Preferences** — Per-user channel preferences, opt-out management, quiet hours
- **Analytics Dashboard** — Delivery rates, open rates, click tracking per channel
- **Notification Hooks** — Trigger notifications from any DocType event via hooks
- **CAPS Integration** — 15 fine-grained capabilities for permission control
- **Bilingual** — Full Arabic + English support with RTL-ready UI

## Architecture

- **30 DocTypes** across 10 modules
- **6 Channel Providers** with abstract base class
- **5 Roles**: NP Admin, NP Manager, NP Operator, NP Viewer, NP API User
- **Services Layer**: notification, template, campaign, routing, channel, analytics

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/sarapil/notifypro --branch main
bench --site your-site install-app notifypro
bench --site your-site migrate
```

### Required Apps

- `frappe` >= 16.0.0
- `frappe_visual` >= 0.1.0
- `arkan_help` >= 0.0.1
- `base_base` >= 0.0.1

## Configuration

1. Navigate to **NP Settings** and configure default channels
2. Set up channel providers under **Channels** workspace
3. Create notification templates under **Templates**
4. Configure routing rules under **Routing**

## Reports

| Report | Module | Description |
|--------|--------|-------------|
| Notification Analytics | Analytics | Delivery rates by channel with bar chart |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. This app uses `pre-commit` for code quality:

```bash
cd apps/notifypro
pre-commit install
```

Tools: ruff, eslint, prettier, pyupgrade

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT — See [license.txt](license.txt)
