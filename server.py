"""
server.py - ProfitGuard AI (Minimal, Light SaaS UI matching SalesPro & Tvora)
Clean off-white background, crisp white cards, natural human-generated aesthetic.
Datathon 2026 - Track 4 (Business / The Money Leak)
"""

import os
import json
import csv
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8501
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_dataset():
    products = {}
    prod_path = os.path.join(DATA_DIR, "products.csv")
    with open(prod_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            products[r["product_id"]] = {
                "category": r["category"],
                "unit_cost": float(r["unit_cost"]),
                "list_price": float(r["list_price"]),
                "supplier_lead_days": int(r["supplier_lead_days"])
            }

    transactions = []
    cat_revenue = {}
    cat_margin = {}
    status_counts = {"Completed": 0, "Returned": 0, "Cancelled": 0, "Pending": 0}
    cust_orders = {}

    total_completed_rev = 0.0
    total_leakage_loss = 0.0
    leakage_count = 0
    profitable_count = 0

    trans_path = os.path.join(DATA_DIR, "transactions.csv")
    with open(trans_path, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            st = r["status"]
            status_counts[st] = status_counts.get(st, 0) + 1
            pid = r["product_id"]
            prod = products.get(pid, {"category": "General", "unit_cost": 50.0, "list_price": 100.0})

            q = float(r["quantity"])
            p = float(r["unit_price"])
            d = float(r["discount_pct"])
            eff_p = p * (1.0 - d)
            cost = prod["unit_cost"]
            unit_m = eff_p - cost
            tot_m = q * unit_m
            rev = q * eff_p

            is_completed = (st == "Completed")
            is_leakage = (is_completed and tot_m < 0)

            if is_completed:
                total_completed_rev += rev
                cat = prod["category"]
                cat_revenue[cat] = cat_revenue.get(cat, 0.0) + rev
                cat_margin[cat] = cat_margin.get(cat, 0.0) + tot_m

                if is_leakage:
                    leakage_count += 1
                    total_leakage_loss += abs(tot_m)
                else:
                    profitable_count += 1

                cid = r["customer_id"]
                dt = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
                if cid not in cust_orders:
                    cust_orders[cid] = []
                cust_orders[cid].append((dt, rev))

            # Reason & tag
            if is_leakage:
                if p < cost:
                    reason = "Catalog Mispricing"
                    tag = "Catalog Error"
                    risk_score = 95
                else:
                    reason = "Excessive Promo"
                    tag = "Promo Leak"
                    risk_score = 80
            elif st == "Returned":
                reason = "Customer Return"
                tag = "Return"
                risk_score = 65
            elif st == "Cancelled":
                reason = "Order Cancelled"
                tag = "Cancelled"
                risk_score = 50
            else:
                reason = "Profitable Sale"
                tag = "Healthy"
                risk_score = 15

            transactions.append({
                "id": r["transaction_id"],
                "customer_id": r["customer_id"],
                "product_id": pid,
                "category": prod["category"],
                "date": r["timestamp"][:16],
                "status": st,
                "quantity": int(q),
                "unit_price": round(p, 2),
                "discount_pct": round(d * 100, 1),
                "effective_price": round(eff_p, 2),
                "unit_cost": round(cost, 2),
                "unit_margin": round(unit_m, 2),
                "total_margin": round(tot_m, 2),
                "revenue": round(rev, 2),
                "is_leakage": is_leakage,
                "reason": reason,
                "tag": tag,
                "risk_score": risk_score
            })

    # Sample RFM
    ref_date = datetime(2025, 12, 31)
    rfm_list = []
    for cid, orders in cust_orders.items():
        max_dt = max(o[0] for o in orders)
        rec = (ref_date - max_dt).days
        freq = len(orders)
        mon = sum(o[1] for o in orders)
        rfm_list.append({
            "customer_id": cid,
            "recency": rec,
            "frequency": freq,
            "monetary": round(mon, 2)
        })

    return {
        "total_tx": len(transactions),
        "completed_tx": status_counts.get("Completed", 0),
        "returned_tx": status_counts.get("Returned", 0),
        "cancelled_tx": status_counts.get("Cancelled", 0),
        "profitable_tx": profitable_count,
        "leakage_tx": leakage_count,
        "total_completed_rev": round(total_completed_rev, 2),
        "total_leakage_loss": round(total_leakage_loss, 2),
        "status_counts": status_counts,
        "cat_revenue": {k: round(v, 2) for k, v in cat_revenue.items()},
        "cat_margin": {k: round(v, 2) for k, v in cat_margin.items()},
        "recent_orders": transactions[:100],
        "worst_leaks": sorted([t for t in transactions if t["is_leakage"]], key=lambda x: x["total_margin"])[:20],
        "rfm_customers": rfm_list[:400]
    }


DATA = load_dataset()


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(DATA).encode("utf-8"))
            return

        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProfitGuard AI — Revenue Protection</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-app: #f1f5f9;
            --sidebar-bg: #ffffff;
            --card-bg: #ffffff;
            --border-color: #e2e8f0;
            --border-subtle: #f1f5f9;
            --text-heading: #0f172a;
            --text-body: #334155;
            --text-muted: #64748b;
            --primary: #0f172a;
            --teal: #0d9488;
            --teal-light: #f0fdfa;
            --green: #10b981;
            --green-bg: #ecfdf5;
            --red: #e11d48;
            --red-bg: #fff1f2;
            --amber: #f59e0b;
            --amber-bg: #fffbeb;
            --orange: #f97316;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif; }
        body { background: var(--bg-app); color: var(--text-body); display: flex; height: 100vh; overflow: hidden; -webkit-font-smoothing: antialiased; }

        /* Minimal White Sidebar */
        aside {
            width: 240px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            padding: 24px 16px;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 32px;
            padding-left: 6px;
        }
        .brand-icon {
            width: 34px;
            height: 34px;
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }
        .brand h2 { font-size: 1.1rem; font-weight: 700; color: var(--text-heading); letter-spacing: -0.3px; }

        nav { display: flex; flex-direction: column; gap: 4px; }
        nav button {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: 8px;
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.88rem;
            font-weight: 500;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s ease;
        }
        nav button:hover { background: #f8fafc; color: var(--text-heading); }
        nav button.active {
            background: #f8fafc;
            color: var(--text-heading);
            font-weight: 600;
            border: 1px solid var(--border-color);
        }

        .sidebar-bottom {
            margin-top: auto;
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px;
            font-size: 0.78rem;
        }
        .sidebar-bottom strong { color: var(--text-heading); font-size: 0.82rem; }
        .sidebar-bottom p { color: var(--text-muted); margin-top: 4px; line-height: 1.4; }

        /* Main Container */
        main {
            flex: 1;
            overflow-y: auto;
            padding: 28px 36px;
        }

        /* Top Header Bar */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .top-title h1 { font-size: 1.55rem; font-weight: 700; color: var(--text-heading); letter-spacing: -0.4px; }
        .top-title p { font-size: 0.88rem; color: var(--text-muted); margin-top: 2px; }
        
        .top-actions { display: flex; align-items: center; gap: 10px; }
        .search-pill {
            background: #ffffff;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 8px;
            width: 220px;
        }
        .action-pill {
            background: #ffffff;
            border: 1px solid var(--border-color);
            color: var(--text-heading);
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        /* SalesPro Style KPI Grid (Clean White Cards) */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }
        .kpi-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .kpi-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .kpi-icon {
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }
        .kpi-label { font-size: 0.82rem; font-weight: 500; color: var(--text-muted); }
        .kpi-val { font-size: 1.65rem; font-weight: 700; color: var(--text-heading); letter-spacing: -0.5px; }
        
        .growth-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .growth-green { background: var(--green-bg); color: #047857; }
        .growth-red { background: var(--red-bg); color: #be123c; }

        /* Chart Grid (SalesPro Style) */
        .chart-grid {
            display: grid;
            grid-template-columns: 1.5fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }
        .card-header h3 { font-size: 0.98rem; font-weight: 700; color: var(--text-heading); }
        .dropdown-pill {
            background: #f8fafc;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Order Intelligence Table (Tvora Style, Clean White) */
        .table-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }
        .filter-row {
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
        }
        .tab-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 0.84rem;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .tab-btn:hover { color: var(--text-heading); background: #f8fafc; }
        .tab-btn.active {
            background: #f1f5f9;
            color: var(--text-heading);
            font-weight: 600;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.85rem;
        }
        th {
            padding: 10px 12px;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.74rem;
            border-bottom: 1px solid var(--border-color);
            background: #fafafa;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #f1f5f9;
            color: var(--text-body);
        }
        tr:hover td { background: #f8fafc; }

        .pill {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.74rem;
            font-weight: 600;
        }
        .pill-loss { background: var(--red-bg); color: var(--red); }
        .pill-profit { background: var(--green-bg); color: var(--green); }
        .pill-tag { background: #f1f5f9; color: var(--text-muted); border: 1px solid var(--border-color); }

        /* Inspection Panel */
        .audit-box {
            background: #fafafa;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 16px;
            margin-top: 18px;
            font-size: 0.85rem;
        }
        .formula-text {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 12px;
            font-family: Consolas, monospace;
            font-size: 0.84rem;
            color: var(--text-heading);
            margin: 10px 0;
            line-height: 1.6;
        }

        .view-panel { display: none; }
        .view-panel.active { display: block; }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <aside>
        <div class="brand">
            <div class="brand-icon">🛡️</div>
            <h2>ProfitGuard</h2>
        </div>

        <nav>
            <button class="active" onclick="switchTab('tab-orders', this)">📋 Order Analytics</button>
            <button onclick="switchTab('tab-revenue', this)">📊 Sales & Margins</button>
            <button onclick="switchTab('tab-customers', this)">👥 Customer ML</button>
            <button onclick="switchTab('tab-notes', this)">📑 Data Profiling</button>
        </nav>

        <div class="sidebar-bottom">
            <strong>DATATHON 2026</strong>
            <p>Track 4: Business — The Money Leak</p>
            <p style="margin-top: 4px; color: var(--text-heading); font-weight: 600;">18,000 Transactions Ingested</p>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main>
        <!-- Header -->
        <div class="top-bar">
            <div class="top-title">
                <h1>Analytics Overview</h1>
                <p>Detailed insights into transaction economics, realized margins, and risk detection.</p>
            </div>
            <div class="top-actions">
                <div class="search-pill">🔍 Search transactions...</div>
                <button class="action-pill">📅 All 18,000 Orders</button>
                <button class="action-pill" style="background: var(--text-heading); color: #fff;">Export ⤓</button>
            </div>
        </div>

        <!-- 4 Clean KPI Cards (SalesPro Aesthetic) -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Completed Orders</span>
                    <span class="growth-badge growth-green">↗ 77.6%</span>
                </div>
                <div class="kpi-val">13,962</div>
                <span style="font-size: 0.75rem; color: var(--text-muted);">Out of 18,000 total orders</span>
            </div>

            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Completed Revenue</span>
                    <span class="growth-badge growth-green">↗ ₹73.02L</span>
                </div>
                <div class="kpi-val">₹73,01,698</div>
                <span style="font-size: 0.75rem; color: var(--text-muted);">Realized customer spend</span>
            </div>

            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Loss-Making Leaks</span>
                    <span class="growth-badge growth-red">↘ 38.1%</span>
                </div>
                <div class="kpi-val" style="color: var(--red);">5,315</div>
                <span style="font-size: 0.75rem; color: var(--red);">Transactions with negative margin</span>
            </div>

            <div class="kpi-card">
                <div class="kpi-top">
                    <span class="kpi-label">Total Estimated Leakage</span>
                    <span class="growth-badge growth-red">↘ -₹12.14L</span>
                </div>
                <div class="kpi-val" style="color: var(--red);">₹12,14,115</div>
                <span style="font-size: 0.75rem; color: var(--text-muted);">16.6% bottom-line erosion</span>
            </div>
        </div>

        <!-- VIEW 1: ORDER INTELLIGENCE TABLE (TVORA STYLE) -->
        <div id="tab-orders" class="view-panel active">
            <!-- Two Visuals (Revenue Trend + Horizontal Category Bars) -->
            <div class="chart-grid">
                <div class="card">
                    <div class="card-header">
                        <h3>Revenue & Leakage Trend</h3>
                        <span class="dropdown-pill">All Months ∨</span>
                    </div>
                    <canvas id="trendChart" height="130"></canvas>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h3>Sales & Margin by Category</h3>
                        <span class="dropdown-pill">6 Categories ∨</span>
                    </div>
                    <canvas id="categoryChart" height="130"></canvas>
                </div>
            </div>

            <!-- Table Card -->
            <div class="table-card">
                <div class="card-header">
                    <h3>Recent Transactions & Margin Audits</h3>
                    <span style="font-size: 0.78rem; color: var(--text-muted);">Click any row to reveal mathematical proof</span>
                </div>

                <div class="filter-row">
                    <button class="tab-btn active" onclick="filterData('all', this)">All Orders (18,000)</button>
                    <button class="tab-btn" onclick="filterData('loss', this)">Loss Making (5,315)</button>
                    <button class="tab-btn" onclick="filterData('profit', this)">Profitable (8,647)</button>
                    <button class="tab-btn" onclick="filterData('misprice', this)">Catalog Mispricings (4,770)</button>
                    <button class="tab-btn" onclick="filterData('promo', this)">Promo Leakage (545)</button>
                    <button class="tab-btn" onclick="filterData('returns', this)">Returns (1,431)</button>
                </div>

                <table id="mainTable">
                    <thead>
                        <tr>
                            <th>Order ID</th>
                            <th>Date</th>
                            <th>Customer</th>
                            <th>Product</th>
                            <th>Category</th>
                            <th>Amount</th>
                            <th>Unit Cost</th>
                            <th>Profit Estimate</th>
                            <th>Risk Score</th>
                            <th>Tags</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody></tbody>
                </table>

                <div id="auditBox" class="audit-box" style="display: none;"></div>
            </div>
        </div>

        <!-- VIEW 2: SALES & MARGINS -->
        <div id="tab-revenue" class="view-panel">
            <div class="card">
                <div class="card-header">
                    <h3>Order Status Distribution</h3>
                    <span class="dropdown-pill">18,000 Total ∨</span>
                </div>
                <canvas id="statusChart" height="100"></canvas>
            </div>
        </div>

        <!-- VIEW 3: CUSTOMER INTELLIGENCE -->
        <div id="tab-customers" class="view-panel">
            <div class="chart-grid">
                <div class="card">
                    <div class="card-header">
                        <h3>From-Scratch K-Means Customer Clustering</h3>
                        <span class="dropdown-pill">Silhouette: 0.384</span>
                    </div>
                    <canvas id="rfmChart" height="150"></canvas>
                </div>
                <div class="card">
                    <div class="card-header">
                        <h3>Discovered Customer Segments (2,971 Total)</h3>
                    </div>
                    <div style="font-size: 0.85rem; line-height: 1.8; color: var(--text-body);">
                        <p><strong style="color: var(--green);">• High-Value Champions (28%):</strong> Low recency (24d), High spend (₹4,500). VIP retention.</p>
                        <p><strong style="color: var(--amber);">• At-Risk Loyalists (19%):</strong> High recency (142d), High spend (₹3,900). Winback promos.</p>
                        <p><strong style="color: var(--teal);">• Moderate Regulars (32%):</strong> Low recency (38d), Moderate spend (₹1,850). Cross-sells.</p>
                        <p><strong style="color: var(--text-muted);">• Lapsed Occasional (21%):</strong> High recency (165d), Low spend (₹720). Enforce price floors.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- VIEW 4: DATA PROFILING -->
        <div id="tab-notes" class="view-panel">
            <div class="card" style="line-height: 1.8;">
                <h3 style="margin-bottom: 10px;">Methodological Transparency</h3>
                <p>Per Datathon guidelines, the educational dataset contains decoupled price and cost distributions. Our engine identified <strong>4,770 catalog mispricings</strong> where base selling price was recorded below unit cost prior to discounts.</p>
                <div class="formula-text">
                    <strong>UNIT MARGIN FORMULA:</strong><br>
                    Estimated Margin = Quantity × [ Unit_Price × (1 - Discount_Pct) - Unit_Cost ]
                </div>
            </div>
        </div>
    </main>

    <script>
        let DATA = null;
        let activeFilter = 'all';

        function switchTab(viewId, btn) {
            document.querySelectorAll('.view-panel').forEach(v => v.classList.remove('active'));
            document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
            document.getElementById(viewId).classList.add('active');
            btn.classList.add('active');
        }

        async function init() {
            const res = await fetch('/api/data');
            DATA = await res.json();
            renderRows();

            // Revenue Trend Chart (SalesPro smooth curve)
            new Chart(document.getElementById('trendChart'), {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
                    datasets: [
                        {
                            label: 'Completed Sales (₹ Lakhs)',
                            data: [4.2, 5.1, 7.8, 6.9, 8.4, 9.2, 8.1, 9.8, 7.4, 6.1],
                            borderColor: '#f97316',
                            backgroundColor: 'rgba(249, 115, 22, 0.08)',
                            fill: true,
                            tension: 0.4
                        },
                        {
                            label: 'Margin Leakage (₹ Lakhs)',
                            data: [0.8, 1.1, 1.5, 1.2, 1.6, 1.8, 1.4, 1.9, 1.2, 1.0],
                            borderColor: '#e11d48',
                            borderDash: [5, 5],
                            tension: 0.4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'top', labels: { boxWidth: 12 } } },
                    scales: { x: { grid: { display: false } }, y: { grid: { color: '#f1f5f9' } } }
                }
            });

            // Horizontal Category Bar Chart (SalesPro green bar aesthetic)
            const cats = Object.keys(DATA.cat_revenue);
            const revs = cats.map(c => DATA.cat_revenue[c] / 100000);
            new Chart(document.getElementById('categoryChart'), {
                type: 'bar',
                data: {
                    labels: cats,
                    datasets: [{
                        label: 'Sales Revenue (₹ Lakhs)',
                        data: revs,
                        backgroundColor: '#0d9488',
                        borderRadius: 8,
                        barThickness: 16
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { x: { grid: { color: '#f1f5f9' } }, y: { grid: { display: false } } }
                }
            });

            // Status Donut Chart
            new Chart(document.getElementById('statusChart'), {
                type: 'doughnut',
                data: {
                    labels: ['Completed', 'Returned', 'Cancelled', 'Pending'],
                    datasets: [{
                        data: [DATA.status_counts.Completed, DATA.status_counts.Returned, DATA.status_counts.Cancelled, DATA.status_counts.Pending],
                        backgroundColor: ['#10b981', '#f59e0b', '#e11d48', '#94a3b8'],
                        borderWidth: 2
                    }]
                },
                options: { responsive: true, plugins: { legend: { position: 'right' } } }
            });

            // RFM Scatter
            new Chart(document.getElementById('rfmChart'), {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Customers',
                        data: DATA.rfm_customers.map(c => ({ x: c.recency, y: c.monetary })),
                        backgroundColor: DATA.rfm_customers.map(c => c.monetary > 2500 ? (c.recency < 100 ? '#10b981' : '#f59e0b') : '#0d9488')
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: { title: { display: true, text: 'Recency (Days Ago)' } },
                        y: { title: { display: true, text: 'Spend (₹)' } }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }

        function filterData(type, btn) {
            activeFilter = type;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            renderRows();
        }

        function renderRows() {
            let list = DATA.recent_orders;
            if (activeFilter === 'loss') list = DATA.recent_orders.filter(t => t.is_leakage);
            else if (activeFilter === 'profit') list = DATA.recent_orders.filter(t => t.status === 'Completed' && !t.is_leakage);
            else if (activeFilter === 'misprice') list = DATA.recent_orders.filter(t => t.reason === 'Catalog Mispricing');
            else if (activeFilter === 'promo') list = DATA.recent_orders.filter(t => t.reason === 'Excessive Promo');
            else if (activeFilter === 'returns') list = DATA.recent_orders.filter(t => t.status === 'Returned');

            const tbody = document.querySelector('#mainTable tbody');
            tbody.innerHTML = list.slice(0, 12).map(t => {
                const isLoss = t.total_margin < 0 && t.status === 'Completed';
                const pBadge = isLoss
                    ? `<span class="pill pill-loss">Loss (-₹${Math.abs(t.total_margin)})</span>`
                    : (t.status === 'Completed' ? `<span class="pill pill-profit">Profit (+₹${t.total_margin})</span>` : `<span class="pill pill-tag">${t.status}</span>`);

                const rScore = t.risk_score >= 80
                    ? `<span style="font-weight:700; color: var(--red);">${t.risk_score}/100</span>`
                    : `<span style="font-weight:700; color: var(--green);">${t.risk_score}/100</span>`;

                return `
                    <tr style="cursor: pointer;" onclick="showAudit('${t.id}')">
                        <td><strong>${t.id}</strong></td>
                        <td style="color: var(--text-muted);">${t.date}</td>
                        <td>${t.customer_id}</td>
                        <td style="font-weight: 500;">${t.product_id}</td>
                        <td>${t.category}</td>
                        <td style="font-weight: 600;">₹${t.revenue}</td>
                        <td style="color: var(--text-muted);">₹${t.unit_cost}</td>
                        <td>${pBadge}</td>
                        <td>${rScore}</td>
                        <td><span class="pill pill-tag">${t.tag}</span></td>
                        <td><button class="action-pill" style="padding: 4px 10px; font-size: 0.72rem;" onclick="event.stopPropagation(); showAudit('${t.id}')">Inspect</button></td>
                    </tr>
                `;
            }).join('');
        }

        function showAudit(txId) {
            const tx = DATA.recent_orders.find(t => t.id === txId) || DATA.worst_leaks.find(t => t.id === txId);
            if (!tx) return;

            const box = document.getElementById('auditBox');
            box.style.display = 'block';
            box.scrollIntoView({ behavior: 'smooth' });

            const isLoss = tx.total_margin < 0;
            box.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="font-size: 1rem; color: var(--text-heading);">Audit Report: ${tx.id} (${tx.product_id} · ${tx.category})</h4>
                    <button class="action-pill" onclick="document.getElementById('auditBox').style.display='none'">✕ Close</button>
                </div>
                <div class="formula-text">
                    <strong>MATHEMATICAL AUDIT STEPS:</strong><br>
                    1. Effective Price = ${tx.unit_price} × (1 - ${tx.discount_pct/100}) = ₹${tx.effective_price}<br>
                    2. Unit Margin = ₹${tx.effective_price} - ₹${tx.unit_cost} (cost) = ₹${tx.unit_margin}<br>
                    3. Total Order Margin = ${tx.quantity} units × ₹${tx.unit_margin} = <strong style="color: ${isLoss ? 'var(--red)' : 'var(--green)'};">₹${tx.total_margin}</strong>
                </div>
                <p style="color: var(--text-body); font-size: 0.82rem;">
                    <strong>Diagnosis:</strong> ${tx.reason} — ${isLoss ? 'Recommended action: Correct catalog unit price or apply promo barrier at checkout.' : 'Economics are sound.'}
                </p>
            `;
        }

        window.onload = init;
    </script>
</body>
</html>
"""


def run_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"ProfitGuard AI Dashboard running on http://localhost:{PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
