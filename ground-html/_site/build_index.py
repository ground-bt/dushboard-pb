#!/usr/bin/env python3
"""Generate index.html (the single entry page) from _site/catalog.json.

Run from the repo root:  python3 _site/build_index.py
Every path in catalog.json must exist in the repo; the script fails otherwise.
"""
import json, os, sys, html, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cat = json.load(open(os.path.join(ROOT, "_site", "catalog.json"), encoding="utf-8"))

KIND = {
    "cloud":      ("雲端即時", "開啟即讀雲端資料庫，隨時最新"),
    "cloud-edit": ("雲端可編輯", "開啟即讀雲端資料庫，網頁上可新增修改"),
    "snapshot":   ("單檔快照", "資料內嵌於檔案，截至同步日"),
    "local-edit": ("單機工具", "原檔會存回自身；GitHub 版僅供瀏覽"),
    "doc":        ("規範／手冊", "靜態文件"),
}

missing, count = [], 0
sections = []
for g in cat["groups"]:
    cards = []
    for it in g["items"]:
        p = it["path"]
        if not os.path.isfile(os.path.join(ROOT, p)):
            missing.append(p)
        count += 1
        label, title = KIND[it["kind"]]
        size = os.path.getsize(os.path.join(ROOT, p)) if os.path.isfile(os.path.join(ROOT, p)) else 0
        mb = f"{size/1048576:.1f} MB" if size >= 1048576 else f"{size/1024:.0f} KB"
        search = html.escape(" ".join([it["code"], it["name"], it["desc"], p]).lower(), quote=True)
        cards.append(f'''
      <a class="card" href="{html.escape(quote(p), quote=True)}" data-s="{search}">
        <div class="card-head"><span class="code">{html.escape(it["code"])}</span><span class="kind k-{it["kind"]}" title="{title}">{label}</span></div>
        <div class="name">{html.escape(it["name"])}</div>
        <div class="desc">{html.escape(it["desc"])}</div>
        <div class="meta">{html.escape(p)} · {mb}</div>
      </a>''')
    sections.append(f'''
  <section class="group">
    <h2>{html.escape(g["name"])}<span class="n">{len(g["items"])}</span></h2>
    <div class="grid">{"".join(cards)}
    </div>
  </section>''')

if missing:
    print("MISSING FILES:\n  " + "\n  ".join(missing), file=sys.stderr)
    sys.exit(1)

today = datetime.date.today().isoformat()
page = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(cat["title"])}</title>
<style>
  @font-face {{ font-family: "Taipei Sans TC Beta"; src: local("Taipei Sans TC Beta"), local("TaipeiSansTCBeta-Regular"); }}
  :root {{
    --blue:#7B97D3; --blue-deep:#4E6DB5; --paper:#F6F1E8; --card:#FFFFFF; --card2:#FBFAF7;
    --tint:#E7EEF8; --line:#D6DEEB; --ink:#2B2B2B; --muted:#6B6F76; --gold:#C6A15B; --red:#C8402F;
  }}
  * {{ box-sizing:border-box; }}
  html,body {{ margin:0; background:var(--paper); color:var(--ink);
    font-family:"Taipei Sans TC Beta","Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif; font-size:15px; line-height:1.6; }}
  header {{ background:var(--card); border-bottom:1px solid var(--line); position:sticky; top:0; z-index:5; }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:0 20px; }}
  .bar {{ display:flex; flex-wrap:wrap; align-items:center; gap:14px 24px; padding:14px 0; }}
  h1 {{ font-size:20px; margin:0; color:var(--blue-deep); font-weight:700; letter-spacing:.02em; }}
  h1 small {{ display:block; font-size:12px; color:var(--muted); font-weight:400; }}
  .search {{ flex:1 1 260px; max-width:460px; }}
  .search input {{ width:100%; padding:9px 12px; border:1px solid var(--line); border-radius:8px; font:inherit; background:var(--card2); color:var(--ink); }}
  .search input:focus {{ outline:2px solid var(--blue); border-color:var(--blue); }}
  .count {{ font-size:13px; color:var(--muted); white-space:nowrap; }}
  .note {{ margin:18px 0 6px; padding:12px 16px; background:var(--tint); border-left:3px solid var(--blue); border-radius:0 8px 8px 0; font-size:13.5px; color:#3b4252; }}
  .legend {{ display:flex; flex-wrap:wrap; gap:8px 14px; font-size:12.5px; color:var(--muted); margin:10px 0 4px; }}
  .legend .kind {{ margin-right:4px; }}
  .group {{ margin:26px 0 8px; }}
  h2 {{ font-size:16px; margin:0 0 12px; padding-bottom:8px; border-bottom:1px solid var(--gold); color:var(--blue-deep); display:flex; align-items:baseline; gap:10px; }}
  h2 .n {{ font-size:12px; color:var(--muted); font-weight:400; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:12px; }}
  .card {{ display:block; background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px 16px; text-decoration:none; color:inherit;
    transition:border-color .15s, box-shadow .15s, transform .15s; }}
  .card:hover {{ border-color:var(--blue); box-shadow:0 4px 14px rgba(78,109,181,.12); transform:translateY(-1px); }}
  .card-head {{ display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:4px; }}
  .code {{ font-size:12px; font-weight:700; color:var(--blue-deep); background:var(--tint); padding:2px 8px; border-radius:6px; letter-spacing:.03em; }}
  .kind {{ font-size:11.5px; padding:2px 8px; border-radius:999px; border:1px solid var(--line); color:var(--muted); background:var(--card2); white-space:nowrap; }}
  .k-cloud, .k-cloud-edit {{ color:var(--blue-deep); border-color:#B9C8EA; background:#EEF3FB; }}
  .k-local-edit {{ color:#7a5a1e; border-color:#E3CF9F; background:#FBF4E3; }}
  .name {{ font-size:15.5px; font-weight:700; margin:2px 0 4px; }}
  .desc {{ font-size:13px; color:#4a4f57; }}
  .meta {{ font-size:11.5px; color:var(--muted); margin-top:8px; word-break:break-all; }}
  .card.hide, .group.hide {{ display:none; }}
  .empty {{ display:none; text-align:center; color:var(--muted); padding:40px 0; }}
  .empty.show {{ display:block; }}
  footer {{ margin:40px 0 30px; padding-top:14px; border-top:1px solid var(--gold); font-size:12.5px; color:var(--muted); }}
  @media (max-width:600px) {{ .grid {{ grid-template-columns:1fr; }} .bar {{ padding:10px 0; }} }}
</style>
</head>
<body>
<header>
  <div class="wrap bar">
    <h1>{html.escape(cat["title"])}<small>GitHub 鏡像 · 同步日 {today}</small></h1>
    <div class="search"><input id="q" type="search" placeholder="搜尋編號、名稱、說明或路徑…" autocomplete="off"></div>
    <div class="count"><span id="shown">{count}</span> / {count} 支</div>
  </div>
</header>
<main class="wrap">
  <div class="note">{html.escape(cat["note"])}</div>
  <div class="legend">
    <span><span class="kind k-cloud">雲端即時</span>開啟即讀雲端資料庫</span>
    <span><span class="kind k-cloud-edit">雲端可編輯</span>網頁上可新增修改</span>
    <span><span class="kind">單檔快照</span>資料內嵌，截至同步日</span>
    <span><span class="kind k-local-edit">單機工具</span>原檔自存，此處僅瀏覽</span>
    <span><span class="kind">規範／手冊</span>靜態文件</span>
  </div>
  {"".join(sections)}
  <div class="empty" id="empty">沒有符合的項目</div>
</main>
<footer class="wrap">寬達生技 Ground Biotech · 入口頁由 _site/build_index.py 依 _site/catalog.json 產生；新增或搬移 HTML 後請重新執行。</footer>
<script>
(function () {{
  var q = document.getElementById('q'), shown = document.getElementById('shown'), empty = document.getElementById('empty');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.group'));
  function run() {{
    var t = q.value.trim().toLowerCase(), n = 0;
    cards.forEach(function (c) {{
      var ok = !t || c.getAttribute('data-s').indexOf(t) !== -1;
      c.classList.toggle('hide', !ok); if (ok) n++;
    }});
    groups.forEach(function (g) {{
      g.classList.toggle('hide', g.querySelectorAll('.card:not(.hide)').length === 0);
    }});
    shown.textContent = n; empty.classList.toggle('show', n === 0);
  }}
  q.addEventListener('input', run);
  if (location.hash.length > 1) {{ q.value = decodeURIComponent(location.hash.slice(1)); run(); }}
}})();
</script>
</body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
print(f"index.html written: {count} items, {len(cat['groups'])} groups")
