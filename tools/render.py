"""Build the site and the downloads from the files in text/.

    python3 tools/render.py            # site, Markdown, Word and PDF
    python3 tools/render.py --no-pdf   # skip the PDF (no Playwright needed)

Writes:
  site/index.html, share.html, source-list.html, 404.html
  site/source-copies/         saved copies of every source, with fingerprints.json
  site/downloads/             guide as PDF, Word and Markdown; summary and source list as Markdown
Needs: Python 3 with PyYAML, pandoc (Word), Node with Playwright (PDF).
"""

import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import content  # noqa: E402

PUBLIC = os.path.join(ROOT, "site")
BUILD = os.path.join(ROOT, "build")
DOWNLOADS = "downloads"
GUIDE = "digital-assets-framework-guide"
FILES = {
    "pdf": f"{DOWNLOADS}/{GUIDE}.pdf",
    "docx": f"{DOWNLOADS}/{GUIDE}.docx",
    "md": f"{DOWNLOADS}/{GUIDE}.md",
    "summary": f"{DOWNLOADS}/community-summary.md",
    "sources": f"{DOWNLOADS}/source-list.md",
}
KIND_TITLES = [
    ("law", "The Act"),
    ("government", "Government"),
    ("asic", "ASIC"),
    ("redbelly", "Redbelly Network"),
    ("tokeniser", "Tokeniser"),
    ("task", "The task brief"),
]
STATUS = {
    "ok": ("s-ok", "Lines up"),
    "part": ("s-part", "Partly"),
    "gap": ("s-gap", "Not covered"),
    "open": ("s-open", "Not settled"),
}

WORD = False  # building the Word version of the document
D = None  # loaded content
EV = None  # evidence by id
SRC = None  # sources by id


# ------------------------------------------------------------------ text

def smart(text):
    text = re.sub(r"(?<=\w)'(?=\w)", "\u2019", text)
    text = re.sub(r"(?<=[\w.,!?])'", "\u2019", text)
    text = re.sub(r"'(?=\w)", "\u2018", text)
    text = re.sub(r'(^|[\s(\[\u2014])"', "\\1\u201c", text)
    text = text.replace('"', "\u201d")
    return text


def esc(text):
    return html.escape(text, quote=True)


TOKEN = re.compile(r"\s*\{\{([a-z0-9 -]+)\}\}|\[([^\]]+)\]\(([^)\s]+)\)|\*\*(.+?)\*\*")


def group_by_source(ids):
    groups = []
    for eid in ids:
        n = SRC[EV[eid]["source"]]["n"]
        for g in groups:
            if g[0] == n:
                g[1].append(eid)
                break
        else:
            groups.append((n, [eid]))
    return sorted(groups, key=lambda g: g[0])


def inline(text, mode="web"):
    """Render inline markup. mode: web | doc | md | plain."""
    text = re.sub(r"\s+", " ", text).strip()
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(_plain(text[pos:m.start()], mode))
        if m.group(1):
            out.append(_cite(m.group(1).split(), mode))
        elif m.group(2):
            label = _plain(m.group(2), mode)
            href = m.group(3)
            if mode == "md":
                out.append(f"[{label}]({href})")
            elif mode == "plain":
                out.append(label)
            else:
                if mode == "doc" and not href.startswith("http"):
                    href = D["explainer"]["site_url"] + "/" + href
                out.append(f'<a href="{esc(href)}">{label}</a>')
        else:
            inner = _plain(m.group(4), mode)
            out.append({"md": f"**{inner}**", "plain": inner}.get(mode, f"<strong>{inner}</strong>"))
        pos = m.end()
    out.append(_plain(text[pos:], mode))
    return "".join(out)


def _plain(text, mode):
    text = smart(text)
    return text if mode in ("md", "plain") else esc(text)


def _cite(ids, mode):
    groups = group_by_source(ids)
    if mode == "plain":
        return ""
    if mode == "md":
        return " " + "".join(f"[{n}]" for n, _ in groups)
    if mode == "doc":
        return '<sup class="c">[' + ", ".join(str(n) for n, _ in groups) + "]</sup>"
    parts = []
    for n, evs in groups:
        src = D["sources"][n - 1]
        parts.append(
            f'<a class="cite" href="source-list.html#e-{evs[0]}" data-ev="{" ".join(evs)}" '
            f'aria-expanded="false" aria-label="Source {n}, {esc(src["publisher"])}: show the exact words">{n}</a>'
        )
    return "".join(parts)


def copy_name(src):
    """Saved copy of a source, relative to source-copies/ (see tools/save_sources.py)."""
    return f"pages/{src['n']:02d}-{src['id']}.txt"


def para(text, mode="web"):
    return f"<p>{inline(text, mode)}</p>"


# ------------------------------------------------------------------ web pages

def head(title, desc, path):
    site = D["explainer"]["site_url"]
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{site}/{path}">
<meta property="og:image" content="{site}/assets/img/social-card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/touch-icon-180.png">
<link rel="stylesheet" href="assets/guide.css">
<script>try{{var t=localStorage.getItem("daf-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>"""


def topbar(current):
    links = [("index.html", "Guide"), ("share.html", "Short version"), ("source-list.html", "Sources")]
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in links
    )
    return f"""<header class="bar"><div class="bar-in">
<a class="brand" href="index.html"><img src="assets/img/logo-dark-bg.png" alt="Redbelly DAO" width="43" height="30"><span>Digital Assets Framework Act</span></a>
<nav class="nav" aria-label="Pages">{nav}</nav>
<button class="theme" type="button" aria-label="Switch colour theme">Dark</button>
</div></header>"""


def footer():
    ex = D["explainer"]
    return f"""<footer class="foot"><div class="foot-in">
<div><img src="assets/img/logo-dark-bg.png" alt="Redbelly DAO" width="48" height="34">
<p><strong>General information, not legal advice.</strong> A reading of a new law and the public papers around it. Whether a particular business needs a licence is a question for its own advisers, and nothing here vouches for the licensing or compliance status of Redbelly, Tokeniser or any issuer.</p>
<p class="mono">Sources checked {esc(ex["checked"])}</p></div>
<div><h2>Take a copy</h2><ul>
<li><a href="{FILES["pdf"]}">Guide (PDF)</a></li>
<li><a href="{FILES["docx"]}">Guide (Word)</a></li>
<li><a href="{FILES["md"]}">Guide (Markdown)</a></li>
<li><a href="{FILES["summary"]}">Community summary (Markdown)</a></li>
<li><a href="{FILES["sources"]}">Source list (Markdown)</a></li></ul></div>
<div><h2>Check the evidence</h2><ul>
<li><a href="source-list.html">Every source and passage</a></li>
<li><a href="source-copies/fingerprints.json">Saved copies with SHA-256</a></li></ul></div>
</div></footer>"""


def evidence_json():
    used = set()
    for _, ids in content.citations(D):
        used.update(ids)
    payload = {
        "evidence": {e["id"]: {"s": SRC[e["source"]]["n"], "q": e["quote"], "at": e["at"]} for e in D["evidence"] if e["id"] in used},
        "sources": {s["n"]: {"title": s["title"], "publisher": s["publisher"], "url": s["url"], "file": copy_name(s)} for s in D["sources"]},
    }
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/json" id="evidence-data">{text}</script>'


def page(title, desc, path, current, body, with_evidence=False):
    parts = [head(title, desc, path), topbar(current), body, footer()]
    if with_evidence:
        parts.append(evidence_json())
    parts.append('<script src="assets/guide.js" defer></script>\n</body>\n</html>\n')
    return "\n".join(parts)


def table_html(tbl, cls, mode="web", statuses=None):
    headers = tbl["head"]
    rows = []
    for i, row in enumerate(tbl["rows"]):
        cells = []
        for j, cell in enumerate(row):
            body = inline(cell, mode)
            if statuses and j == len(row) - 1 and mode == "web":
                key = statuses[i]
                klass, label = STATUS[key]
                body = f'<span class="status {klass}">{label}</span><br>' + inline(re.sub(r"^\*\*[^*]+\*\*\s*", "", cell), mode)
            mono = ' class="mono"' if cls == "terms" and j == 2 else ""
            cells.append(f'<td data-h="{esc(headers[j])}"{mono}>{body}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    head_html = "".join(f"<th scope=\"col\">{esc(smart(h))}</th>" for h in headers)
    return (
        f'<div class="table"><table class="{cls}"><caption>{esc(smart(tbl["caption"]))}</caption>'
        f"<thead><tr>{head_html}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
    )


def timeline_html(items, checked):
    out, marked = [], False
    for item in items:
        if item["state"] != "past" and not marked:
            out.append(f'<li class="today"><span>Sources checked {esc(checked)}</span></li>')
            marked = True
        cls = item["state"] + (" key" if item.get("key") else "")
        out.append(f'<li class="{cls}"><time>{esc(item["date"])}</time><span class="what">{inline(item["text"])}</span></li>')
    return '<ol class="when">' + "".join(out) + "</ol>"


def panel(kind, label, inner):
    return f'<div class="panel panel-{kind}"><h3 class="label">{label}</h3>{inner}</div>'


def chapter_html(sec, num):
    out = [f'<section class="chapter" id="{sec["id"]}" aria-labelledby="{sec["id"]}-h">']
    out.append(f'<p class="chapter-num">{num:02d}</p><h2 id="{sec["id"]}-h">{esc(smart(sec["title"]))}</h2>')
    if sec.get("lede"):
        out.append(f'<p class="lede">{inline(sec["lede"])}</p>')
    law = "".join(para(t) for t in sec.get("law", []))
    if "law_table" in sec:
        law += table_html(sec["law_table"], "terms")
    if "timeline" in sec:
        law = timeline_html(sec["timeline"], D["explainer"]["checked"]) + law
    if law:
        out.append(panel("law", "What the law says", law))
    if "callout" in sec:
        c = sec["callout"]
        out.append(f'<div class="callout"><h3>{esc(c["title"])}</h3>' + "".join(para(t) for t in c["paragraphs"]) + "</div>")
    if "steps" in sec:
        st = sec["steps"]
        items = "".join(f"<li>{inline(t)}</li>" for t in st["items"])
        out.append(panel("law", esc(st["title"]), f'<ol class="steps">{items}</ol><p class="small">{inline(st["note"])}</p>'))
    if "companies" in sec:
        out.append(panel("co", "What the companies say", "".join(para(t) for t in sec["companies"])))
    if "fit_table" in sec:
        out.append(table_html(sec["fit_table"], "fit", statuses=sec["fit_table"]["status"]))
    meaning = ""
    if sec["id"] == "open":
        meaning = '<ul class="plain">' + "".join(f"<li>{inline(t)}</li>" for t in sec["meaning"]) + "</ul>"
    else:
        meaning = "".join(para(t) for t in sec.get("meaning", []))
    if "meaning_table" in sec:
        meaning += table_html(sec["meaning_table"], "roles")
    if "checklist" in sec:
        cl = sec["checklist"]
        meaning += f'<p><strong>{esc(cl["title"])}</strong></p><ul class="checks">' + "".join(f"<li>{inline(t)}</li>" for t in cl["items"]) + "</ul>"
    if meaning:
        out.append(panel("mean", "What this means", meaning))
    if sec.get("unsettled"):
        out.append(panel("open", "Not settled", "".join(para(t) for t in sec["unsettled"])))
    out.append("</section>")
    return "\n".join(out)


def index_page():
    ex = D["explainer"]
    n_src = len(D["sources"])
    n_ev = len(D["evidence"])
    facts = "".join(f"<li><b>{esc(k['date'])}</b>{inline(k['label'])}</li>" for k in ex["key_dates"])
    toc = '<li><a href="#short"><span class="n">00</span><span>The short version</span></a></li>' + "".join(
        f'<li><a href="#{s["id"]}"><span class="n">{i:02d}</span><span>{esc(smart(s["title"]))}</span></a></li>'
        for i, s in enumerate(ex["sections"], 1)
    )
    short = "".join(f"<li><h3>{esc(smart(q['q']))}</h3><p>{inline(q['a'])}</p></li>" for q in ex["short"])
    chapters = "\n".join(chapter_html(s, i) for i, s in enumerate(ex["sections"], 1))
    body = f"""<section class="hero"><div class="hero-in">
<p class="eyebrow"><b>&#9632;</b> Plain-language explainer &middot; Redbelly DAO research</p>
<h1>{esc(smart(ex["title"]))}</h1>
<p class="sub">{esc(smart(ex["subtitle"]))}</p>
<ul class="facts">{facts}</ul>
<div class="actions"><a class="btn btn-fill" href="{FILES["pdf"]}" download>Download the PDF</a><a class="btn btn-line" href="{FILES["docx"]}" download>Word</a><a class="btn btn-line" href="share.html">Short version to share</a></div>
</div></section>
<div class="wrap cols">
<nav class="toc" aria-label="Contents"><p class="label toc-h">Contents</p><ol>{toc}</ol>
<p class="small" style="margin:20px 0 0 12px">{n_src} sources &middot; {n_ev} quoted passages<br>Checked {esc(ex["checked"])}</p></nav>
<main id="main" class="read" tabindex="-1">
<div class="notice" role="note"><span class="label">Read this first</span><p>{inline(ex["notice"])}</p></div>
<section class="short" id="short" aria-labelledby="short-h"><p class="chapter-num">00</p><h2 id="short-h">The short version</h2>
<p class="lede">Five questions, answered in a sentence or two. The numbered markers open the exact words each answer rests on.</p>
<ul class="qa">{short}</ul></section>
{chapters}
</main></div>"""
    desc = "A plain-language explainer of Australia's Digital Assets Framework Act: which businesses need a licence, the key dates, what it means for issuers, and how Redbelly and Tokeniser measure up. General information, not legal advice."
    return page(ex["title"] + " | Redbelly DAO research", desc, "", "index.html", body, with_evidence=True)


def summary_page():
    sm = D["summary"]
    site = D["explainer"]["site_url"]
    paras = "".join(para(t) for t in sm["paragraphs"])
    plain = "\n\n".join(inline(t, "plain") for t in sm["paragraphs"])
    posts = []
    for i, p in enumerate(thread(), 1):
        n = content.x_length(p)
        intent = "https://x.com/intent/post?text=" + __import__("urllib.parse").parse.quote(p)
        posts.append(
            f'<li class="post"><p id="post-{i}">{esc(p)}</p><div class="post-meta"><span class="count">{n} / 280</span>'
            f'<span><button class="mini" type="button" data-copy="post-{i}">Copy</button> '
            f'<a class="mini" href="{esc(intent)}" target="_blank" rel="noopener">Post on X</a></span></div></li>'
        )
    whole = "\n\n".join(thread())
    body = f"""<section class="hero"><div class="hero-in">
<p class="eyebrow"><b>&#9632;</b> Community summary</p>
<h1>{esc(smart(sm["title"]))}</h1>
<p class="sub">{esc(smart(sm["lede"]))}</p>
</div></section>
<div class="wrap"><main id="main" class="page" tabindex="-1">
<section class="card" aria-labelledby="sum-h"><div class="row"><h2 id="sum-h">A few paragraphs</h2>
<button class="mini" type="button" data-copy="sum-text">Copy the paragraphs</button></div>
<div id="sum-text" data-text="{esc(plain)}">{paras}</div>
<p class="small">The numbered markers show the source behind each statement. The copied text leaves them out; the full guide at <a href="{site}">{site}</a> keeps them.</p></section>
<section class="card" aria-labelledby="thread-h"><div class="row"><h2 id="thread-h">X thread, {len(posts)} posts</h2>
<button class="mini" type="button" data-copy="thread-all">Copy the whole thread</button></div>
<div id="thread-all" data-text="{esc(whole)}" hidden></div>
<ol class="posts">{"".join(posts)}</ol>
<p class="small">Counts follow X's rules, where a link counts as 23 characters. Every fact in the thread is cited in the guide.</p></section>
<section class="card"><h2>Downloads</h2><p><a href="{FILES["summary"]}">Community summary (Markdown)</a> &middot; <a href="{FILES["pdf"]}">Full guide (PDF)</a> &middot; <a href="index.html">Read the guide online</a></p></section>
</main></div>"""
    desc = "A short, shareable summary of Australia's Digital Assets Framework Act and an X thread for the Redbelly DAO community. Not legal advice."
    return page("Short version | " + D["explainer"]["title"], desc, "share.html", "share.html", body, with_evidence=True)


def usage_map():
    """evidence id -> list of (anchor, label) where it is cited."""
    titles = {s["id"]: s["title"] for s in D["explainer"]["sections"]}
    uses = {}
    for where, ids in content.citations(D):
        first = where.split()[0]
        if first in titles:
            anchor, label = "index.html#" + first, smart(titles[first])
        elif first in ("summary", "thread"):
            anchor, label = "share.html", "Short version to share"
        else:
            anchor, label = "index.html#short", "The short version"
        for eid in ids:
            lst = uses.setdefault(eid, [])
            if (anchor, label) not in lst:
                lst.append((anchor, label))
    return uses


def sources_page():
    with open(os.path.join(ROOT, "source-copies", "fingerprints.json"), encoding="utf-8") as fh:
        manifest = {c["id"]: c for c in json.load(fh)["pages"]}
    uses = usage_map()
    groups = []
    for kind, title in KIND_TITLES:
        cards = []
        for s in [s for s in D["sources"] if s["kind"] == kind]:
            evs = [e for e in D["evidence"] if e["source"] == s["id"]]
            m = manifest[s["id"]]
            quotes = "".join(
                f'<li id="e-{e["id"]}"><blockquote>\u201c{esc(e["quote"])}\u201d</blockquote>'
                f'<span class="at">{esc(e["at"])} &middot; used in '
                + ", ".join(f'<a href="{a}">{esc(l)}</a>' for a, l in uses.get(e["id"], []))
                + "</span></li>"
                for e in evs
            )
            cards.append(
                f'<article class="src" id="src-{s["n"]}"><div class="src-top"><span class="src-n">[{s["n"]}]</span><div>'
                f'<h3>{esc(smart(s["title"]))}</h3><p class="pub">{esc(s["publisher"])}</p>'
                f'<a class="url" href="{esc(s["url"])}" rel="noopener">{esc(s["url"])}</a>'
                f'<p class="meta">Saved copy <a href="source-copies/{m["file"]}">{m["file"]}</a> &middot; captured {m["captured_utc"]} &middot; SHA-256 {m["sha256"]}</p>'
                f'<details open><summary>{len(evs)} passage{"s" if len(evs) != 1 else ""} relied on</summary><ul class="quotes">{quotes}</ul></details>'
                "</div></div></article>"
            )
        groups.append(f'<section class="src-group"><h2>{title}</h2>{"".join(cards)}</section>')
    body = f"""<section class="hero"><div class="hero-in">
<p class="eyebrow"><b>&#9632;</b> Evidence</p>
<h1>Every source, and the exact words used</h1>
<p class="sub">{len(D["sources"])} sources, numbered as they are cited in the guide. Primary sources come first. Each passage is quoted word for word, with a link to the source and to a saved copy taken on {esc(D["explainer"]["checked"])}.</p>
<div class="actions"><a class="btn btn-fill" href="{FILES["sources"]}" download>Source list (Markdown)</a><a class="btn btn-line" href="source-copies/fingerprints.json">Saved copies with SHA-256</a></div>
</div></section>
<div class="wrap"><main id="main" class="page" tabindex="-1">{"".join(groups)}</main></div>"""
    desc = "Every source behind the Digital Assets Framework Act explainer, with the exact words relied on and a saved copy of each."
    return page("Sources | " + D["explainer"]["title"], desc, "source-list.html", "source-list.html", body)


def not_found_page():
    body = """<section class="hero"><div class="hero-in"><p class="eyebrow"><b>&#9632;</b> 404</p>
<h1>That page is not here</h1><p class="sub">The guide, the short version and the sources are all one click away.</p>
<div class="actions"><a class="btn btn-fill" href="index.html">Go to the guide</a><a class="btn btn-line" href="source-list.html">Sources</a></div></div></section>"""
    return page("Page not found | " + D["explainer"]["title"], "Page not found.", "404.html", "", body)


def thread():
    site = D["explainer"]["site_url"]
    return [p.replace("{site_url}", site) for p in D["summary"]["thread"]]


# ------------------------------------------------------------------ document (PDF and Word)

def doc_html(for_word=False):
    global WORD
    WORD = for_word
    ex = D["explainer"]
    mode = "doc"
    out = []
    logo = os.path.join(PUBLIC, "assets", "img", "logo-dark-bg.png")
    css = os.path.join(ROOT, "tools", "doc.css")
    if not for_word:
        out.append(f'<section class="cover"><img src="file://{logo}" alt="Redbelly DAO" class="logo">'
                   f'<p class="eyebrow">Plain-language explainer &middot; Redbelly DAO research</p>'
                   f"<h1>{esc(smart(ex['title']))}</h1><p class=\"sub\">{esc(smart(ex['subtitle']))}</p>"
                   f'<p class="checked">Sources checked {esc(ex["checked"])} &middot; {len(D["sources"])} sources &middot; {len(D["evidence"])} quoted passages</p></section>')
    else:
        out.append(f"<p><em>{esc(smart(ex['subtitle']))}</em></p>"
                   f"<p>Sources checked {esc(ex['checked'])}.</p>")
    out.append(doc_panel("notice", "Read this first", f'<p>{inline(ex["notice"], mode)}</p>'))
    out.append('<div class="keys">' + "".join(f"<p><b>{esc(k['date'])}</b> {inline(k['label'], mode)}</p>" for k in ex["key_dates"]) + "</div>")
    out.append('<p class="howto">Numbers in square brackets point to the sources at the end, where the exact words relied on are quoted. Text under <b>What the law says</b> and <b>What the companies say</b> reports the sources; text under <b>What this means</b> and <b>Not settled</b> is analysis.</p>')
    out.append('<h2 class="chap">The short version</h2>')
    for q in ex["short"]:
        out.append(f'<p class="q"><b>{esc(smart(q["q"]))}</b> {inline(q["a"], mode)}</p>')
    for i, sec in enumerate(ex["sections"], 1):
        out.append(f'<h2 class="chap"><span class="n">{i:02d}</span> {esc(smart(sec["title"]))}</h2>')
        if sec.get("lede"):
            out.append(f'<p class="lede">{inline(sec["lede"], mode)}</p>')
        law = []
        if "timeline" in sec:
            rows = "".join(f'<tr class="{t["state"]}"><td class="d">{esc(t["date"])}</td><td>{inline(t["text"], mode)}</td></tr>' for t in sec["timeline"])
            law.append(f'<table class="tl"><colgroup><col width="26%"><col width="74%"></colgroup><thead><tr><th>Date</th><th>What happens</th></tr></thead><tbody>{rows}</tbody></table>')
        law += [para(t, mode) for t in sec.get("law", [])]
        if "law_table" in sec:
            law.append(doc_table(sec["law_table"]))
        if law:
            out.append(doc_panel("law", "What the law says", "".join(law)))
        if "callout" in sec:
            c = sec["callout"]
            out.append(doc_panel("callout", esc(c["title"]), "".join(para(t, mode) for t in c["paragraphs"])))
        if "steps" in sec:
            st = sec["steps"]
            out.append(doc_panel("law", esc(st["title"]), "<ol>" + "".join(f"<li>{inline(t, mode)}</li>" for t in st["items"]) + f'</ol><p class="small">{inline(st["note"], mode)}</p>'))
        if "companies" in sec:
            out.append(doc_panel("co", "What the companies say", "".join(para(t, mode) for t in sec["companies"])))
        if "fit_table" in sec:
            out.append(doc_table(sec["fit_table"]))
        meaning = []
        if sec["id"] == "open":
            meaning.append("<ul>" + "".join(f"<li>{inline(t, mode)}</li>" for t in sec["meaning"]) + "</ul>")
        else:
            meaning += [para(t, mode) for t in sec.get("meaning", [])]
        if "meaning_table" in sec:
            meaning.append(doc_table(sec["meaning_table"]))
        if "checklist" in sec:
            cl = sec["checklist"]
            meaning.append(f"<p><b>{esc(cl['title'])}</b></p><ul>" + "".join(f"<li>{inline(t, mode)}</li>" for t in cl["items"]) + "</ul>")
        if meaning:
            out.append(doc_panel("mean", "What this means", "".join(meaning)))
        if sec.get("unsettled"):
            out.append(doc_panel("open", "Not settled", "".join(para(t, mode) for t in sec["unsettled"])))
    out.append('<h2 class="chap appendix">Sources and the exact words relied on</h2>')
    out.append(f'<p class="small">Saved copies of every source, with SHA-256 fingerprints, are published with the online guide at {esc(D["explainer"]["site_url"])}/source-list.html.</p>')
    for s in D["sources"]:
        evs = [e for e in D["evidence"] if e["source"] == s["id"]]
        items = "".join(f"<li>\u201c{esc(e['quote'])}\u201d <span class=\"at\">({esc(e['at'])})</span></li>" for e in evs)
        out.append(f'<div class="src"><p class="st"><b>[{s["n"]}] {esc(smart(s["title"]))}</b><br>{esc(s["publisher"])} &middot; <a href="{esc(s["url"])}">{esc(s["url"])}</a></p><ul>{items}</ul></div>')
    out.append(f'<p class="end">General information, not legal advice. Sources checked {esc(ex["checked"])}.</p>')
    style = "" if for_word else f'<link rel="stylesheet" href="file://{css}">'
    fonts = os.path.join(PUBLIC, "assets", "fonts")
    face = "" if for_word else "".join(
        f'@font-face{{font-family:"{fam}";src:url("file://{fonts}/{file}.woff2");font-weight:{w}}}'
        for fam, file, w in [("Be Vietnam Pro", "vietnam-400", 400), ("Be Vietnam Pro", "vietnam-500", 500),
                             ("Be Vietnam Pro", "vietnam-600", 600), ("Be Vietnam Pro", "vietnam-700", 700),
                             ("JetBrains Mono", "jbmono-400", 400), ("JetBrains Mono", "jbmono-500", 500)]
    )
    return (f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>{esc(ex["title"])}</title>'
            f"<style>{face}</style>{style}</head><body>" + "\n".join(out) + "</body></html>")


def doc_panel(kind, label, inner):
    if WORD:
        return f"<h4>{label}</h4>{inner}"
    return f'<div class="panel {kind}"><p class="label">{label}</p>{inner}</div>'


TABLE_WIDTHS = {3: ["28%", "36%", "36%"]}


def doc_table(tbl):
    widths = tbl.get("widths") or TABLE_WIDTHS.get(len(tbl["head"]), [])
    cols = "".join(f'<col width="{w}">' for w in widths)
    head_html = "".join(f"<th>{esc(smart(h))}</th>" for h in tbl["head"])
    rows = "".join("<tr>" + "".join(f"<td>{inline(c, 'doc')}</td>" for c in row) + "</tr>" for row in tbl["rows"])
    return (f'<table><caption>{esc(smart(tbl["caption"]))}</caption><colgroup>{cols}</colgroup>'
            f"<thead><tr>{head_html}</tr></thead><tbody>{rows}</tbody></table>")


# ------------------------------------------------------------------ Markdown

def guide_md():
    ex = D["explainer"]
    md = [f"# {smart(ex['title'])}", "", f"_{smart(ex['subtitle'])}_", "", f"Sources checked {ex['checked']}.", "",
          "> " + inline(ex["notice"], "md"), "",
          "Numbers in square brackets point to the source list at the end. Text under **What the law says** and **What the companies say** reports the sources; text under **What this means** and **Not settled** is analysis.", "",
          "## The short version", ""]
    for q in ex["short"]:
        md += [f"**{smart(q['q'])}** {inline(q['a'], 'md')}", ""]
    for i, sec in enumerate(ex["sections"], 1):
        md += [f"## {i}. {smart(sec['title'])}", "", f"_{inline(sec.get('lede', ''), 'md')}_", ""]
        if "timeline" in sec:
            md += ["### What the law says", "", "| Date | What happens |", "| --- | --- |"]
            md += [f"| {t['date']} | {inline(t['text'], 'md')} |" for t in sec["timeline"]]
            md.append("")
            md += [inline(t, "md") + "\n" for t in sec.get("law", [])]
        elif sec.get("law") or "law_table" in sec:
            md += ["### What the law says", ""] + [inline(t, "md") + "\n" for t in sec.get("law", [])]
        if "law_table" in sec:
            md += md_table(sec["law_table"])
        if "callout" in sec:
            md += [f"#### {sec['callout']['title']}", ""] + [inline(t, "md") + "\n" for t in sec["callout"]["paragraphs"]]
        if "steps" in sec:
            md += [f"#### {sec['steps']['title']}", ""] + [f"{j}. {inline(t, 'md')}" for j, t in enumerate(sec["steps"]["items"], 1)] + ["", "_" + inline(sec["steps"]["note"], "md") + "_", ""]
        if "companies" in sec:
            md += ["### What the companies say", ""] + [inline(t, "md") + "\n" for t in sec["companies"]]
        if "fit_table" in sec:
            md += md_table(sec["fit_table"])
        if sec.get("meaning") or "meaning_table" in sec or "checklist" in sec:
            md += ["### What this means", ""]
            if sec["id"] == "open":
                md += [f"- {inline(t, 'md')}" for t in sec["meaning"]] + [""]
            else:
                md += [inline(t, "md") + "\n" for t in sec.get("meaning", [])]
            if "meaning_table" in sec:
                md += md_table(sec["meaning_table"])
            if "checklist" in sec:
                md += [f"**{sec['checklist']['title']}**", ""] + [f"- {inline(t, 'md')}" for t in sec["checklist"]["items"]] + [""]
        if sec.get("unsettled"):
            md += ["### Not settled", ""] + [inline(t, "md") + "\n" for t in sec["unsettled"]]
    md += ["## Sources", ""] + source_list_lines()
    return "\n".join(md).rstrip() + "\n"


def md_table(tbl):
    rows = [f"**{smart(tbl['caption'])}**", "", "| " + " | ".join(smart(h) for h in tbl["head"]) + " |", "|" + " --- |" * len(tbl["head"])]
    rows += ["| " + " | ".join(inline(c, "md").replace("|", "\\|") for c in row) + " |" for row in tbl["rows"]]
    return rows + [""]


def source_list_lines():
    lines = []
    for s in D["sources"]:
        lines += [f"**[{s['n']}] {smart(s['title'])}**  ", f"{s['publisher']} · <{s['url']}>  ", f"Saved copy: `source-copies/{copy_name(s)}`", ""]
        for e in [e for e in D["evidence"] if e["source"] == s["id"]]:
            lines.append(f"- \u201c{e['quote']}\u201d ({e['at']})")
        lines.append("")
    return lines


def sources_md():
    ex = D["explainer"]
    return "\n".join([f"# Source list: {smart(ex['title'])}", "",
                      f"Sources checked {ex['checked']}. {len(D['sources'])} sources and {len(D['evidence'])} quoted passages. "
                      "Each passage is quoted word for word, with where it sits in the source. Saved copies with SHA-256 fingerprints are in `source-copies/`.",
                      "", "General information, not legal advice.", ""] + source_list_lines()).rstrip() + "\n"


def summary_md():
    site = D["explainer"]["site_url"]
    lines = ["# The Digital Assets Framework Act: the short version", "",
             f"Full guide with every source: {site}", ""]
    lines += [inline(t, "md") + "\n" for t in D["summary"]["paragraphs"]]
    lines += ["Numbers in square brackets refer to the source list in the full guide.", "", "## X thread", ""]
    for p in thread():
        lines += [p, ""]
    return "\n".join(lines).rstrip() + "\n"


# ------------------------------------------------------------------ outputs

def write(rel, text):
    path = os.path.join(PUBLIC, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def word(doc_path, out_path):
    ref = os.path.join(ROOT, "tools", "reference.docx")
    cmd = ["pandoc", doc_path, "-f", "html", "-t", "docx", "-o", out_path,
           "--metadata", "title=" + D["explainer"]["title"]]
    if os.path.exists(ref):
        cmd += ["--reference-doc", ref]
    subprocess.run(cmd, check=True)


def pdf(doc_path, out_path):
    script = os.path.join(ROOT, "tools", "pdf.cjs")
    subprocess.run(["node", script, doc_path, out_path, D["explainer"]["title"]], check=True)


def main(args):
    global D, EV, SRC
    D = content.load()
    EV = {e["id"]: e for e in D["evidence"]}
    SRC = {s["id"]: s for s in D["sources"]}
    os.makedirs(BUILD, exist_ok=True)

    write("index.html", index_page())
    write("share.html", summary_page())
    write("source-list.html", sources_page())
    write("404.html", not_found_page())

    ev_out = os.path.join(PUBLIC, "source-copies")
    if os.path.exists(ev_out):
        shutil.rmtree(ev_out)
    shutil.copytree(os.path.join(ROOT, "source-copies"), ev_out)

    write(FILES["md"], guide_md())
    write(FILES["summary"], summary_md())
    write(FILES["sources"], sources_md())

    word_html = os.path.join(BUILD, "guide-word.html")
    with open(word_html, "w", encoding="utf-8") as fh:
        fh.write(doc_html(for_word=True))
    word(word_html, os.path.join(PUBLIC, FILES["docx"]))

    if "--no-pdf" not in args:
        print_html = os.path.join(BUILD, "guide-print.html")
        with open(print_html, "w", encoding="utf-8") as fh:
            fh.write(doc_html())
        pdf(print_html, os.path.join(PUBLIC, FILES["pdf"]))
    print("built", ", ".join(sorted(os.listdir(PUBLIC))))


if __name__ == "__main__":
    main(sys.argv[1:])
