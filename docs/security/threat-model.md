# NotifyPro — Threat Model

## Overview

Security analysis for NotifyPro notification delivery system.

## Assets

| Asset | Sensitivity | Description |
|-------|------------|-------------|
| NP Channel credentials | HIGH | API keys for SMS, WhatsApp, Telegram providers |
| Notification content | MEDIUM | Message bodies may contain PII |
| Recipient data | MEDIUM | Email addresses, phone numbers |
| Delivery logs | LOW | Operational data |

## Threats (OWASP-aligned)

### T1: Credential Exposure
- **Risk**: Channel provider API keys stored insecurely
- **Mitigation**: Credentials stored via `frappe.conf` or encrypted Password fields, never in plain text
- **Status**: Mitigated

### T2: Injection via Template Variables
- **Risk**: Template variable substitution could inject HTML/script
- **Mitigation**: All template output sanitized via `frappe.utils.sanitize_html()`
- **Status**: Mitigated

### T3: Unauthorized Bulk Send
- **Risk**: Unauthorized user triggers mass notifications
- **Mitigation**: CAPS capability `NP_bulk_send` required, rate limiting on APIs
- **Status**: Mitigated

### T4: Notification Spoofing
- **Risk**: Attacker sends notifications impersonating the system
- **Mitigation**: All sends routed through authenticated channel providers
- **Status**: Mitigated

## Audit Logging

- All notification sends logged in NP Notification Log with user, timestamp, channel
- Failed deliveries logged with error details
- Campaign results tracked per recipient
