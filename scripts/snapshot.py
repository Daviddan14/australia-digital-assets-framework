"""Save a plain-text copy of every source listed in content/sources.yaml.

Each copy is written to evidence/snapshots/<id>.txt, and evidence/manifest.json
records where it came from, when it was captured (UTC) and its SHA-256, so
anyone can check that a quoted passage really appears in the source.

    python3 scripts/snapshot.py            # capture every source
    python3 scripts/snapshot.py act cp392  # capture only these ids

PDFs are converted with `pdftotext` (poppler-utils). Pages that only render
in a browser (marked `render: browser`) are read with Playwright's Chromium.
"""

import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP_DIR = os.path.join(ROOT, "evidence", "snapshots")
MANIFEST = os.path.join(ROOT, "evidence", "manifest.json")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"


def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def html_to_text(raw):
    text = raw.decode("utf-8", errors="replace")
    text = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", text)
    text = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|td|th|section|article|dd|dt)>", "\n", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    lines = [re.sub(r"[ \t ]+", " ", line).strip() for line in text.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def pdf_to_text(raw):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "source.pdf")
        with open(src, "wb") as fh:
            fh.write(raw)
        out = subprocess.run(["pdftotext", "-enc", "UTF-8", src, "-"], check=True, capture_output=True)
    return out.stdout.decode("utf-8")


def browser_text(url):
    script = os.path.join(ROOT, "scripts", "page_text.cjs")
    out = subprocess.run(["node", script, url], check=True, capture_output=True)
    return out.stdout.decode("utf-8").strip() + "\n"


def capture(src):
    url = src.get("fetch", src["url"])
    if src.get("render") == "browser":
        return browser_text(url)
    raw, ctype = fetch_bytes(url)
    if raw[:5] == b"%PDF-" or "pdf" in ctype:
        return pdf_to_text(raw)
    return html_to_text(raw)


def main(only):
    with open(os.path.join(ROOT, "content", "sources.yaml"), encoding="utf-8") as fh:
        sources = yaml.safe_load(fh)["sources"]
    manifest = {}
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding="utf-8") as fh:
            manifest = {c["id"]: c for c in json.load(fh)["copies"]}
    os.makedirs(SNAP_DIR, exist_ok=True)
    for src in sources:
        if only and src["id"] not in only:
            continue
        text = capture(src)
        path = os.path.join(SNAP_DIR, src["id"] + ".txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        data = text.encode("utf-8")
        manifest[src["id"]] = {
            "id": src["id"],
            "url": src["url"],
            "fetched_from": src.get("fetch", src["url"]),
            "file": "snapshots/" + src["id"] + ".txt",
            "captured_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        print(f"{src['id']:<22} {len(data):>8} bytes")
    order = [s["id"] for s in sources]
    copies = sorted(manifest.values(), key=lambda c: order.index(c["id"]) if c["id"] in order else len(order))
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump({"note": "Plain-text copies of every source, with SHA-256 of each file.", "copies": copies}, fh, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
