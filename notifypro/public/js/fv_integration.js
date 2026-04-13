// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for NotifyPro — Scene Dashboard & Visual Components

(function() {
    "use strict";

    // ── App Configuration ─────────────────────────────────────────
    const APP_CONFIG = {
        name: "notifypro",
        title: "NotifyPro",
        color: "#7C3AED",
        gradient: "linear-gradient(135deg, #7C3AED, #5B21B6)",
        module: "NotifyPro",
    };

    // ── CSS Variables Registration ────────────────────────────────
    function registerCSSVariables() {
        document.documentElement.style.setProperty("--notifypro-primary", APP_CONFIG.color);
        document.documentElement.style.setProperty("--notifypro-gradient", APP_CONFIG.gradient);
    }

    // ── Scene Dashboard Builder ───────────────────────────────────
    async function buildSceneDashboard(container) {
        if (!frappe.visual) {
            console.warn("[NotifyPro] frappe_visual not available for scene dashboard");
            return null;
        }

        try {
            let sceneContainer = container.querySelector('#notifypro-scene-header');
            if (!sceneContainer) {
                sceneContainer = document.createElement('div');
                sceneContainer.id = 'notifypro-scene-header';
                sceneContainer.className = 'notifypro-scene-container fv-fx-glass';
                container.insertBefore(sceneContainer, container.firstChild);
            }

            const scene = await frappe.visual.scenePresetOffice({
                container: '#notifypro-scene-header',
                theme: 'warm',
                frames: [
                    { label: __('Messages Sent'), status: 'success' },
                    { label: __('Delivery Rate'), status: 'success' },
                    { label: __('Active Campaigns'), status: 'info' },
                    { label: __('Pending Queue'), status: 'warning' }
                ],
                documents: [{ label: __('Recent Deliveries'), href: '/app/np-message', color: '#7C3AED' }],
                books: [{ label: __('NotifyPro Help'), href: '/notifypro-onboarding', color: '#7C3AED' }]
            });

            if (frappe.visual.sceneDataBinder) {
                await frappe.visual.sceneDataBinder({
                    engine: scene,
                    frames: [
                        { label: __('Messages Sent'), doctype: 'NP Message', aggregate: 'count', filters: { status: 'Sent' }, status_rules: { '>1000': 'success', '<100': 'warning' } },
                        { label: __('Delivery Rate'), method: 'notifypro.api.dashboard.get_delivery_rate', format: '%s%', status_rules: { '>90': 'success', '<70': 'danger' } },
                        { label: __('Active Campaigns'), doctype: 'NP Campaign', aggregate: 'count', filters: { status: 'Running' }, status_rules: { '>0': 'info' } },
                        { label: __('Pending Queue'), doctype: 'NP Message', aggregate: 'count', filters: { status: 'Queued' }, status_rules: { '>100': 'warning', '>500': 'danger' } }
                    ],
                    refreshInterval: 30000
                });
            }
            return scene;
        } catch (e) {
            console.error("[NotifyPro] Scene dashboard error:", e);
            return null;
        }
    }

    // ── KPI Cards Builder (Fallback) ──────────────────────────────
    async function buildKPICards(container) {
        const kpiContainer = document.createElement('div');
        kpiContainer.className = 'notifypro-kpi-grid';
        kpiContainer.innerHTML = `
            <div class="notifypro-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="sent">
                <div class="notifypro-kpi-icon">📧</div>
                <div class="notifypro-kpi-value" data-field="sent_count">--</div>
                <div class="notifypro-kpi-label">${__('Messages Sent')}</div>
            </div>
            <div class="notifypro-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="delivered">
                <div class="notifypro-kpi-icon">✅</div>
                <div class="notifypro-kpi-value" data-field="delivered_count">--</div>
                <div class="notifypro-kpi-label">${__('Delivered')}</div>
            </div>
            <div class="notifypro-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="campaigns">
                <div class="notifypro-kpi-icon">📢</div>
                <div class="notifypro-kpi-value" data-field="campaigns_count">--</div>
                <div class="notifypro-kpi-label">${__('Active Campaigns')}</div>
            </div>
            <div class="notifypro-kpi-card fv-fx-glass fv-fx-hover-lift" data-stat="channels">
                <div class="notifypro-kpi-icon">📡</div>
                <div class="notifypro-kpi-value" data-field="channels_count">--</div>
                <div class="notifypro-kpi-label">${__('Active Channels')}</div>
            </div>
        `;
        container.insertBefore(kpiContainer, container.firstChild);

        try {
            const stats = await frappe.xcall('notifypro.api.dashboard.get_dashboard_stats');
            if (stats) {
                animateNumber(kpiContainer.querySelector('[data-field="sent_count"]'), stats.sent_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="delivered_count"]'), stats.delivered_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="campaigns_count"]'), stats.campaigns_count || 0);
                animateNumber(kpiContainer.querySelector('[data-field="channels_count"]'), stats.channels_count || 0);
            }
        } catch (e) {
            console.warn("[NotifyPro] KPI fetch failed:", e);
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
        if (frappe.visual && frappe.visual.scenePresetOffice) {
            await buildSceneDashboard(workspaceMain);
        } else {
            await buildKPICards(workspaceMain);
        }
    }

    // ── Form Dashboard Enhancement ────────────────────────────────
    function enhanceFormDashboard(frm) {
        if (!frm || !frappe.visual) return;
        const npDocTypes = ['NP Message', 'NP Template', 'NP Campaign', 'NP Channel', 'NP Hook', 'NP Segment'];
        if (!npDocTypes.includes(frm.doctype)) return;
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
        if (route.includes('notifypro') || route.includes('NotifyPro')) setTimeout(enhanceWorkspace, 100);
        if (route === 'notifypro-settings' && frappe.visual && frappe.visual.generator) {
            const page = frappe.container.page;
            if (page && page.main) frappe.visual.generator.settingsPage(page.main[0] || page.main, "NotifyPro Settings");
        }
        if (route === 'notifypro-reports' && frappe.visual && frappe.visual.generator) {
            const page = frappe.container.page;
            if (page && page.main) frappe.visual.generator.reportsHub(page.main[0] || page.main, "NotifyPro");
        }
    });

    $(document).on("form-refresh", function(e, frm) { enhanceFormDashboard(frm); });

    frappe.notifypro = frappe.notifypro || {};
    frappe.notifypro.visual = { buildSceneDashboard, buildKPICards, animateNumber };
})();
