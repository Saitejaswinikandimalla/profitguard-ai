"""
render_tvora_mvp.py
Renders a pixel-perfect, high-resolution mockup of the ProfitGuard Order Intelligence UI
styled after Tvora & SalesPro SaaS dashboards.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = r"C:\Users\tejas\.gemini\antigravity\scratch\profitguard_work\screenshots"
os.makedirs(IMG_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=200)
fig.patch.set_facecolor('#0f1422')
ax.set_facecolor('#0f1422')
ax.axis('off')

# Left Sidebar
sidebar = patches.Rectangle((0, 0), 0.18, 1.0, facecolor='#141b2d', edgecolor='#263353', lw=1)
ax.add_patch(sidebar)

# Brand
ax.text(0.02, 0.93, "🛡️", fontsize=16)
ax.text(0.045, 0.94, "ProfitGuard AI", color='#ffffff', fontsize=12, fontweight='bold')
ax.text(0.045, 0.915, "ANALYTICS & PROFIT", color='#38bdf8', fontsize=7, fontweight='bold')

# Nav Items
nav_items = [
    ("📦 Order Intelligence", True),
    ("📊 Sales & Margins", False),
    ("🧠 Customer RFM (ML)", False),
    ("📦 Inventory Warnings", False),
    ("📑 Data Profiling", False)
]
for i, (item, active) in enumerate(nav_items):
    y = 0.82 - i * 0.065
    if active:
        btn = patches.FancyBboxPatch((0.015, y - 0.015), 0.15, 0.045, boxstyle="round,pad=0.01",
                                     fc='#0284c7', ec='none')
        ax.add_patch(btn)
        ax.text(0.025, y, item, color='#ffffff', fontsize=8.5, fontweight='bold')
    else:
        ax.text(0.025, y, item, color='#94a3b8', fontsize=8.5, fontweight='bold')

# Sidebar Bottom Badge
badge_bg = patches.FancyBboxPatch((0.015, 0.04), 0.15, 0.10, boxstyle="round,pad=0.01",
                                  fc='#1a2238', ec='#263353', lw=1)
ax.add_patch(badge_bg)
ax.text(0.025, 0.11, "DATATHON 2026", color='#ffffff', fontsize=7.5, fontweight='bold')
ax.text(0.025, 0.08, "Track 4: The Money Leak", color='#38bdf8', fontsize=6.8)
ax.text(0.025, 0.055, "From-Scratch NumPy ML", color='#94a3b8', fontsize=6.8)

# Top Bar
ax.text(0.21, 0.94, "Order Intelligence", color='#ffffff', fontsize=15, fontweight='bold')
ax.text(0.21, 0.915, "Smart transaction management with profit estimates & revenue leakage tracking.", color='#94a3b8', fontsize=8.5)

# Date & Action pills
d_pill = patches.FancyBboxPatch((0.76, 0.92), 0.12, 0.035, boxstyle="round,pad=0.008",
                                fc='#1a2238', ec='#263353', lw=1)
ax.add_patch(d_pill)
ax.text(0.82, 0.935, "📅 All 18,000 Records", color='#f8fafc', fontsize=7.5, ha='center', fontweight='bold')

q_btn = patches.FancyBboxPatch((0.89, 0.92), 0.08, 0.035, boxstyle="round,pad=0.008",
                               fc='#0284c7', ec='none')
ax.add_patch(q_btn)
ax.text(0.93, 0.935, "🔍 Quick Audit", color='#ffffff', fontsize=7.5, ha='center', fontweight='bold')

# Metric Strip (Tvora Style)
strip = patches.FancyBboxPatch((0.21, 0.77), 0.76, 0.11, boxstyle="round,pad=0.01",
                               fc='#1a2238', ec='#263353', lw=1)
ax.add_patch(strip)

metrics = [
    ("Completed Orders", "13,962", "↑ 77.6% Completed", '#10b981'),
    ("Loss-Making Leaks", "5,315", "↑ 38.1% of Sales", '#ef4444'),
    ("High-Profit Orders", "8,647", "↑ 61.9% Profitable", '#10b981'),
    ("Gross Revenue", "₹73.02L", "₹7,301,698 Topline", '#0ea5e9'),
    ("Estimated Leakage", "-₹12.14L", "-16.6% Bottom Line", '#ef4444'),
    ("Returns Flagged", "1,431", "8.0% Return Rate", '#f59e0b'),
    ("Cancelled Orders", "1,689", "9.4% Churn", '#94a3b8')
]
for i, (label, val, sub, col) in enumerate(metrics):
    x = 0.22 + i * 0.108
    ax.text(x, 0.85, label, color='#94a3b8', fontsize=6.5, fontweight='bold')
    ax.text(x, 0.81, val, color=col, fontsize=11, fontweight='bold')
    ax.text(x, 0.785, sub, color=col, fontsize=6.2)
    if i < 6:
        ax.plot([x + 0.10, x + 0.10], [0.78, 0.86], color='#263353', lw=1)

# Filter Tabs (Tvora Style)
tabs = [("All Orders (18,000)", False), ("Loss Making (5,315)", True), ("High Profit (8,647)", False),
        ("Catalog Mispricing (4,770)", False), ("Promo Leakage (545)", False), ("Returns (1,431)", False)]
for i, (tab_name, active) in enumerate(tabs):
    x = 0.21 + i * 0.125
    if active:
        tab_bg = patches.FancyBboxPatch((x, 0.71), 0.115, 0.035, boxstyle="round,pad=0.006",
                                        fc='#0284c7', ec='none')
        ax.add_patch(tab_bg)
        ax.text(x + 0.0575, 0.725, tab_name, color='#ffffff', fontsize=7.5, ha='center', fontweight='bold')
    else:
        ax.text(x + 0.0575, 0.725, tab_name, color='#94a3b8', fontsize=7.5, ha='center', fontweight='bold')

# Order Table Card
table_bg = patches.FancyBboxPatch((0.21, 0.19), 0.76, 0.49, boxstyle="round,pad=0.01",
                                  fc='#1a2238', ec='#263353', lw=1)
ax.add_patch(table_bg)

ax.text(0.23, 0.65, "Recent Suspicious Transactions & Profit Estimates", color='#ffffff', fontsize=10.5, fontweight='bold')
ax.text(0.95, 0.65, "Click row to view mathematical proof", color='#94a3b8', fontsize=7.5, ha='right')

# Table Header
headers = [("Order ID", 0.23), ("Date", 0.31), ("Customer", 0.39), ("Product", 0.46), ("Category", 0.52),
           ("Order Value", 0.60), ("Cost", 0.67), ("Profit Estimate", 0.74), ("Risk Score", 0.84), ("Tags", 0.91)]
for h, hx in headers:
    ax.text(hx, 0.61, h, color='#94a3b8', fontsize=7.5, fontweight='bold')

ax.plot([0.22, 0.96], [0.595, 0.595], color='#263353', lw=1)

# Sample Rows
rows = [
    ("TX015158", "2025-08-14", "CU00939", "PR0163", "Electronics", "₹199.85", "₹238.49", "Loss (-₹992.58)", "98/100", "Catalog Misprice", True),
    ("TX012734", "2025-06-22", "CU01046", "PR0037", "Beauty", "₹103.00", "₹218.49", "Loss (-₹989.45)", "97/100", "Catalog Misprice", True),
    ("TX005702", "2025-09-02", "CU02351", "PR0021", "Beauty", "₹206.30", "₹236.46", "Loss (-₹975.98)", "95/100", "Catalog Misprice", True),
    ("TX000001", "2025-08-22", "CU01588", "PR0103", "Sports", "₹1,230.80", "₹320.00", "Loss (-₹369.20)", "85/100", "Promo Leakage", True),
    ("TX000319", "2025-05-18", "CU01207", "PR0026", "Electronics", "₹611.88", "₹187.66", "Loss (-₹138.77)", "80/100", "Promo Leakage", True),
    ("TX000004", "2025-07-11", "CU00842", "PR0015", "Fashion", "₹1,850.00", "₹110.00", "Profit (+₹870.00)", "15/100", "Healthy", False),
    ("TX000007", "2025-09-29", "CU01923", "PR0088", "Home", "₹940.50", "₹85.00", "Profit (+₹420.50)", "12/100", "Healthy", False)
]

for idx, (oid, dt, cust, prod, cat, val, cost, p_est, risk, tag, is_loss) in enumerate(rows):
    y = 0.555 - idx * 0.05
    ax.text(0.23, y, oid, color='#ffffff', fontsize=7.8, fontweight='bold')
    ax.text(0.31, y, dt, color='#cbd5e1', fontsize=7.2)
    ax.text(0.39, y, cust, color='#cbd5e1', fontsize=7.2)
    ax.text(0.46, y, prod, color='#38bdf8', fontsize=7.2)
    ax.text(0.52, y, cat, color='#cbd5e1', fontsize=7.2)
    ax.text(0.60, y, val, color='#ffffff', fontsize=7.2, fontweight='bold')
    ax.text(0.67, y, cost, color='#94a3b8', fontsize=7.2)

    # Profit badge
    bg_col = '#450a0a' if is_loss else '#064e3b'
    txt_col = '#f87171' if is_loss else '#34d399'
    border_col = '#ef4444' if is_loss else '#10b981'
    p_box = patches.FancyBboxPatch((0.735, y - 0.012), 0.088, 0.026, boxstyle="round,pad=0.004",
                                   fc=bg_col, ec=border_col, lw=0.8)
    ax.add_patch(p_box)
    ax.text(0.779, y, p_est, color=txt_col, fontsize=6.8, ha='center', fontweight='bold')

    # Risk badge
    r_col = '#ef4444' if is_loss else '#10b981'
    ax.text(0.85, y, risk, color=r_col, fontsize=7.2, fontweight='bold')

    # Tag
    t_box = patches.FancyBboxPatch((0.905, y - 0.012), 0.052, 0.026, boxstyle="round,pad=0.004",
                                   fc='#1e293b', ec='#38bdf8', lw=0.8)
    ax.add_patch(t_box)
    ax.text(0.931, y, tag[:11], color='#38bdf8', fontsize=6.5, ha='center', fontweight='bold')

    ax.plot([0.22, 0.96], [y - 0.02, y - 0.02], color='#263353', lw=0.6)

# Bottom Diagnostic Audit Banner
banner = patches.FancyBboxPatch((0.21, 0.04), 0.76, 0.12, boxstyle="round,pad=0.01",
                                fc='#141b2d', ec='#38bdf8', lw=1.2)
ax.add_patch(banner)
ax.text(0.23, 0.12, "🔍 LIVE AUDIT BREAKDOWN: TRANSACTION TX000001 (PR0103)", color='#38bdf8', fontsize=9.2, fontweight='bold')
ax.text(0.23, 0.085, "Formula: Q × [P(1 - D) - C] = 5 × [₹307.70 × (1 - 0.20) - ₹320.00] = 5 × (-₹73.84) = -₹369.20 (NET LEAKAGE)", color='#f8fafc', fontsize=7.8, fontfamily='monospace')
ax.text(0.23, 0.055, "Root Cause: Uncontrolled Promotional Discounting  |  Action: Enforce checkout profit-floor barrier", color='#fca5a5', fontsize=7.5, fontweight='bold')

out_path = os.path.join(IMG_DIR, "screen2_tvora_mvp.png")
plt.tight_layout()
plt.savefig(out_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Tvora MVP UI rendered successfully to:", out_path)
