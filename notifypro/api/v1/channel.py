# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from notifypro.api.response import success, error


@frappe.whitelist()
def get_channels():
    """Get all configured notification channels."""
    frappe.has_permission("NP Channel", "read", throw=True)
    channels = frappe.get_all("NP Channel",
        fields=["name", "channel_name", "channel_type", "enabled"],
        order_by="channel_type asc",
    )
    return success(data=channels)


@frappe.whitelist()
def check_health(channel_name=None):
    """Check health status of notification channels."""
    frappe.has_permission("NP Channel", "read", throw=True)
    from notifypro.services.channel_service import ChannelService
    try:
        if channel_name:
            result = ChannelService.check_single_channel_health(channel_name)
        else:
            result = ChannelService.check_channel_health()
        return success(data=result)
    except Exception as e:
        return error(str(e), error_code="NP_HEALTH_CHECK_FAILED")


@frappe.whitelist()
def get_analytics(channel=None, period="30d"):
    """Get notification analytics."""
    frappe.has_permission("NP Analytics Summary", "read", throw=True)
    from notifypro.services.analytics_service import AnalyticsService
    try:
        result = AnalyticsService.get_summary(channel=channel, period=period)
        return success(data=result)
    except Exception as e:
        return error(str(e), error_code="NP_ANALYTICS_FAILED")


@frappe.whitelist()
def get_user_preferences(user=None):
    """Get notification preferences for a user."""
    user = user or frappe.session.user
    if user != frappe.session.user:
        frappe.has_permission("NP User Preference", "read", throw=True)
    prefs = frappe.get_all("NP User Preference",
        filters={"user": user},
        fields=["name", "channel", "enabled", "quiet_hours_start", "quiet_hours_end"],
    )
    return success(data=prefs)


@frappe.whitelist()
def update_preference(channel, enabled=1, quiet_hours_start=None, quiet_hours_end=None):
    frappe.only_for(["NP User", "NP Manager", "System Manager"])
    """Update notification preference for current user."""
    user = frappe.session.user
    existing = frappe.db.get_value("NP User Preference",
        {"user": user, "channel": channel}, "name")

    if existing:
        doc = frappe.get_doc("NP User Preference", existing)
        doc.enabled = int(enabled)
        if quiet_hours_start is not None:
            doc.quiet_hours_start = quiet_hours_start
        if quiet_hours_end is not None:
            doc.quiet_hours_end = quiet_hours_end
        doc.save(ignore_permissions=True)
    else:
        doc = frappe.get_doc({
            "doctype": "NP User Preference",
            "user": user,
            "channel": channel,
            "enabled": int(enabled),
            "quiet_hours_start": quiet_hours_start,
            "quiet_hours_end": quiet_hours_end,
        }).insert(ignore_permissions=True)

    return success(data={"name": doc.name}, message="Preference updated")
