// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// NotifyPro — frappe_visual Integration
frappe.provide("notifypro.visual");

notifypro.visual.init = function () {
    if (!frappe.visual) return;

    // Register app with ThemeManager
    if (frappe.visual.themeManager) {
        frappe.visual.themeManager.registerApp("notifypro", {
            label: __("NotifyPro"),
            color: "#7C3AED",
            icon: "bell",
        });
    }
};

// Auto-init when visual is loaded
if (frappe.visual) {
    notifypro.visual.init();
} else {
    $(document).on("frappe_visual_ready", notifypro.visual.init);
}
