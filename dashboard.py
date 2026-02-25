#!/usr/bin/env python3
"""
MegaMind Dashboard — Knowledge graph visualisation and extraction manager.

A lightweight web dashboard that provides:
  - Interactive knowledge graph of categories, tags, and extractions
  - Status management (Backlog → TODO → Done → Cancel)
  - Click-through links to Discord threads, Obsidian notes, YouTube videos, source URLs
  - API budget overview

Usage:
    python dashboard.py              # Starts on http://localhost:8050
    python dashboard.py --port 9000  # Custom port
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

import config
from outputs.index import _read_index, update_status

DASHBOARD_PORT = int(__import__("os").getenv("DASHBOARD_PORT", "8050"))


def _parse_index_entries() -> list[dict]:
    """Parse INDEX.md into a list of entry dicts."""
    content = _read_index()
    entries = []
    for line in content.split("\n"):
        if not line.startswith("|") or line.startswith("| #") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 9:
            continue
        # cells: ['', '#', 'Title', 'Source', 'Category', 'Tags', 'Status', 'Date', 'File', '']
        tags_raw = cells[5]
        tags = re.findall(r"`#([^`]+)`", tags_raw)
        file_match = re.search(r"\[view\]\(\./(.+?)\)", cells[8])
        filename = file_match.group(1) if file_match else ""

        entries.append({
            "num": cells[1],
            "title": cells[2],
            "source": cells[3],
            "category": cells[4],
            "tags": tags,
            "status": cells[6],
            "date": cells[7],
            "filename": filename,
        })
    return entries


def _load_budget() -> dict:
    """Load budget data."""
    budget_file = config.PROJECT_ROOT / "api_budget.json"
    if budget_file.exists():
        try:
            return json.loads(budget_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            pass
    return {"total_cost": 0, "extraction_count": 0, "total_input_tokens": 0, "total_output_tokens": 0, "history": []}


def _build_graph_data(entries: list[dict]) -> dict:
    """Build nodes and links for the knowledge graph."""
    nodes = []
    links = []
    node_ids = set()

    # Centre node
    nodes.append({"id": "megamind", "label": "MegaMind", "group": "centre", "size": 30})
    node_ids.add("megamind")

    # Category nodes
    categories = set(e["category"] for e in entries if e["category"])
    for cat in categories:
        cat_id = f"cat:{cat}"
        if cat_id not in node_ids:
            nodes.append({"id": cat_id, "label": cat, "group": "category", "size": 20})
            node_ids.add(cat_id)
            links.append({"source": "megamind", "target": cat_id})

    # Tag nodes
    all_tags = set()
    for e in entries:
        all_tags.update(e["tags"])
    for tag in all_tags:
        tag_id = f"tag:{tag}"
        if tag_id not in node_ids:
            nodes.append({"id": tag_id, "label": f"#{tag}", "group": "tag", "size": 10})
            node_ids.add(tag_id)

    # Extraction nodes and links
    for e in entries:
        ext_id = f"ext:{e['num']}"
        status_class = e["status"].lower().replace(" ", "-")
        nodes.append({
            "id": ext_id,
            "label": e["title"][:40],
            "group": "extraction",
            "status": status_class,
            "size": 14,
            "data": e,
        })
        node_ids.add(ext_id)

        # Link to category
        cat_id = f"cat:{e['category']}"
        if cat_id in node_ids:
            links.append({"source": cat_id, "target": ext_id})

        # Link to tags
        for tag in e["tags"]:
            tag_id = f"tag:{tag}"
            if tag_id in node_ids:
                links.append({"source": ext_id, "target": tag_id})

    return {"nodes": nodes, "links": links}


def _build_html(entries: list[dict], budget: dict) -> str:
    """Generate the full dashboard HTML with embedded JS knowledge graph."""
    graph_data = _build_graph_data(entries)
    entries_json = json.dumps(entries)
    graph_json = json.dumps(graph_data)
    budget_json = json.dumps(budget)

    status_counts = {}
    for e in entries:
        s = e["status"]
        status_counts[s] = status_counts.get(s, 0) + 1
    source_counts = {}
    for e in entries:
        s = e["source"]
        source_counts[s] = source_counts.get(s, 0) + 1

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MegaMind Dashboard</title>
<style>
  :root {{
    --bg: #0f172a; --surface: #1e293b; --border: #334155;
    --text: #e2e8f0; --muted: #94a3b8; --accent: #818cf8;
    --green: #34d399; --amber: #fbbf24; --red: #f87171; --blue: #60a5fa;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); }}
  .header {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; }}
  .header h1 {{ font-size: 1.4rem; font-weight: 700; }}
  .header h1 span {{ color: var(--accent); }}
  .stats {{ display: flex; gap: 1.5rem; font-size: 0.85rem; color: var(--muted); }}
  .stats .stat {{ text-align: center; }}
  .stats .stat-value {{ font-size: 1.3rem; font-weight: 700; color: var(--text); }}
  .layout {{ display: grid; grid-template-columns: 1fr 380px; height: calc(100vh - 60px); }}
  .graph-panel {{ position: relative; overflow: hidden; }}
  #graph {{ width: 100%; height: 100%; }}
  .sidebar {{ background: var(--surface); border-left: 1px solid var(--border); overflow-y: auto; }}
  .sidebar-header {{ padding: 1rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }}
  .sidebar-header h2 {{ font-size: 1rem; font-weight: 600; }}
  .filters {{ padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); display: flex; gap: 0.5rem; flex-wrap: wrap; }}
  .filter-btn {{ padding: 0.25rem 0.75rem; border-radius: 9999px; border: 1px solid var(--border); background: transparent; color: var(--muted); cursor: pointer; font-size: 0.75rem; transition: all 0.2s; }}
  .filter-btn:hover, .filter-btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}
  .entry-list {{ padding: 0.5rem; }}
  .entry-card {{ background: var(--bg); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem; margin-bottom: 0.5rem; cursor: pointer; transition: border-color 0.2s; }}
  .entry-card:hover {{ border-color: var(--accent); }}
  .entry-title {{ font-size: 0.85rem; font-weight: 600; margin-bottom: 0.35rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .entry-meta {{ display: flex; gap: 0.5rem; align-items: center; font-size: 0.7rem; color: var(--muted); flex-wrap: wrap; }}
  .badge {{ padding: 0.1rem 0.5rem; border-radius: 9999px; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; }}
  .badge-backlog {{ background: #374151; color: #9ca3af; }}
  .badge-todo {{ background: #1e3a5f; color: var(--blue); }}
  .badge-in-progress {{ background: #422006; color: var(--amber); }}
  .badge-done {{ background: #064e3b; color: var(--green); }}
  .badge-cancel {{ background: #450a0a; color: var(--red); }}
  .tag {{ color: var(--accent); }}
  .status-select {{ background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 4px; padding: 0.2rem 0.4rem; font-size: 0.7rem; cursor: pointer; }}
  .budget-bar {{ padding: 1rem; border-top: 1px solid var(--border); background: var(--bg); }}
  .budget-bar h3 {{ font-size: 0.8rem; color: var(--muted); margin-bottom: 0.5rem; }}
  .budget-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.75rem; }}
  .budget-item {{ background: var(--surface); padding: 0.5rem; border-radius: 6px; }}
  .budget-item .label {{ color: var(--muted); font-size: 0.65rem; }}
  .budget-item .value {{ font-weight: 700; font-size: 1rem; }}
  .legend {{ position: absolute; bottom: 1rem; left: 1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem; font-size: 0.7rem; }}
  .legend-item {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
  .view-toggle {{ display: flex; gap: 0.25rem; }}
  .view-btn {{ padding: 0.25rem 0.5rem; border-radius: 4px; border: 1px solid var(--border); background: transparent; color: var(--muted); cursor: pointer; font-size: 0.7rem; }}
  .view-btn.active {{ background: var(--accent); color: white; border-color: var(--accent); }}
  .zoom-controls {{ position: absolute; top: 1rem; right: 1rem; display: flex; flex-direction: column; gap: 0.25rem; }}
  .zoom-btn {{ width: 32px; height: 32px; border-radius: 6px; border: 1px solid var(--border); background: var(--surface); color: var(--text); cursor: pointer; font-size: 1.1rem; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }}
  .zoom-btn:hover {{ background: var(--accent); color: white; }}
  .layout.graph-only {{ grid-template-columns: 1fr; }}
  .layout.graph-only .sidebar {{ display: none; }}
  canvas {{ display: block; }}
</style>
</head>
<body>
<div class="header">
  <h1><span>MegaMind</span> Dashboard</h1>
  <div class="stats">
    <div class="stat"><div class="stat-value">{len(entries)}</div>Extractions</div>
    <div class="stat"><div class="stat-value">{len(set(e['category'] for e in entries))}</div>Categories</div>
    <div class="stat"><div class="stat-value">{len(set(t for e in entries for t in e['tags']))}</div>Tags</div>
    <div class="stat"><div class="stat-value">${budget.get('total_cost', 0):.4f}</div>API Cost</div>
  </div>
</div>
<div class="layout">
  <div class="graph-panel">
    <canvas id="graph"></canvas>
    <div class="zoom-controls">
      <button class="zoom-btn" onclick="zoomIn()" title="Zoom in">+</button>
      <button class="zoom-btn" onclick="zoomOut()" title="Zoom out">&minus;</button>
      <button class="zoom-btn" onclick="zoomReset()" title="Reset zoom">&#8634;</button>
    </div>
    <div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:#818cf8"></div>Centre</div>
      <div class="legend-item"><div class="legend-dot" style="background:#f59e0b"></div>Category</div>
      <div class="legend-item"><div class="legend-dot" style="background:#34d399"></div>Extraction</div>
      <div class="legend-item"><div class="legend-dot" style="background:#60a5fa"></div>Tag</div>
    </div>
  </div>
  <div class="sidebar">
    <div class="sidebar-header">
      <h2>Extractions</h2>
      <div class="view-toggle">
        <button class="view-btn active" onclick="setView('all')">All</button>
        <button class="view-btn" onclick="setView('graph')">Graph only</button>
      </div>
    </div>
    <div class="filters" id="filters"></div>
    <div class="entry-list" id="entry-list"></div>
    <div class="budget-bar">
      <h3>API Budget</h3>
      <div class="budget-grid">
        <div class="budget-item"><div class="label">Total Spend</div><div class="value">${budget.get('total_cost', 0):.4f}</div></div>
        <div class="budget-item"><div class="label">Extractions</div><div class="value">{budget.get('extraction_count', 0)}</div></div>
        <div class="budget-item"><div class="label">Input Tokens</div><div class="value">{budget.get('total_input_tokens', 0):,}</div></div>
        <div class="budget-item"><div class="label">Output Tokens</div><div class="value">{budget.get('total_output_tokens', 0):,}</div></div>
      </div>
    </div>
  </div>
</div>

<script>
const entries = {entries_json};
const graphData = {graph_json};
const budget = {budget_json};
let activeFilter = 'all';

// ── Render entry list ──
function renderEntries(filter) {{
  const list = document.getElementById('entry-list');
  let filtered = entries;
  if (filter && filter !== 'all') {{
    filtered = entries.filter(e =>
      e.status.toLowerCase() === filter.toLowerCase() ||
      e.category.toLowerCase() === filter.toLowerCase() ||
      e.source.toLowerCase() === filter.toLowerCase()
    );
  }}
  list.innerHTML = filtered.map(e => `
    <div class="entry-card" data-num="${{e.num}}" onclick="highlightNode('ext:${{e.num}}')">
      <div class="entry-title">${{e.title}}</div>
      <div class="entry-meta">
        <span class="badge badge-${{e.status.toLowerCase().replace(' ', '-')}}">${{e.status}}</span>
        <span>${{e.source}}</span>
        <span>${{e.category}}</span>
        <span>${{e.date}}</span>
        <select class="status-select" onchange="updateStatus(${{e.num}}, this.value)" onclick="event.stopPropagation()">
          ${{['Backlog','TODO','In Progress','Done','Cancel'].map(s =>
            `<option value="${{s}}" ${{e.status===s?'selected':''}}>${{s}}</option>`
          ).join('')}}
        </select>
      </div>
      <div class="entry-meta" style="margin-top:0.25rem">
        ${{e.tags.map(t => `<span class="tag">#${{t}}</span>`).join(' ')}}
      </div>
    </div>
  `).join('');
}}

// ── Render filters ──
function renderFilters() {{
  const filters = document.getElementById('filters');
  const statuses = [...new Set(entries.map(e => e.status))];
  const sources = [...new Set(entries.map(e => e.source))];
  const cats = [...new Set(entries.map(e => e.category))];
  const all = [{{"label":"All","value":"all"}},
    ...statuses.map(s => ({{"label":s,"value":s}})),
    ...sources.map(s => ({{"label":s,"value":s}})),
    ...cats.slice(0,6).map(c => ({{"label":c,"value":c}}))
  ];
  filters.innerHTML = all.map(f =>
    `<button class="filter-btn ${{f.value===activeFilter?'active':''}}" onclick="setFilter('${{f.value}}')">${{f.label}}</button>`
  ).join('');
}}

function setFilter(f) {{
  activeFilter = f;
  renderFilters();
  renderEntries(f);
}}

function setView(v) {{
  document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  const layout = document.querySelector('.layout');
  if (v === 'graph') {{
    layout.classList.add('graph-only');
  }} else {{
    layout.classList.remove('graph-only');
  }}
  resize();
}}

// ── Status update (calls API) ──
function updateStatus(num, newStatus) {{
  fetch(`/api/status?num=${{num}}&status=${{encodeURIComponent(newStatus)}}`, {{method: 'POST'}})
    .then(r => r.json())
    .then(d => {{
      if (d.ok) {{
        const entry = entries.find(e => e.num == num);
        if (entry) entry.status = newStatus;
        renderEntries(activeFilter);
      }}
    }})
    .catch(console.error);
}}

// ── Canvas-based force graph ──
const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');
let W, H;
let animId;
let highlightedNode = null;
let zoom = 1;
let panX = 0, panY = 0;

function zoomIn() {{ zoom = Math.min(zoom * 1.25, 5); }}
function zoomOut() {{ zoom = Math.max(zoom / 1.25, 0.2); }}
function zoomReset() {{ zoom = 1; panX = 0; panY = 0; }}

canvas.addEventListener('wheel', e => {{
  e.preventDefault();
  if (e.deltaY < 0) zoom = Math.min(zoom * 1.1, 5);
  else zoom = Math.max(zoom / 1.1, 0.2);
}}, {{passive: false}});

const groupColors = {{
  centre: '#818cf8', category: '#f59e0b', extraction: '#34d399', tag: '#60a5fa'
}};
const statusColors = {{
  backlog: '#6b7280', todo: '#3b82f6', 'in-progress': '#f59e0b', done: '#10b981', cancel: '#ef4444'
}};

// Initialise node positions
const nodeMap = {{}};
graphData.nodes.forEach((n, i) => {{
  n.x = Math.random() * 800 + 100;
  n.y = Math.random() * 600 + 100;
  n.vx = 0; n.vy = 0;
  nodeMap[n.id] = n;
}});
// Centre node in middle
if (nodeMap['megamind']) {{
  nodeMap['megamind'].x = 500;
  nodeMap['megamind'].y = 400;
  nodeMap['megamind'].fixed = true;
}}

function resize() {{
  W = canvas.parentElement.clientWidth;
  H = canvas.parentElement.clientHeight;
  canvas.width = W; canvas.height = H;
  if (nodeMap['megamind']) {{
    nodeMap['megamind'].x = W/2;
    nodeMap['megamind'].y = H/2;
  }}
}}
window.addEventListener('resize', resize);
resize();

// Simple force simulation
function simulate() {{
  const nodes = graphData.nodes;
  const links = graphData.links;
  const alpha = 0.3;

  // Repulsion between all nodes
  for (let i = 0; i < nodes.length; i++) {{
    for (let j = i+1; j < nodes.length; j++) {{
      let dx = nodes[j].x - nodes[i].x;
      let dy = nodes[j].y - nodes[i].y;
      let dist = Math.sqrt(dx*dx + dy*dy) || 1;
      let force = 800 / (dist * dist);
      let fx = dx / dist * force;
      let fy = dy / dist * force;
      if (!nodes[i].fixed) {{ nodes[i].vx -= fx * alpha; nodes[i].vy -= fy * alpha; }}
      if (!nodes[j].fixed) {{ nodes[j].vx += fx * alpha; nodes[j].vy += fy * alpha; }}
    }}
  }}

  // Attraction along links
  links.forEach(l => {{
    let s = nodeMap[l.source], t = nodeMap[l.target];
    if (!s || !t) return;
    let dx = t.x - s.x, dy = t.y - s.y;
    let dist = Math.sqrt(dx*dx + dy*dy) || 1;
    let force = (dist - 120) * 0.005;
    let fx = dx / dist * force;
    let fy = dy / dist * force;
    if (!s.fixed) {{ s.vx += fx; s.vy += fy; }}
    if (!t.fixed) {{ t.vx -= fx; t.vy -= fy; }}
  }});

  // Centre gravity
  nodes.forEach(n => {{
    if (n.fixed) return;
    n.vx += (W/2 - n.x) * 0.001;
    n.vy += (H/2 - n.y) * 0.001;
  }});

  // Apply velocities with damping
  nodes.forEach(n => {{
    if (n.fixed) return;
    n.vx *= 0.6; n.vy *= 0.6;
    n.x += n.vx; n.y += n.vy;
    n.x = Math.max(20, Math.min(W-20, n.x));
    n.y = Math.max(20, Math.min(H-20, n.y));
  }});
}}

function draw() {{
  ctx.clearRect(0, 0, W, H);
  ctx.save();
  ctx.translate(W/2 + panX, H/2 + panY);
  ctx.scale(zoom, zoom);
  ctx.translate(-W/2, -H/2);

  // Draw links
  ctx.strokeStyle = 'rgba(100,116,139,0.2)';
  ctx.lineWidth = 1;
  graphData.links.forEach(l => {{
    let s = nodeMap[l.source], t = nodeMap[l.target];
    if (!s || !t) return;
    ctx.beginPath();
    ctx.moveTo(s.x, s.y);
    ctx.lineTo(t.x, t.y);
    ctx.stroke();
  }});

  // Draw nodes
  graphData.nodes.forEach(n => {{
    let color = groupColors[n.group] || '#64748b';
    if (n.group === 'extraction' && n.status) {{
      color = statusColors[n.status] || color;
    }}
    let r = n.size / 2;
    let isHighlighted = highlightedNode === n.id;

    ctx.beginPath();
    ctx.arc(n.x, n.y, r + (isHighlighted ? 3 : 0), 0, Math.PI * 2);
    ctx.fillStyle = color;
    ctx.globalAlpha = isHighlighted ? 1 : 0.8;
    ctx.fill();
    ctx.globalAlpha = 1;

    if (isHighlighted) {{
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    }}

    // Labels
    ctx.fillStyle = 'rgba(226,232,240,0.9)';
    ctx.font = n.group === 'centre' ? 'bold 12px system-ui' : '10px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(n.label, n.x, n.y + r + 14);
  }});

  ctx.restore();
  simulate();
  animId = requestAnimationFrame(draw);
}}

function highlightNode(id) {{
  highlightedNode = id;
  setTimeout(() => {{ highlightedNode = null; }}, 3000);
}}

// ── Transform screen coords to graph coords ──
function screenToGraph(sx, sy) {{
  return {{
    x: (sx - W/2 - panX) / zoom + W/2,
    y: (sy - H/2 - panY) / zoom + H/2,
  }};
}}

// ── Mouse interaction ──
let dragNode = null;
let isPanning = false;
let lastPanX = 0, lastPanY = 0;
canvas.addEventListener('mousedown', e => {{
  const rect = canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left, sy = e.clientY - rect.top;
  const gp = screenToGraph(sx, sy);
  for (let n of graphData.nodes) {{
    let dx = n.x - gp.x, dy = n.y - gp.y;
    if (dx*dx + dy*dy < ((n.size/2 + 5) / zoom) ** 2) {{
      dragNode = n;
      dragNode.fixed = true;
      return;
    }}
  }}
  isPanning = true;
  lastPanX = e.clientX;
  lastPanY = e.clientY;
}});
canvas.addEventListener('mousemove', e => {{
  if (dragNode) {{
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    const gp = screenToGraph(sx, sy);
    dragNode.x = gp.x;
    dragNode.y = gp.y;
  }} else if (isPanning) {{
    panX += e.clientX - lastPanX;
    panY += e.clientY - lastPanY;
    lastPanX = e.clientX;
    lastPanY = e.clientY;
  }}
}});
canvas.addEventListener('mouseup', () => {{
  if (dragNode && dragNode.id !== 'megamind') dragNode.fixed = false;
  dragNode = null;
  isPanning = false;
}});

// ── Init ──
renderFilters();
renderEntries('all');
draw();
</script>
</body>
</html>"""


class DashboardHandler(SimpleHTTPRequestHandler):
    """Serve the dashboard and API endpoints."""

    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            entries = _parse_index_entries()
            budget = _load_budget()
            html = _build_html(entries, budget)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path.startswith("/api/entries"):
            entries = _parse_index_entries()
            self._json_response(entries)
        elif self.path.startswith("/api/budget"):
            self._json_response(_load_budget())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith("/api/status"):
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            num = int(params.get("num", [0])[0])
            new_status = params.get("status", [""])[0]
            if num and new_status:
                ok = update_status(num, new_status)
                self._json_response({"ok": ok})
            else:
                self._json_response({"ok": False, "error": "Missing num or status"})
        else:
            self.send_error(404)

    def _json_response(self, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # Silence request logs


def main():
    parser = argparse.ArgumentParser(description="MegaMind Dashboard")
    parser.add_argument("--port", type=int, default=DASHBOARD_PORT, help="Port (default: 8050)")
    args = parser.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), DashboardHandler)
    print(f"MegaMind Dashboard running at http://localhost:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")


if __name__ == "__main__":
    main()
