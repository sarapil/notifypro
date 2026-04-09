# NotifyPro — Dependency Graph
# مخطط التبعيات — NotifyPro

```mermaid
graph TD
    frappe["frappe v16"]
    frappe_visual["frappe_visual"]
    arkan_help["arkan_help"]
    base_base["base_base"]
    notifypro["📣 NotifyPro"]

    frappe --> frappe_visual
    frappe_visual --> arkan_help
    arkan_help --> base_base
    frappe_visual --> notifypro
    arkan_help --> notifypro
    base_base --> notifypro

    style notifypro fill:#7C3AED,color:#fff,stroke:#5B21B6
    style frappe fill:#0089FF,color:#fff
    style frappe_visual fill:#6366F1,color:#fff
    style arkan_help fill:#06B6D4,color:#fff
    style base_base fill:#64748B,color:#fff
```
