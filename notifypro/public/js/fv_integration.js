// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for NotifyPro

(function() {
    "use strict";

    const APP_CONFIG = {
        name: "notifypro",
        title: __("NotifyPro"),
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
