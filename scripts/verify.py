"""Check the explainer against its own rules before anything is published.

    python3 scripts/verify.py           # content and evidence checks
    python3 scripts/verify.py --links   # also request every source link

Checks:
  1. Every saved copy matches the SHA-256 in evidence/manifest.json.
  2. Every quoted passage appears word for word in its saved copy.
  3. Every citation in the content points to a known passage, and every
     passage is used at least once.
  4. Every paragraph under "What the law says" carries at least one citation.
  5. No sentence says Redbelly, Tokeniser or an issuer is licensed or
     compliant, and there is no price talk or investment advice.
  6. No personal credit (names, handles, "made by" lines) in the deliverables.
  7. The "not legal advice" statement opens every deliverable.
  8. Each post in the X thread fits in 280 characters.
Exits with status 1 if any check fails.
"""

import hashlib
import json
import os
import re
import sys
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import content  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36"

failures = []
passes = []


def check(ok, label, detail=""):
    (passes if ok else failures).append(label + (f": {detail}" if detail and not ok else ""))


def normalise(text):
    text = text.replace("­", "")
    text = re.sub(r"[‘’ʼ]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‐‑‒–—−]", "-", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"- (?=[a-z])", "-", text)
    return text.strip()


def main(check_links):
    data = content.load()
    sources = {s["id"]: s for s in data["sources"]}
    evidence = {e["id"]: e for e in data["evidence"]}
    with open(os.path.join(ROOT, "evidence", "manifest.json"), encoding="utf-8") as fh:
        manifest = {c["id"]: c for c in json.load(fh)["copies"]}

    # 1. saved copies are unchanged
    snapshots = {}
    for sid in sources:
        copy = manifest.get(sid)
        check(copy is not None, f"saved copy listed for {sid}")
        if not copy:
            continue
        with open(os.path.join(ROOT, "evidence", copy["file"]), "rb") as fh:
            raw = fh.read()
        check(hashlib.sha256(raw).hexdigest() == copy["sha256"], f"SHA-256 matches for {sid}")
        snapshots[sid] = normalise(raw.decode("utf-8"))

    # 2. quotes are in their saved copies
    for eid, ev in evidence.items():
        check(ev["source"] in sources, f"{eid} names a known source", ev["source"])
        found = normalise(ev["quote"]) in snapshots.get(ev["source"], "")
        check(found, f"quote {eid} found in {ev['source']}", ev["quote"][:80])

    # 3. citations resolve, and every passage is used
    used = set()
    for where, ids in content.citations(data):
        for cid in ids:
            used.add(cid)
            check(cid in evidence, f"citation in {where} resolves", cid)
    for eid in evidence:
        check(eid in used, f"passage {eid} is cited somewhere")

    # 4. statements of law are cited
    for where, text in content.law_paragraphs(data):
        check(bool(content.CITE.search(text)), f"law paragraph cited in {where}", text[:80])

    # 5. compliance claims, price talk, advice
    banned = [
        (r"\b(redbelly|tokeniser|issuer)s?\b[^.]{0,60}\b(is|are|has been|have been)\s+(fully\s+)?(licensed|compliant|approved|authorised)\b", "says a company is licensed or compliant"),
        (r"\b(price target|will (rise|increase) in value|returns? of \d|guaranteed return|buy rbnt|good investment|undervalued|to the moon)\b", "price talk or promised returns"),
        (r"\byou should (buy|sell|invest|hold)\b", "investment advice"),
    ]
    prose = list(content.all_prose(data))
    sentences = [s for _, t in prose for s in re.split(r"(?<=[.?!])\s+", t)]
    negated = re.compile(r"\b(no|not|never|nor|without)\b", re.I)
    for pattern, label in banned:
        hits = []
        for sentence in sentences:
            match = re.search(pattern, sentence, re.I)
            # "no sentence says X is compliant" is a statement about the guide, not a claim
            if match and not negated.search(sentence[: match.end()]):
                hits.append(sentence)
        check(not hits, f"no sentence {label}", hits[0][:100] if hits else "")

    # 6. no personal credit
    credit = re.compile(r"(made by|written by|prepared by|author:|@[a-z0-9_]{3,}|github\.com/[a-z0-9-]+|©\s*\d{4}\s+[A-Z])", re.I)
    hits = [t for _, t in prose if credit.search(t)]
    check(not hits, "no personal credit in the deliverables", hits[0][:100] if hits else "")

    # 7. not legal advice up front
    check("not legal advice" in data["explainer"]["notice"].lower(), "explainer opens with 'not legal advice'")
    check("not legal advice" in data["summary"]["paragraphs"][0].lower(), "summary opens with 'not legal advice'")

    # 8. thread posts fit
    for i, post in enumerate(data["summary"]["thread"], 1):
        n = content.x_length(post)
        check(n <= 280, f"post {i} fits in 280 characters", f"{n} characters")
    check(any("not legal advice" in p.lower() for p in data["summary"]["thread"]), "thread says 'not legal advice'")

    # links
    if check_links:
        for sid, src in sources.items():
            status = link_status(src["url"])
            check(status is not None and status < 400, f"link works for {sid}", f"{src['url']} -> {status}")

    for line in failures:
        print("FAIL  " + line)
    print(f"{len(passes)} checks passed, {len(failures)} failed")
    return 1 if failures else 0


def link_status(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status
        except urllib.error.HTTPError as err:
            if method == "GET":
                return err.code
        except Exception:
            if method == "GET":
                return None
    return None


if __name__ == "__main__":
    sys.exit(main("--links" in sys.argv))
