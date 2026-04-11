/* docvault — Combined JS (reduces HTTP requests) */
/* Auto-generated from 2 individual files */


/* === docvault_boot.js === */
// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// DocVault — Global Bootstrap
(function() {
"use strict";
// Guard: skip if frappe core not loaded (transient HTTP/2 proxy failures)
if (typeof frappe === "undefined" || typeof frappe.provide !== "function") return;
frappe.provide("docvault");

docvault.COLORS = {
    primary: "#059669",
    secondary: "#6EE7B7",
    success: "#10B981",
    warning: "#F59E0B",
    danger: "#EF4444",
};

// Real-time document events
frappe.realtime.on("dv_document_updated", (data) => {
    if (data && data.document) {
        frappe.show_alert({
            message: __("Document {0} has been updated", [data.title || data.document]),
            indicator: "green",
        });
    }
});

frappe.realtime.on("dv_review_assigned", (data) => {
    if (data && data.document) {
        frappe.show_alert({
            message: __("Review assigned for {0}", [data.title || data.document]),
            indicator: "blue",
        });
    }
});
})();


/* === fv_integration.js === */
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

