# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

app_name = "notifypro"
app_title = "NotifyPro"
app_publisher = "Arkan Lab"
app_description = "Unified Notification Center for Frappe"
app_email = "dev@arkan.it.com"
app_license = "mit"
app_icon = "/assets/notifypro/images/notifypro_icon.svg"
app_color = "#7C3AED"
app_logo_url = "/assets/notifypro/images/notifypro-logo.svg"

# Required Apps
required_apps = ["frappe", "frappe_visual", "arkan_help", "base_base"]

# Feature Registry (Open Core)
app_feature_registry = {
    "email_notifications": "free",
    "in_app_notifications": "free",
    "basic_templates": "free",
    "whatsapp_channel": "premium",
    "telegram_channel": "premium",
    "sms_channel": "premium",
    "push_notifications": "premium",
    "smart_routing": "premium",
    "campaigns": "premium",
    "analytics_dashboard": "premium",
    "hook_triggers": "premium",
    "ai_send_time": "premium",
    "ai_template_suggestions": "premium",
    "bulk_sending": "premium",
    "api_access": "premium",
}

# Apps Screen
add_to_apps_screen = [
    {
        "name": "notifypro",
        "logo": "/assets/notifypro/images/notifypro_icon.svg",
        "title": "NotifyPro",
        "route": "/app/notifypro",
        "has_permission": "notifypro.api.permissions.has_app_permission",
    }
]

# Includes in <head>
# CODESPACES: app_include_css = ["/assets/notifypro/css/notifypro_combined.css"]
# CODESPACES: app_include_js = ["/assets/notifypro/js/notifypro_combined.js"]

# Installation
before_install = "notifypro.install.before_install"
after_install = "notifypro.install.after_install"
after_migrate = ["notifypro.seed.seed_data"]
before_uninstall = "notifypro.install.before_uninstall"

# Boot Session
boot_session = "notifypro.boot.boot_session"

# Scheduled Tasks
scheduler_events = {
    "cron": {
        "* * * * *": [
            "notifypro.services.queue_service.process_queue",
        ],
    },
    "daily": [
        "notifypro.services.analytics_service.generate_daily_summary",
    ],
    "hourly": [
        "notifypro.services.queue_service.retry_failed_messages",
        "notifypro.services.channel_service.check_channel_health",
    ],
    "weekly": [
        "notifypro.services.analytics_service.generate_weekly_report",
    ],
}

# Document Events
doc_events = {
    "*": {
        "after_insert": "notifypro.events.hook_events.on_doc_event",
        "on_update": "notifypro.events.hook_events.on_doc_event",
        "on_submit": "notifypro.events.hook_events.on_doc_event",
        "on_cancel": "notifypro.events.hook_events.on_doc_event",
    },
}

# Fixtures
fixtures = [
    {"dt": "Role", "filters": [["name", "like", "NP%"]]},
    {"dt": "Workspace", "filters": [["module", "like", "Notifypro%"]]},
    {"dt": "Desktop Icon", "filters": [["app", "=", "notifypro"]]},
]

# Website Route Rules
website_route_rules = [
    {"from_route": "/notifypro-about", "to_route": "notifypro_about"},
    {"from_route": "/notifypro-onboarding", "to_route": "notifypro_onboarding"},
]

# Global Search
global_search_doctypes = {
    "Default": [
        {"doctype": "NP Message", "index": 1},
        {"doctype": "NP Template", "index": 2},
        {"doctype": "NP Campaign", "index": 3},
        {"doctype": "NP Channel", "index": 4},
    ]
}

export_python_type_annotations = True

# CAPS Integration
caps_capabilities = [
    {"name": "NP_manage_channels", "category": "Module", "description": "إدارة القنوات"},
    {"name": "NP_create_campaigns", "category": "Action", "description": "إنشاء حملات"},
    {"name": "NP_send_bulk", "category": "Action", "description": "إرسال جماعي"},
    {"name": "NP_view_analytics", "category": "Report", "description": "عرض التحليلات"},
    {"name": "NP_manage_templates", "category": "Action", "description": "إدارة القوالب"},
    {"name": "NP_view_costs", "category": "Field", "description": "عرض التكاليف"},
    {"name": "NP_manage_preferences", "category": "Module", "description": "إدارة التفضيلات"},
    {"name": "NP_manage_hooks", "category": "Module", "description": "إدارة المشغلات"},
    {"name": "NP_export_data", "category": "Report", "description": "تصدير البيانات"},
    {"name": "NP_manage_rate_limits", "category": "Module", "description": "حدود الإرسال"},
    {"name": "NP_view_delivery_logs", "category": "Report", "description": "سجلات التسليم"},
    {"name": "NP_manage_segments", "category": "Action", "description": "إدارة الشرائح"},
    {"name": "NP_configure_webhooks", "category": "Module", "description": "إعداد ويب هوك"},
    {"name": "NP_api_access", "category": "Module", "description": "وصول API"},
    {"name": "NP_manage_optouts", "category": "Action", "description": "إدارة إلغاء الاشتراك"},
]

caps_field_maps = [
    {"capability": "NP_view_costs", "doctype": "NP Cost Record", "field": "cost_amount", "behavior": "mask"},
    {"capability": "NP_view_costs", "doctype": "NP Channel Provider", "field": "cost_per_message", "behavior": "mask"},
]
