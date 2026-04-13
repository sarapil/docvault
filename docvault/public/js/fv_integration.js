// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for DocVault — Scene Dashboard & Visual Components

(function() {
    "use strict";

    // ── App Configuration ─────────────────────────────────────────
    const APP_CONFIG = {
        name: "docvault",
        title: "DocVault",
        color: "#059669",
        gradient: "linear-gradient(135deg, #059669, #047857)",
        module: "DocVault",
    };

    // ── CSS Variables Registration ────────────────────────────────
    function registerCSSVariables() {
        document.documentElement.style.setProperty("--docvault-primary", APP_CONFIG.color);
        document.documentElement.style.setProperty("--docvault-gradient", APP_CONFIG.gradient);
    }

    // ── Scene Dashboard Builder ───────────────────────────────────
    async function buildSceneDashboard(container) {
        if (!frappe.visual) {
            console.warn("[DocVault] frappe_visual not available for scene dashboard");
            return null;
        }

        try {
            let sceneContainer = container.querySelector('#docvault-scene-header');
            if (!sceneContainer) {
                sceneContainer = document.createElement('div');
                sceneContainer.id = 'docvault-scene-header';
                sceneContainer.className = 'docvault-scene-container fv-fx-glass';
                container.insertBefore(sceneContainer, container.firstChild);
            }

            const scene = await frappe.visual.scenePresetLibrary({
                container: '#docvault-scene-header',
                theme: 'cool',
                frames: [
                    { label: __('Total Documents'), status: 'success' },
                    { label: __('Pending Approval'), status: 'warning' },
                    { label: __('Checked Out'), status: 'info' },
                    { label: __('Due for Review'), status: 'danger' }
                ],
                documents: [{ label: __('Recent Documents'), href: '/app/dv-document', color: '#059669' }],
                books: [{ label: __('DocVault Help'), href: '/docvault-onboarding', color: '#059669' }]
            });

            if (frappe.visual.sceneDataBinder) {
                await frappe.visual.sceneDataBinder({
                    engine: scene,
                    frames: [
                        { label: __('Total Documents'), doctype: 'DV Document', aggregate: 'count', status_rules: { '>1000': 'success', '<100': 'warning' } },
                        { label: __('Pending Approval'), doctype: 'DV Document', aggregate: 'count', filters: { status: 'Pending Approval' }, status_rules: { '>10': 'warning', '>50': 'danger' } },
                        { label: __('Checked Out'), doctype: 'DV Document', aggregate: 'count', filters: { is_checked_out: 1 }, status_rules: { '>0': 'info' } },
                        { label: __('Due for Review'), doctype: 'DV Document', aggregate: 'count', filters: { review_due: ['<', 'today()'] }, status_rules: { '>0': 'danger' } }
                    ],
                    refreshInterval: 60000
                });
            }
            return scene;
        } catch (e) {
            console.error("[DocVault] Scene dashboard error:", e);
            return null;
        }
    }

    // ── KPI Cards Builder (Fallback) ──────────────────────────────
    async function buildKPICards(container) {
        const kpiContainer = document.createElement('div');
        kpiContainer.className = 'docvault-kpi-grid';
        kpiContainer.innerHTML = `
            <div class="docvault-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="documents">
                <div class="docvault-kpi-icon">📄</div>
                <div class="docvault-kpi-value" data-field="documents_count">--</div>
                <div class="docvault-kpi-label">${__('Total Documents')}</div>
            </div>
            <div class="docvault-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="pending">
                <div class="docvault-kpi-icon">⏳</div>
                <div class="docvault-kpi-value" data-field="pending_count">--</div>
                <div class="docvault-kpi-label">${__('Pending Approval')}</div>
            </div>
            <div class="docvault-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="storage">
                <div class="docvault-kpi-icon">💾</div>
                <div class="docvault-kpi-value" data-field="storage_used">--</div>
                <div class="docvault-kpi-label">${__('Storage Used')}</div>
            </div>
            <div class="docvault-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="versions">
                <div class="docvault-kpi-icon">📑</div>
                <div class="docvault-kpi-value" data-field="versions_count">--</div>
                <div class="docvault-kpi-label">${__('Total Versions')}</div>
            </div>
        `;
        container.insertBefore(kpiContainer, container.firstChild);

        try {
            const stats = await frappe.xcall('docvault.api.dashboard.get_dashboard_stats');
            if (stats) {
                animateNumber(kpiContainer.querySelector('[data-field="documents_count"]'), stats.documents_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="pending_count"]'), stats.pending_count || 0);
                kpiContainer.querySelector('[data-field="storage_used"]').textContent = stats.storage_used || '0 GB';
                animateNumber(kpiContainer.querySelector('[data-field="versions_count"]'), stats.versions_count || 0);
            }
        } catch (e) {
            console.warn("[DocVault] KPI fetch failed:", e);
        }
    }

    // ── Number Animation ──────────────────────────────────────────
    function animateNumber(element, targetValue) {
        if (!element) return;
        const duration = 1000, start = 0, startTime = performance.now();
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            element.textContent = Math.round(start + (targetValue - start) * eased).toLocaleString();
            if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
    }

    // ── Workspace Enhancement ─────────────────────────────────────
    async function enhanceWorkspace() {
        const workspaceMain = document.querySelector('.workspace-main');
        if (!workspaceMain) return;
        workspaceMain.classList.add('fv-fx-page-enter');
        if (frappe.visual && frappe.visual.scenePresetLibrary) {
            await buildSceneDashboard(workspaceMain);
        } else {
            await buildKPICards(workspaceMain);
        }
    }

    // ── Form Dashboard Enhancement ────────────────────────────────
    function enhanceFormDashboard(frm) {
        if (!frm || !frappe.visual) return;
        const dvDocTypes = ['DV Document', 'DV Folder', 'DV Category', 'DV Controlled Document', 'DV Workflow', 'DV Retention Policy'];
        if (!dvDocTypes.includes(frm.doctype)) return;
        if (frappe.visual.formDashboard) {
            const dashContainer = frm.page.main.find('.form-dashboard');
            if (dashContainer.length) {
                frappe.visual.formDashboard(dashContainer[0], { doctype: frm.doctype, docname: frm.doc.name });
            }
        }
    }

    // ── Initialize ────────────────────────────────────────────────
    $(document).on("app_ready", function() {
        registerCSSVariables();
        if (frappe.visual && frappe.visual.ThemeManager) {
            try { frappe.visual.ThemeManager.registerApp(APP_CONFIG); } catch(e) {}
        }
    });

    $(document).on("page-change", function() {
        const route = frappe.get_route_str();
        if (route.includes('docvault') || route.includes('DocVault')) setTimeout(enhanceWorkspace, 100);
        if (route === 'docvault-settings' && frappe.visual && frappe.visual.generator) {
            const page = frappe.container.page;
            if (page && page.main) frappe.visual.generator.settingsPage(page.main[0] || page.main, "DocVault Settings");
        }
        if (route === 'docvault-reports' && frappe.visual && frappe.visual.generator) {
            const page = frappe.container.page;
            if (page && page.main) frappe.visual.generator.reportsHub(page.main[0] || page.main, "DocVault");
        }
    });

    $(document).on("form-refresh", function(e, frm) { enhanceFormDashboard(frm); });

    frappe.docvault = frappe.docvault || {};
    frappe.docvault.visual = { buildSceneDashboard, buildKPICards, animateNumber };
})();
