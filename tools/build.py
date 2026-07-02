# -*- coding: utf-8 -*-
"""
月光書房 — static site builder (multi-volume + portal).

Reads tools/site.json + tools/data/<volume-id>/story-XX.md (+ _about.md,
_connections.md per volume) and emits the publishable GitHub Pages site:

  /index.html                  … portal (両夜集の入口)
  /<vol>/index.html            … volume table of contents
  /<vol>/about.html            … この巻について
  /<vol>/connections.html      … 符牒について（早見表つき）
  /<vol>/stories/XX.html       … each story
  /assets/...                  … shared (static)
"""
import json
import html
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "data"

KANJI = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
         "十一", "十二", "十三", "十四", "十五"]

MOTIFS = [
    ("ミラ彗星", ["ミラ彗星", "彗星", "箒星", "ほうき星"]),
    ("月光堂のマッチ", ["月光堂", "マッチ"]),
    ("子守唄", ["子守唄", "子守歌", "眠れ、眠れ", "眠れ眠れ"]),
    ("月光書房", ["月光書房"]),
    ("片方の手袋", ["手袋", "手甲"]),
]

CHARS_PER_PAGE = 620  # rough 文庫本 page

COMET_SVG = """<svg class="comet" viewBox="0 0 1200 420" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="tail" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#9cc4ee" stop-opacity="0"/>
      <stop offset="1" stop-color="#9cc4ee" stop-opacity="0.9"/>
    </linearGradient>
    <radialGradient id="star"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#9cc4ee" stop-opacity="0"/></radialGradient>
  </defs>
  <g opacity="0.9">
    <line x1="120" y1="60" x2="930" y2="300" stroke="url(#tail)" stroke-width="2.4"/>
    <circle cx="930" cy="300" r="5.5" fill="#fff"/>
    <circle cx="930" cy="300" r="20" fill="url(#star)"/>
  </g>
  <g fill="#cdd8ee">
    <circle cx="200" cy="120" r="1.1"/><circle cx="340" cy="70" r="0.9"/><circle cx="520" cy="150" r="1.2"/>
    <circle cx="680" cy="90" r="0.8"/><circle cx="1040" cy="120" r="1.1"/><circle cx="1100" cy="240" r="0.9"/>
    <circle cx="260" cy="260" r="0.8"/><circle cx="440" cy="300" r="1.0"/><circle cx="760" cy="260" r="0.9"/>
  </g>
</svg>"""


def esc(s):
    return html.escape(str(s), quote=True)


def body_char_count(body):
    t = re.sub(r"\s+", "", body)
    t = t.replace("*", "").replace("#", "")
    return len(t)


def md_to_html(body, prose_class="prose"):
    blocks = re.split(r"\n[ \t]*\n", body.strip())
    out = []
    for raw in blocks:
        block = raw.strip("\n")
        flat = block.strip()
        if not flat:
            continue
        if re.fullmatch(r"[*＊]\s*[*＊]\s*[*＊]", flat) or flat in ("***", "* * *"):
            out.append('<p class="scene" aria-hidden="true"></p>')
            continue
        if flat.startswith("## "):
            out.append(f"<h2>{esc(flat[3:].strip())}</h2>")
            continue
        if flat.startswith("# "):
            out.append(f"<h2>{esc(flat[2:].strip())}</h2>")
            continue
        lines = [esc(ln.strip()) for ln in block.split("\n") if ln.strip()]
        out.append("<p>" + "<br>".join(lines) + "</p>")
    return f'<div class="{prose_class}">\n' + "\n".join(out) + "\n</div>"


def detect_motifs(body):
    return [name for name, keys in MOTIFS if any(k in body for k in keys)]


def read_md(rel):
    return (DATA / rel).read_text(encoding="utf-8")


def write_html(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def head(title, base, desc=""):
    desc = desc or "彗星の夜にだけ現れる古書店『月光書房』── 一日の十二刻・百四十四編からなる日本語短編集（AIによる創作）。"
    return f"""<!doctype html>
<html lang="ja" data-theme="night">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;500;600&family=Noto+Sans+JP:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
"""


def topbar(base, with_tategaki=False):
    tg = '<button class="btn" data-action="tategaki" aria-pressed="false">縦書き</button>' if with_tategaki else ""
    return f"""<header class="topbar">
  <a class="brand" href="{base}index.html"><b>月光</b>書房</a>
  <div class="controls">
    <button class="btn" data-action="fs-down" aria-label="文字を小さく">A−</button>
    <button class="btn" data-action="fs-up" aria-label="文字を大きく">A＋</button>
    {tg}
    <button class="btn" data-action="theme" aria-pressed="false">☀ 紙</button>
  </div>
</header>
"""


def foot(base, volumes):
    return f"""<footer class="site-foot">
  <div>月光書房 — 十二刻、百四十四の物語</div>
  <div style="margin-top:.6rem"><a href="{base}index.html">入口</a>　<a href="{base}about.html">この本について</a></div>
  <p class="disclaimer">本作品はすべてAI（Claude）によって生成された創作です。作中の人物・団体・地名・出来事、および著者として記した名前はすべて架空であり、実在するいかなる人物・団体・事件とも一切関係ありません。</p>
</footer>
<script src="{base}assets/app.js"></script>
</body>
</html>
"""


def load_story(vol, s):
    body = read_md(f"{vol['id']}/story-{s['num']}.md")
    s["_body"] = body
    s["_chars"] = body_char_count(body)
    s["_motifs"] = detect_motifs(body)
    s["_pages"] = max(24, round(s["_chars"] / CHARS_PER_PAGE))
    return s


def story_card(vol, s):
    num = int(s["num"])
    pov = f'<span class="pov">{esc(s["pov"])}</span>' if s.get("pov") else ""
    return f"""    <a class="card" href="stories/{s['num']}.html">
      <div class="no">第{KANJI[num]}話</div>
      <h3 class="ttl">{esc(s['title'])}</h3>
      <span class="genre">{esc(s['genre'])}</span>{pov}
      <p class="blurb">{esc(s['blurb'])}</p>
      <div class="meta"><span class="author">{esc(s['pseudonym'])}</span><span>約{s['_pages']}頁</span></div>
    </a>"""


def build_volume_index(vol, other, volumes):
    base = "../"
    cards = "\n".join(story_card(vol, s) for s in vol["stories"])
    other_link = (
        f'<a href="../{other["id"]}/index.html">{esc(other["label"])}『{esc(other["title"])}』へ →</a>'
        if other else ""
    )
    body = f"""{topbar(base)}
<section class="hero hero-vol">
  {COMET_SVG}
  <div class="kicker">{esc(vol['label'])} ・ {esc(vol.get('axis',''))}</div>
  <h1>{esc(vol['title'])}</h1>
  <p class="lead">{esc(vol['subtitle'])}</p>
  <div class="index-nav"><a href="about.html">この巻について</a><a href="connections.html">十二をつなぐ符牒</a>{other_link}</div>
</section>
<main class="wrap">
  <div class="section-label">目次 ・ 十二の物語</div>
  <div class="grid">
{cards}
  </div>
  <div class="backhome"><a href="../index.html">← 月光書房の入口へ</a></div>
</main>
{foot(base, volumes)}"""
    write_html(ROOT / vol["id"] / "index.html",
               head(f"{vol['title']} — 月光書房 {vol['label']}", base, vol["subtitle"]) + body)


def build_volume_about(vol, volumes):
    base = "../"
    ap = DATA / vol["id"] / "_about.md"
    about_md = ap.read_text(encoding="utf-8") if ap.exists() else vol.get("subtitle", "")
    body_html = md_to_html(about_md, "page-prose")
    inner = f"""{topbar(base)}
<main class="page">
  <div class="eyebrow">月光書房 ・ {esc(vol['label'])}</div>
  <h1>この巻について</h1>
  {body_html}
  <div class="backhome"><a href="index.html">← 『{esc(vol['title'])}』目次へ</a></div>
</main>
{foot(base, volumes)}"""
    write_html(ROOT / vol["id"] / "about.html",
               head(f"この巻について — {vol['title']}", base) + inner)


def build_volume_connections(vol, volumes):
    base = "../"
    header_cells = "".join(f"<th>{esc(name)}</th>" for name, _ in MOTIFS)
    rows = []
    for s in vol["stories"]:
        num = int(s["num"])
        cells = []
        for name, _ in MOTIFS:
            mark = '<span class="dot">●</span>' if name in s["_motifs"] else '<span style="opacity:.25">·</span>'
            cells.append(f"<td>{mark}</td>")
        rows.append(
            f'<tr><td class="motif-name"><a href="stories/{s["num"]}.html">第{KANJI[num]}話　{esc(s["title"])}</a></td>{"".join(cells)}</tr>'
        )
    table = f"""<table class="motif-table">
  <tr><th>物語</th>{header_cells}</tr>
  {''.join(rows)}
</table>"""
    cp = DATA / vol["id"] / "_connections.md"
    conn_md = cp.read_text(encoding="utf-8") if cp.exists() else read_md("_connections_default.md")
    body_html = md_to_html(conn_md, "page-prose")
    inner = f"""{topbar(base)}
<main class="page">
  <div class="eyebrow">月光書房 ・ {esc(vol['label'])}</div>
  <h1>十二をつなぐ符牒</h1>
  {body_html}
  {table}
  <div class="backhome"><a href="index.html">← 『{esc(vol['title'])}』目次へ</a></div>
</main>
{foot(base, volumes)}"""
    write_html(ROOT / vol["id"] / "connections.html",
               head(f"十二をつなぐ符牒 — {vol['title']}", base) + inner)


def build_story(vol, s, prev_s, next_s, volumes):
    base = "../../"
    num = int(s["num"])
    prose = md_to_html(s["_body"], "prose")
    motif_items = "".join(f"<li>{esc(m)}</li>" for m in s["_motifs"])
    pov_line = f' ・ {esc(s["pov"])}' if s.get("pov") else ""

    if prev_s:
        prev_html = f'<a class="prev" href="{prev_s["num"]}.html"><span class="label">前の物語</span><span class="t">{esc(prev_s["title"])}</span></a>'
    else:
        prev_html = '<span class="prev disabled"><span class="label">前の物語</span><span class="t">—</span></span>'
    if next_s:
        next_html = f'<a class="next" href="{next_s["num"]}.html"><span class="label">次の物語</span><span class="t">{esc(next_s["title"])}</span></a>'
    else:
        next_html = '<span class="next disabled"><span class="label">次の物語</span><span class="t">—</span></span>'

    inner = f"""{topbar(base, with_tategaki=True)}
<main>
  <article class="reader">
    <div class="story-no">{esc(vol['label'])} ・ 第 {KANJI[num]} 話</div>
    <h1 class="story-title">{esc(s['title'])}</h1>
    <div class="story-by">{esc(s['pseudonym'])}</div>
    <div class="story-genre">{esc(s['genre'])}{pov_line} ・ 約{s['_pages']}頁</div>
    <hr class="rule">
    {prose}
  </article>
  <div class="story-foot">
    <details class="charm">
      <summary>この物語にひそむ符牒</summary>
      <p>ほかの物語と、ひそかに分かち合っているもの：</p>
      <ul>{motif_items}</ul>
      <p><a href="../connections.html" style="color:var(--comet)">十二をつなぐ符牒について →</a></p>
    </details>
  </div>
  <nav class="pager">{prev_html}{next_html}</nav>
  <div class="backhome"><a href="../index.html">← 『{esc(vol['title'])}』目次へ</a></div>
</main>
{foot(base, volumes)}"""
    write_html(ROOT / vol["id"] / "stories" / f"{s['num']}.html",
               head(f"{s['title']} — 月光書房", base) + inner)


def build_portal(site):
    base = ""
    vol_cards = []
    for v in sorted(site["volumes"], key=lambda x: x.get("cycle", 999)):
        titles = "".join(
            f'<li><span class="li-no">{KANJI[int(s["num"])]}</span>{esc(s["title"])}</li>'
            for s in v["stories"]
        )
        vol_cards.append(f"""    <a class="vol-card" href="{v['id']}/index.html">
      <div class="vol-label">{esc(v['label'])}</div>
      <h2 class="vol-title">{esc(v['title'])}</h2>
      <div class="vol-axis">{esc(v.get('axis',''))}</div>
      <p class="vol-sub">{esc(v['subtitle'])}</p>
      <ul class="vol-toc">{titles}</ul>
      <span class="vol-enter">十二編を読む →</span>
    </a>""")
    intro = read_md("_portal.md").strip().split("\n\n")[0]
    body = f"""{topbar(base)}
<section class="hero">
  {COMET_SVG}
  <div class="kicker">{esc(site.get('tagline','十二刻の物語'))}</div>
  <h1>月光書房</h1>
  <p class="sub">げっこうしょぼう</p>
  <p class="lead">{esc(intro)}</p>
</section>
<main class="wrap">
  <div class="section-label">二つの夜集</div>
  <div class="vol-grid">
{chr(10).join(vol_cards)}
  </div>
  <div class="index-nav" style="margin-top:2.4rem"><a href="about.html">月光書房について</a></div>
</main>
{foot(base, site['volumes'])}"""
    write_html(ROOT / "index.html", head(f"{site['title']} — {site.get('tagline','')}", base) + body)


def build_portal_about(site):
    base = ""
    body_html = md_to_html(read_md("_about.md"), "page-prose")
    inner = f"""{topbar(base)}
<main class="page">
  <div class="eyebrow">月光書房</div>
  <h1>月光書房について</h1>
  {body_html}
  <div class="backhome"><a href="index.html">← 入口へもどる</a></div>
</main>
{foot(base, site['volumes'])}"""
    write_html(ROOT / "about.html", head("月光書房について", base) + inner)


def main():
    site = json.loads((ROOT / "tools" / "site.json").read_text(encoding="utf-8"))
    volumes = site["volumes"]

    for vol in volumes:
        vol["stories"] = sorted(vol["stories"], key=lambda x: x["num"])
        for s in vol["stories"]:
            load_story(vol, s)

    build_portal(site)
    build_portal_about(site)
    for i, vol in enumerate(volumes):
        other = None
        build_volume_index(vol, other, volumes)
        build_volume_about(vol, volumes)
        build_volume_connections(vol, volumes)
        sts = vol["stories"]
        for j, s in enumerate(sts):
            build_story(vol, s, sts[j - 1] if j > 0 else None,
                        sts[j + 1] if j < len(sts) - 1 else None, volumes)

    grand = 0
    for vol in volumes:
        total = sum(s["_chars"] for s in vol["stories"])
        grand += total
        print(f"[{vol['id']}] {vol['title']} — {total:,} chars")
        for s in vol["stories"]:
            flag = "" if s["_chars"] >= 15000 else "  <-- SHORT"
            print(f"  {s['num']} {s['title'][:22]:<24} {s['_chars']:>7,}  ~{s['_pages']}p  motifs={len(s['_motifs'])}{flag}")
    print(f"= grand total: {grand:,} chars across {sum(len(v['stories']) for v in volumes)} stories")


if __name__ == "__main__":
    main()
