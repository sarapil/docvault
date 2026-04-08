// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// DocVault — Global Bootstrap
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
