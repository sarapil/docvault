// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// DocVault — frappe_visual Integration
frappe.provide("docvault.visual");

docvault.visual.init = function () {
    if (!frappe.visual) return;
    if (frappe.visual.themeManager) {
        frappe.visual.themeManager.registerApp("docvault", {
            label: __("DocVault"),
            color: "#059669",
            icon: "file-text",
        });
    }
};

if (frappe.visual) {
    docvault.visual.init();
} else {
    $(document).on("frappe_visual_ready", docvault.visual.init);
}
