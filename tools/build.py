# -*- coding: utf-8 -*-
"""
月光書房 — static site builder.
Reads tools/manifest.json + tools/data/story-XX.md (+ _about.md, _connections.md)
and emits the publishable GitHub Pages site (index.html, about.html,
connections.html, stories/XX.html, assets are static).
"""
import json
import html
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "data"
STORIES_DIR = ROOT / "stories"
STORIES_DIR.mkdir(exist_ok=True)

KANJI = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
         "十一", "十二", "十三", "十四", "十五"]

MOTIFS = [
    ("ミラ彗星", ["ミラ彗星", "彗星", "箒星", "ほうき星"]),
    ("月光堂のマッチ", ["月光堂", "マッチ"]),
    ("子守唄", ["子守唄", "眠れ、眠れ", "眠れ眠れ"]),
    ("月光書房", ["月光書房"]),
    ("片方の手袋", ["手袋", "手甲"]),
]

CHARS_PER_PAGE = 620  # rough 文庫本 page


def esc(s):
    return html.escape(s, quote=True)


def body_char_count(body):
    # count Japanese/content characters, ignoring whitespace and structural marks
    t = re.sub(r"\s+", "", body)
    t = t.replace("*", "").replace("#", "")
    return len(t)


def md_to_html(body, prose_class="prose"):
    """Tiny converter: blank-line blocks -> <p>; '* * *' -> scene divider; '## ' -> h2."""
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
    found = []
    for name, keys in MOTIFS:
        if any(k in body for k in keys):
            found.append(name)
    return found


def head(title, depth, extra_desc=""):
    base = "../" if depth else ""
    desc = extra_desc or "彗星の夜にだけ現れる古書店『月光書房』から借り受けた、十二編の物語集。"
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


def topbar(depth, with_tategaki=False):
    base = "../" if depth else ""
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


def foot(depth):
    base = "../" if depth else ""
    return f"""<footer class="site-foot">
  <div>月光書房  — 十二夜の物語集</div>
  <div style="margin-top:.6rem"><a href="{base}index.html">目次</a>　<a href="{base}about.html">この本について</a>　<a href="{base}connections.html">符牒について</a></div>
</footer>
<script src="{base}assets/app.js"></script>
</body>
</html>
"""


def build_index(man, stories):
    cards = []
    for s in stories:
        num = int(s["num"])
        pages = max(24, round(s["_chars"] / CHARS_PER_PAGE))
        cards.append(f"""    <a class="card" href="stories/{s['num']}.html">
      <div class="no">第{KANJI[num]}話</div>
      <h3 class="ttl">{esc(s['title'])}</h3>
      <span class="genre">{esc(s['genre'])}</span>
      <p class="blurb">{esc(s['blurb'])}</p>
      <div class="meta"><span class="author">{esc(s['pseudonym'])}</span><span>約{pages}頁</span></div>
    </a>""")
    comet_svg = """<svg class="comet" viewBox="0 0 1200 420" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
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
    about_html = md_to_html(read_md("_about.md"), "lead-prose")
    # use only the first two paragraphs of the frame as the index lead
    lead_para = read_md("_about.md").strip().split("\n\n")
    lead = lead_para[0]
    body = f"""{topbar(0)}
<section class="hero">
  {comet_svg}
  <div class="kicker">十二夜の物語集</div>
  <h1>月光書房</h1>
  <p class="sub">げっこうしょぼう</p>
  <p class="lead">{esc(lead)}<span class="signoff">― 借り受けた者より</span></p>
  <div class="index-nav"><a href="about.html">この本について</a><a href="connections.html">十二をつなぐ符牒</a></div>
</section>
<main class="wrap">
  <div class="section-label">目次 ・ 十二の物語</div>
  <div class="grid">
{chr(10).join(cards)}
  </div>
</main>
{foot(0)}"""
    write_html(ROOT / "index.html", head(man["title"] + " — 十二夜の物語集", 0) + body)


def build_prose_page(filename, title, md_name, depth=0, extra_html=""):
    body_html = md_to_html(read_md(md_name), "page-prose")
    inner = f"""{topbar(depth)}
<main class="page">
  <div class="eyebrow">月光書房</div>
  <h1>{esc(title)}</h1>
  {body_html}
  {extra_html}
  <div class="backhome"><a href="{'../' if depth else ''}index.html">← 目次へもどる</a></div>
</main>
{foot(depth)}"""
    write_html(ROOT / filename, head(title + " — 月光書房", depth) + inner)


def build_connections(stories):
    # motif matrix
    header_cells = "".join(f"<th>{esc(name)}</th>" for name, _ in MOTIFS)
    rows = []
    for s in stories:
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
    build_prose_page("connections.html", "十二をつなぐ符牒", "_connections.md", depth=0, extra_html=table)


def build_story(s, prev_s, next_s):
    num = int(s["num"])
    body = read_md(f"story-{s['num']}.md")
    prose = md_to_html(body, "prose")
    pages = max(24, round(s["_chars"] / CHARS_PER_PAGE))
    motif_items = "".join(f"<li>{esc(m)}</li>" for m in s["_motifs"])

    if prev_s:
        prev_html = f'<a class="prev" href="{prev_s["num"]}.html"><span class="label">前の物語</span><span class="t">{esc(prev_s["title"])}</span></a>'
    else:
        prev_html = '<span class="prev disabled"><span class="label">前の物語</span><span class="t">—</span></span>'
    if next_s:
        next_html = f'<a class="next" href="{next_s["num"]}.html"><span class="label">次の物語</span><span class="t">{esc(next_s["title"])}</span></a>'
    else:
        next_html = '<span class="next disabled"><span class="label">次の物語</span><span class="t">—</span></span>'

    inner = f"""{topbar(1, with_tategaki=True)}
<main>
  <article class="reader">
    <div class="story-no">第 {KANJI[num]} 話</div>
    <h1 class="story-title">{esc(s['title'])}</h1>
    <div class="story-by">{esc(s['pseudonym'])}</div>
    <div class="story-genre">{esc(s['genre'])} ・ 約{pages}頁</div>
    <hr class="rule">
    {prose}
  </article>
  <div class="story-foot">
    <details class="charm">
      <summary>この物語にひそむ符牒</summary>
      <p>ほかの十一編と、ひそかに分かち合っているもの：</p>
      <ul>{motif_items}</ul>
      <p><a href="../connections.html" style="color:var(--comet)">十二をつなぐ符牒について →</a></p>
    </details>
  </div>
  <nav class="pager">{prev_html}{next_html}</nav>
  <div class="backhome"><a href="../index.html">← 目次へもどる</a></div>
</main>
{foot(1)}"""
    write_html(STORIES_DIR / f"{s['num']}.html", head(f"{s['title']} — 月光書房", 1) + inner)


def read_md(name):
    return (DATA / name).read_text(encoding="utf-8")


def write_html(path, content):
    path.write_text(content, encoding="utf-8", newline="\n")


def main():
    man = json.loads((ROOT / "tools" / "manifest.json").read_text(encoding="utf-8"))
    stories = sorted(man["stories"], key=lambda x: x["num"])
    for s in stories:
        body = read_md(f"story-{s['num']}.md")
        s["_chars"] = body_char_count(body)
        s["_motifs"] = detect_motifs(body)

    build_index(man, stories)
    build_prose_page("about.html", "この本について", "_about.md", depth=0)
    build_connections(stories)
    for i, s in enumerate(stories):
        prev_s = stories[i - 1] if i > 0 else None
        next_s = stories[i + 1] if i < len(stories) - 1 else None
        build_story(s, prev_s, next_s)

    total = sum(s["_chars"] for s in stories)
    print(f"built {len(stories)} stories, {total:,} chars total")
    for s in stories:
        pages = max(24, round(s["_chars"] / CHARS_PER_PAGE))
        flag = "" if s["_chars"] >= 15000 else "  <-- SHORT"
        print(f"  {s['num']} {s['title'][:24]:<26} {s['_chars']:>7,} chars  ~{pages}p  motifs={len(s['_motifs'])}{flag}")


if __name__ == "__main__":
    main()
