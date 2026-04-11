/* notifypro — Combined JS (reduces HTTP requests) */
/* Auto-generated from 2 individual files */


/* === notifypro_boot.js === */
// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// NotifyPro — Global Bootstrap
// Guard: skip if frappe core not loaded (transient HTTP/2 proxy failures)
if (typeof frappe === "undefined" || typeof frappe.provide !== "function") { return; }
frappe.provide("notifypro");

notifypro.COLORS = {
    primary: "#7C3AED",
    secondary: "#A78BFA",
    success: "#10B981",
    warning: "#F59E0B",
    danger: "#EF4444",
};

// Boot: inject notification badge count
$(document).ready(function () {
    if (frappe.boot.notifypro_unread_count) {
        notifypro.updateBadge(frappe.boot.notifypro_unread_count);
    }
});

notifypro.updateBadge = function (count) {
    // Update navbar notification badge
    let badge = $(".notifypro-badge");
    if (!badge.length) {
        badge = $(`<span class="notifypro-badge badge badge-danger" style="display:none;position:absolute;top:2px;right:2px;font-size:10px;"></span>`);
        $(".navbar .notifications-icon").parent().css("position", "relative").append(badge);
    }
    if (count > 0) {
        badge.text(count > 99 ? "99+" : count).show();
    } else {
        badge.hide();
    }
};

// Real-time listener for new notifications
frappe.realtime.on("np_notification", (data) => {
    if (data && data.unread_count !== undefined) {
        notifypro.updateBadge(data.unread_count);
    }
    if (data && data.message) {
        frappe.show_alert({
            message: data.message,
            indicator: data.indicator || "blue",
        });
    }
});


/* === fv_integration.js === */
// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for NotifyPro

(function() {
    "use strict";

    const APP_CONFIG = {
        name: "notifypro",
        title: "NotifyPro",
        color: "#7C3AED",
        module: "NotifyPro",
    };

    $(document).on("app_ready", function() {
        if (frappe.visual && frappe.visual.ThemeManager) {
            try {
                frappe.visual.ThemeManager.registerApp(APP_CONFIG);
            } catch(e) {
                // frappe_visual not yet loaded
            }
        }
    });
})();

