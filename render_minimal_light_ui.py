"""
render_minimal_light_ui.py
Renders a clean, light, minimal SaaS dashboard screenshot matching SalesPro & Tvora.
Uses soft light gray background, pure white cards, crisp typography, and natural colors.
Zero emoji glyph warnings.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_DIR = r"C:\Users\tejas\.gemini\antigravity\scratch\profitguard_work\screenshots"
os.makedirs(IMG_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=200)
fig.patch.set_facecolor('#f8fafc')
ax.set_facecolor('#f8fafc')
ax.axis('off')

# Left Sidebar (Crisp White)
sidebar = patches.Rectangle((0, 0), 0.17, 1.0, facecolor='#ffffff', edgecolor='#e2e8f0', lw=1)
ax.add_patch(sidebar)

# Minimal Brand Icon (clean geometric icon, no emoji glyph)
b_icon = patches.FancyBboxPatch((0.02, 0.925), 0.024, 0.038, boxstyle="round,pad=0.004",
                                fc='#fff7ed', ec='#fed7aa', lw=1)
ax.add_patch(b_icon)
# Small inner shield shape
shield = patches.Polygon([[0.032, 0.955], [0.039, 0.950], [0.039, 0.938], [0.032, 0.930], [0.025, 0.938], [0.025, 0.950]],
                         closed=True, facecolor='#f97316', edgecolor='none')
ax.add_patch(shield)

ax.text(0.052, 0.938, "ProfitGuard", color='#0f172a', fontsize=12.5, fontweight='bold', va='center')

# Sidebar Navigation (Minimal Gray & White)
nav_items = [
    ("Order Analytics", True),
    ("Sales & Margins", False),
    ("Customer ML", False),
    ("Data Profiling", False)
]
for i, (item, active) in enumerate(nav_items):
    y = 0.84 - i * 0.055
    if active:
        btn = patches.FancyBboxPatch((0.012, y - 0.012), 0.145, 0.038, boxstyle="round,pad=0.006",
                                     fc='#f1f5f9', ec='#e2e8f0', lw=1)
        ax.add_patch(btn)
        # Small circle indicator
        ax.plot(0.025, y, marker='o', markersize=4, color='#0f172a')
        ax.text(0.035, y, item, color='#0f172a', fontsize=8.2, fontweight='bold', va='center')
    else:
        ax.plot(0.025, y, marker='o', markersize=3, color='#94a3b8')
        ax.text(0.035, y, item, color='#64748b', fontsize=8.2, fontweight='normal', va='center')

# Sidebar Bottom Badge
badge_bg = patches.FancyBboxPatch((0.012, 0.04), 0.145, 0.09, boxstyle="round,pad=0.008",
                                  fc='#f8fafc', ec='#e2e8f0', lw=1)
ax.add_patch(badge_bg)
ax.text(0.022, 0.10, "DATATHON 2026", color='#0f172a', fontsize=7.2, fontweight='bold')
ax.text(0.022, 0.075, "Track 4: The Money Leak", color='#64748b', fontsize=6.8)
ax.text(0.022, 0.052, "18,000 Transactions", color='#0ea5e9', fontsize=6.8, fontweight='bold')

# Top Bar (SalesPro Style)
ax.text(0.20, 0.945, "Analytics Overview", color='#0f172a', fontsize=14.5, fontweight='bold')
ax.text(0.20, 0.92, "Detailed insights into transaction economics, realized margins, and risk detection.", color='#64748b', fontsize=8.2)

# Search & Action Pills
search_box = patches.FancyBboxPatch((0.70, 0.92), 0.13, 0.036, boxstyle="round,pad=0.008",
                                    fc='#ffffff', ec='#e2e8f0', lw=1)
ax.add_patch(search_box)
ax.text(0.71, 0.935, "Search orders...", color='#94a3b8', fontsize=7.2, va='center')

date_btn = patches.FancyBboxPatch((0.84, 0.92), 0.08, 0.036, boxstyle="round,pad=0.006",
                                  fc='#ffffff', ec='#e2e8f0', lw=1)
ax.add_patch(date_btn)
ax.text(0.88, 0.935, "All Time v", color='#0f172a', fontsize=7.2, ha='center', va='center', fontweight='bold')

export_btn = patches.FancyBboxPatch((0.925, 0.92), 0.055, 0.036, boxstyle="round,pad=0.006",
                                    fc='#0f172a', ec='none')
ax.add_patch(export_btn)
ax.text(0.952, 0.935, "Export", color='#ffffff', fontsize=7.2, ha='center', va='center', fontweight='bold')

# 4 Clean White KPI Cards (SalesPro Style)
kpi_data = [
    ("Completed Orders", "13,962", "+77.6%", True, "77.6% fulfillment rate"),
    ("Completed Revenue", "INR 73.02L", "+INR 7.30M", True, "Topline sales volume"),
    ("Loss-Making Leaks", "5,315", "-38.1%", False, "Orders sold below cost"),
    ("Estimated Leakage", "INR 12.14L", "-16.6%", False, "Net operating loss")
]

for i, (label, val, growth, is_pos, sub) in enumerate(kpi_data):
    x = 0.20 + i * 0.195
    card = patches.FancyBboxPatch((x, 0.77), 0.185, 0.125, boxstyle="round,pad=0.008",
                                  fc='#ffffff', ec='#e2e8f0', lw=1)
    ax.add_patch(card)

    ax.text(x + 0.012, 0.865, label, color='#64748b', fontsize=7.5, fontweight='bold')

    gb_fc = '#ecfdf5' if is_pos else '#fff1f2'
    gb_tc = '#047857' if is_pos else '#be123c'
    gb = patches.FancyBboxPatch((x + 0.122, 0.855), 0.052, 0.022, boxstyle="round,pad=0.004",
                                fc=gb_fc, ec='none')
    ax.add_patch(gb)
    ax.text(x + 0.148, 0.865, growth, color=gb_tc, fontsize=6.8, ha='center', va='center', fontweight='bold')

    val_col = '#0f172a' if is_pos else '#e11d48'
    ax.text(x + 0.012, 0.815, val, color=val_col, fontsize=12.5, fontweight='bold')
    ax.text(x + 0.012, 0.785, sub, color='#94a3b8', fontsize=6.5)

# Middle Row: Two Clean Visual Cards (SalesPro Aesthetic)
trend_card = patches.FancyBboxPatch((0.20, 0.49), 0.47, 0.255, boxstyle="round,pad=0.008",
                                    fc='#ffffff', ec='#e2e8f0', lw=1)
ax.add_patch(trend_card)
ax.text(0.215, 0.715, "Revenue & Margin Leakage Trend", color='#0f172a', fontsize=8.8, fontweight='bold')
ax.text(0.655, 0.715, "Monthly v", color='#64748b', fontsize=7, ha='right')

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
x_pts = [0.22 + j * 0.048 for j in range(len(months))]
y_rev = [0.55, 0.57, 0.63, 0.61, 0.66, 0.68, 0.65, 0.69, 0.64, 0.62]
y_leak = [0.52, 0.53, 0.56, 0.54, 0.57, 0.58, 0.55, 0.59, 0.54, 0.53]

poly_x = x_pts + [x_pts[-1], x_pts[0]]
poly_y = y_rev + [0.51, 0.51]
ax.fill(poly_x, poly_y, color='#fed7aa', alpha=0.35)
ax.plot(x_pts, y_rev, color='#f97316', lw=2)
ax.plot(x_pts, y_leak, color='#e11d48', lw=1.5, linestyle='--')

for j, m in enumerate(months):
    ax.text(x_pts[j], 0.50, m, color='#94a3b8', fontsize=6.2, ha='center')

# Card 2: Horizontal Category Bars (SalesPro Green Bar Aesthetic)
cat_card = patches.FancyBboxPatch((0.69, 0.49), 0.29, 0.255, boxstyle="round,pad=0.008",
                                  fc='#ffffff', ec='#e2e8f0', lw=1)
ax.add_patch(cat_card)
ax.text(0.705, 0.715, "Sales by Category", color='#0f172a', fontsize=8.8, fontweight='bold')
ax.text(0.965, 0.715, "All Categories v", color='#64748b', fontsize=7, ha='right')

cat_bars = [
    ("Home", 0.85, "INR 13.9L"),
    ("Electronics", 0.81, "INR 13.1L"),
    ("Sports", 0.79, "INR 13.0L"),
    ("Grocery", 0.77, "INR 12.8L"),
    ("Fashion", 0.65, "INR 10.7L")
]
for j, (cat_name, pct, val_str) in enumerate(cat_bars):
    by = 0.67 - j * 0.038
    ax.text(0.705, by, cat_name, color='#334155', fontsize=6.8, fontweight='bold', va='center')
    bar_bg = patches.FancyBboxPatch((0.765, by - 0.007), 0.155, 0.015, boxstyle="round,pad=0.003",
                                    fc='#f1f5f9', ec='none')
    ax.add_patch(bar_bg)
    bar_fill = patches.FancyBboxPatch((0.765, by - 0.007), 0.155 * pct, 0.015, boxstyle="round,pad=0.003",
                                      fc='#0d9488', ec='none')
    ax.add_patch(bar_fill)
    ax.text(0.965, by, val_str, color='#64748b', fontsize=6.5, ha='right', va='center')

# Bottom Row: Order Intelligence Table (Tvora Clean White Table)
table_card = patches.FancyBboxPatch((0.20, 0.04), 0.78, 0.425, boxstyle="round,pad=0.008",
                                    fc='#ffffff', ec='#e2e8f0', lw=1)
ax.add_patch(table_card)

ax.text(0.215, 0.435, "Order Intelligence & Risk Audits", color='#0f172a', fontsize=9.2, fontweight='bold')

ftabs = [("All Orders (18,000)", False), ("Loss Making (5,315)", True), ("Profitable (8,647)", False),
         ("Catalog Mispricing (4,770)", False), ("Promo Leakage (545)", False), ("Returns (1,431)", False)]
for j, (tname, active) in enumerate(ftabs):
    tx = 0.215 + j * 0.125
    if active:
        tbg = patches.FancyBboxPatch((tx, 0.395), 0.115, 0.024, boxstyle="round,pad=0.004",
                                     fc='#f1f5f9', ec='#cbd5e1', lw=0.8)
        ax.add_patch(tbg)
        ax.text(tx + 0.0575, 0.407, tname, color='#0f172a', fontsize=6.8, ha='center', va='center', fontweight='bold')
    else:
        ax.text(tx + 0.0575, 0.407, tname, color='#64748b', fontsize=6.8, ha='center', va='center')

ax.plot([0.215, 0.965], [0.385, 0.385], color='#e2e8f0', lw=1)
t_heads = [("Order ID", 0.22), ("Date", 0.29), ("Customer", 0.36), ("Product", 0.43), ("Category", 0.50),
           ("Order Value", 0.58), ("Unit Cost", 0.66), ("Profit Estimate", 0.74), ("Risk Score", 0.85), ("Tags", 0.91)]
for th, thx in t_heads:
    ax.text(thx, 0.37, th, color='#64748b', fontsize=6.8, fontweight='bold')
ax.plot([0.215, 0.965], [0.36, 0.36], color='#f1f5f9', lw=1)

sample_rows = [
    ("TX015158", "2025-08-14", "CU00939", "PR0163", "Electronics", "INR 199.85", "INR 238.49", "Loss (-INR 992.58)", "98/100", "Catalog Misprice", True),
    ("TX012734", "2025-06-22", "CU01046", "PR0037", "Beauty", "INR 103.00", "INR 218.49", "Loss (-INR 989.45)", "97/100", "Catalog Misprice", True),
    ("TX005702", "2025-09-02", "CU02351", "PR0021", "Beauty", "INR 206.30", "INR 236.46", "Loss (-INR 975.98)", "95/100", "Catalog Misprice", True),
    ("TX000001", "2025-08-22", "CU01588", "PR0103", "Sports", "INR 1,230.80", "INR 320.00", "Loss (-INR 369.20)", "85/100", "Promo Leakage", True),
    ("TX000004", "2025-07-11", "CU00842", "PR0015", "Fashion", "INR 1,850.00", "INR 110.00", "Profit (+INR 870.00)", "15/100", "Healthy", False)
]

for idx, (oid, dt, cust, prod, cat, val, cost, p_est, risk, tag, is_loss) in enumerate(sample_rows):
    ry = 0.335 - idx * 0.038
    ax.text(0.22, ry, oid, color='#0f172a', fontsize=7.2, fontweight='bold', va='center')
    ax.text(0.29, ry, dt, color='#64748b', fontsize=6.8, va='center')
    ax.text(0.36, ry, cust, color='#334155', fontsize=6.8, va='center')
    ax.text(0.43, ry, prod, color='#0ea5e9', fontsize=6.8, fontweight='bold', va='center')
    ax.text(0.50, ry, cat, color='#334155', fontsize=6.8, va='center')
    ax.text(0.58, ry, val, color='#0f172a', fontsize=6.8, fontweight='bold', va='center')
    ax.text(0.66, ry, cost, color='#64748b', fontsize=6.8, va='center')

    p_fc = '#fff1f2' if is_loss else '#ecfdf5'
    p_tc = '#e11d48' if is_loss else '#10b981'
    p_pill = patches.FancyBboxPatch((0.735, ry - 0.010), 0.098, 0.022, boxstyle="round,pad=0.003",
                                    fc=p_fc, ec='none')
    ax.add_patch(p_pill)
    ax.text(0.784, ry, p_est, color=p_tc, fontsize=6.4, ha='center', va='center', fontweight='bold')

    r_col = '#e11d48' if is_loss else '#10b981'
    ax.text(0.85, ry, risk, color=r_col, fontsize=6.8, fontweight='bold', va='center')

    t_pill = patches.FancyBboxPatch((0.905, ry - 0.010), 0.055, 0.022, boxstyle="round,pad=0.003",
                                    fc='#f1f5f9', ec='#e2e8f0', lw=0.6)
    ax.add_patch(t_pill)
    ax.text(0.9325, ry, tag[:11], color='#475569', fontsize=6.2, ha='center', va='center')

    ax.plot([0.215, 0.965], [ry - 0.016, ry - 0.016], color='#f8fafc', lw=0.8)

# Minimal Human-Readable Audit Footnote
audit_pill = patches.FancyBboxPatch((0.215, 0.06), 0.745, 0.065, boxstyle="round,pad=0.006",
                                    fc='#f8fafc', ec='#e2e8f0', lw=1)
ax.add_patch(audit_pill)
ax.text(0.23, 0.098, "Audit Breakdown: TX000001 (PR0103)", color='#0f172a', fontsize=7.5, fontweight='bold')
ax.text(0.23, 0.075, "Formula: Q x [P(1 - D) - C] = 5 x [INR 307.70 x (1 - 0.20) - INR 320.00] = 5 x (-INR 73.84) = -INR 369.20", color='#334155', fontsize=6.8, fontfamily='monospace')
ax.text(0.72, 0.086, "Root Cause: Promo Discount Exceeded Margin Floor", color='#e11d48', fontsize=6.8, fontweight='bold')

out_path = os.path.join(IMG_DIR, "screen2_minimal_light.png")
plt.tight_layout()
plt.savefig(out_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close()
print("Clean minimal light UI rendered with zero warnings to:", out_path)
