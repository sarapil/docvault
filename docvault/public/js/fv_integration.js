// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for DocVault

(function() {
    "use strict";

    const APP_CONFIG = {
        name: "docvault",
        title: "DocVault",
        color: "#059669",
        module: "DocVault",
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
